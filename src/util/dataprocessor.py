import rasterio
import rasterio.mask
import rasterio.fill
import shapely.wkt
import shapely.geometry
from dataloader import *
import os
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt


histogram = [0]*256
"""
arr = [7351, 59207, 517782, 2523349, 6016352, 9464772, 11187272, 11457639, 11971765, 13413846, 14944536, 15433808, 14347374, 12048750, 10558530, 9020942, 7956455, 7657302, 7820728, 7167020, 5728236, 4354547, 3736215, 2812963, 1872242, 1216544, 927607, 746448, 661068, 613623, 
603210, 577400, 580521, 580131, 581102, 587031, 580776, 608086, 626462, 651738, 662323, 716023, 760739, 810208, 849942, 948414, 1032537, 1140834, 1274156, 1388360, 1607759, 1843796, 2129549, 2449630, 2870093, 3271951, 3936327, 4623501, 5475473, 6244188, 7475146, 8597975, 9874536, 10862020, 13022260, 13695012, 15864653, 16646344, 17720061, 19854044, 19742650, 21368657, 21016669, 21011532, 22379188, 20744522, 20307535, 20752786, 18758731, 18718136, 16816846, 15716662, 15266314, 13199209, 12779099, 11051234, 9918286, 9435727, 7946410, 7064300, 6658463, 5541325, 5108138, 4299068, 3725765, 3440748, 2822765, 2576816, 2131029, 1818645, 1672373, 1351462, 1172898, 1002990, 908703, 735505, 662907, 536777, 452980, 411289, 330292, 280791, 253867, 200172, 179656, 143321, 121938, 108627, 86835, 76167, 60835, 50875, 44631, 35021, 29024, 26017, 20172, 18577, 13819, 11567, 9531, 8043, 7594, 5890, 5060, 4434, 3864, 3304, 3316, 2505, 2191, 1903, 1779, 1709, 1420, 1131, 1020, 843, 685, 441, 358, 287, 241, 207, 144, 95, 81]
arr = arr[13:73]
print(arr.index(min(arr))+13)
arr = [np.log10(v) for v in arr]

plt.hist(arr, bins = range(len(arr))) 
plt.show()
"""
def getImagePair(r,g,b,ir):
    global histogram
    rgb = np.dstack((b*2.5,g*2.5,r*2.5))#getNaturalColor(b,g,r)
    rgb = rgb[1:-1,1:-1,:]
    ir = ir[1:-1,1:-1]
    hist, bins = np.histogram(ir.flatten(),bins = range(256))
    histogram = [x + y for x, y in zip(histogram, hist)]
    print(histogram)
    
    return rgb, ir

def cropTiffByPolygon(tiff,polygon):
    out_image, out_transform = rasterio.mask.mask(tiff, [polygon], crop=True)
    out_image = out_image[0]
    th, mask = cv.threshold(out_image,254,255,cv.THRESH_BINARY_INV)
    out_image = rasterio.fill.fillnodata(out_image, mask=mask, max_search_distance=100.0, smoothing_iterations=0)
    return out_image


#subdir = "D:\Downloads\mosaics\S2GM_Q10_20200701_20200930_Danube_STD_v1.3.0_278134\H189V41"

order_dir = "D:\Downloads\mosaics\S2GM_Q10_20200701_20200930_Danube_STD_v1.3.0_278134"#"D:\Downloads\mosaics\S2GM_Y10_20200101_20201231_Amazon_STD_v1.3.0_522021"
river_name = "Danube"
output_dir = os.path.join("D:\Doktorat\SenRiver\SenRiver\data\pairs",river_name)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
rgb_dir = os.path.join(output_dir,'rgb')
if not os.path.exists(rgb_dir):
    os.makedirs(rgb_dir)
ir_dir = os.path.join(output_dir,'ir')
if not os.path.exists(ir_dir):
    os.makedirs(ir_dir)
mask_dir = os.path.join(output_dir,'mask')
if not os.path.exists(mask_dir):
    os.makedirs(mask_dir)


subdirs = os.listdir(order_dir)
for subdir in subdirs:
    subdir = os.path.join(order_dir,subdir)
    if os.path.isdir(subdir):
        files = os.listdir(subdir)
        pathes = {}
        for file in files:
            if file.startswith("B02"):
                pathes["b"] = os.path.join(subdir,file)
            elif file.startswith("B03"):
                pathes["g"] = os.path.join(subdir,file)
            elif file.startswith("B04"):
                pathes["r"] = os.path.join(subdir,file)
            elif file.startswith("B08"):
                pathes["ir"] = os.path.join(subdir,file)


        rivers = read_rivers_csv("data/majorrivers.csv")
        river = rivers[river_name]
        polygons = list(shapely.wkt.loads(river['area']))


        tiffs = {}
        for band in pathes:
            tiffs[band] = rasterio.open(pathes[band])
            

        bounds  = tiffs["ir"].bounds
        box = shapely.geometry.box(*bounds).buffer(-0.01)
        for polygon in polygons:
            if polygon.intersects(box):
                
                r = cropTiffByPolygon(tiffs["r"],polygon)
                g = cropTiffByPolygon(tiffs["g"],polygon)
                b = cropTiffByPolygon(tiffs["b"],polygon)
                ir = cropTiffByPolygon(tiffs["ir"],polygon)
                rgb, ir = getImagePair(r,g,b,ir)
                file_base_name = "{}_{}_{}_{}".format(*polygon.bounds)
                cv.imwrite(os.path.join(rgb_dir,file_base_name+".jpg"),rgb)
                cv.imwrite(os.path.join(ir_dir,file_base_name+".png"),ir)

plt.hist(histogram, bins = range(256)) 
plt.show()
start = 13
stop = 73
histogram = histogram[start:stop]
th = histogram.index(min(histogram))+start
print(th)
ir_names = os.listdir(ir_dir)
for ir_name in ir_names:
    ir = cv.imread(os.path.join(ir_dir,ir_name))
    thr, mask = cv.threshold(ir,th,255,cv.THRESH_BINARY_INV)
    cv.imwrite(os.path.join(mask_dir,ir_name),mask)