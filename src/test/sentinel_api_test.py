from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
import secret

api = SentinelAPI(secret.user, secret.password, 'https://scihub.copernicus.eu/dhus')

# search by polygon, time, and SciHub query keywords
footprint = 'POINT (27.90904510917007 44.2479151246996)'

products = api.query(footprint,
                     date=(date(2015, 12, 29),'NOW'),
                     platformname='Sentinel-2',
                     producttype='S2MSI2A',
                     order_by='cloudcoverpercentage',
                     limit=1,
                     offset=2,
                     cloudcoverpercentage=(0, 2))

# convert to Pandas DataFrame
products_df = api.to_dataframe(products)

# download sorted and reduced products
out = api.download_all(products_df.index)
print(out)