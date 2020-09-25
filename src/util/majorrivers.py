import geopandas
import csv
import wkt

data = geopandas.read_file("data\gis\major_rivers\MajorRivers.shp")

with open('data/majorrivers.csv', mode='w',newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for index, row in data.iterrows():
        name = row['NAME'].strip("\r\n")
        line = row['geometry'].wkt
        area = wkt.line2MultiPolygon(line)
        #if line.startswith("MULTILINE"):
        #    line = wkt.multiLine2Line(line)

        csv_writer.writerow([name, line, area])

