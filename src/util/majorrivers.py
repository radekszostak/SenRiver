import geopandas
import csv
import wkt

data = geopandas.read_file("data\gis\major_rivers\MajorRivers.shp")

with open('data/discharge.csv', mode = 'r') as discharge_file:
    discharges = list(csv.reader(discharge_file, delimiter=';', quotechar='\"'))

with open('data/majorrivers.csv', mode='w',newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for index, row in data.iterrows():
        name = row['NAME'].strip("\r\n")
        line = row['geometry'].wkt
        area = wkt.line2MultiPolygon(line)
        discharge = ""
        length = ""
        continent = ""
        for row in discharges:
            if row[2].strip() == name:
                discharge = str(row[3]).strip()
                length = str(row[5]).strip()
                continent = str(row[1]).strip()

        #if line.startswith("MULTILINE"):
        #    line = wkt.multiLine2Line(line)

        csv_writer.writerow([name, line, area, continent, discharge, length])

