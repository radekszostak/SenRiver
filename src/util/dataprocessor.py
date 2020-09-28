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

from skimage import exposure
from skimage.segmentation import quickshift, slic, mark_boundaries
import time

def getImagePair(r,g,b,ir):
    rgb = np.dstack((b*2.5,g*2.5,r*2.5))#getNaturalColor(b,g,r)
    rgb = rgb[1:-1,1:-1,:]
    ir = ir[1:-1,1:-1]
    """
    hist = np.histogram(ir.ravel(),256,[0,256])
    lab = hist[1][:-1]
    val = hist[0]
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.bar(lab,val)
    plt.show()
    
    #
    band_data = np.dstack([rgb,ir])
    # scale image values from 0.0 - 1.0
    img = exposure.rescale_intensity(band_data)
    
    # do segmentation multiple options with quickshift and slic
    #seg_start = time.time()
    # segments = quickshift(img, convert2lab=False)
    # segments = quickshift(img, ratio=0.8, convert2lab=False)
    # segments = quickshift(img, ratio=0.99, max_dist=5, convert2lab=False)
    # segments = slic(img, n_segments=100000, compactness=0.1)
    # segments = slic(img, n_segments=500000, compactness=0.01)
    segments = quickshift(img, convert2lab=False)
    plt.imshow(mark_boundaries(rgb, segments))
    #plt.show() 
    #print('segments complete', time.time() - seg_start)


    
    where = np.where(mask == 255)
    seg_set = set([])
    for x, y in zip(where[0],where[1]):
        seg_set.add(segments[x][y])
    for i, row in enumerate(segments):
        for j, val in enumerate(row):
            if val in seg_set:
                mask[i][j] = 255
    plt.imshow(mask)
    #plt.show()
    #mask = mask[1:-1,1:-1]
    """
    th, mask = cv.threshold(ir,19,255,cv.THRESH_BINARY_INV)
    return rgb, mask

def cropTiffByPolygon(tiff,polygon):
    out_image, out_transform = rasterio.mask.mask(tiff, [polygon], crop=True)
    out_image = out_image[0]
    th, mask = cv.threshold(out_image,254,255,cv.THRESH_BINARY_INV)
    out_image = rasterio.fill.fillnodata(out_image, mask=mask, max_search_distance=100.0, smoothing_iterations=0)
    return out_image


#subdir = "D:\Downloads\mosaics\S2GM_Q10_20200701_20200930_Danube_STD_v1.3.0_278134\H189V41"

order_dir = "D:\Downloads\mosaics\S2GM_Y10_20200101_20201231_Amazon_STD_v1.3.0_522021"
river_name = "Amazon"
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
        