import rasterio
import rasterio.features
from shapely import geometry

out_dir = "D:\Doktorat\SenRiver\SenRiver\data"
tiff_path = 

with rasterio.open("D:\Downloads\mosaics\S2GM_Q10_20200701_20200930_Danube_STD_v1.3.0_278134\H189V41\B08_Q10_20200701_H189V41.tiff") as dataset:
    mask = dataset.dataset_mask()
    for geom, val in rasterio.features.shapes(mask, transform=dataset.transform):
        print(geom)
