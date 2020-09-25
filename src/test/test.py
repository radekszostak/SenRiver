import geopandas
import matplotlib.pyplot as plt
import sentinelsat
import shapely
from shapely import geometry, ops
import math
import numpy
from decimal import *
distance = 0.1


data = geopandas.read_file("data/gis/river/eu_river.shp")
L1 = data[data["R_level"]==1]
all = geometry.MultiLineString()
lines = []
for l in L1.geometry:
    lines.append(l)
multi_line = geometry.MultiLineString(lines)
merged_line = ops.linemerge(multi_line)

lines = []
for line in merged_line:
    lines.append(line.wkt+"\n")
outF = open("lines.txt", "w")
outF.writelines(lines)
line = merged_line[0]
dilated = line.buffer(0.1).simplify(0.05)
bounds = list(dilated.bounds)
multiplier = 10.0
print(bounds)
bounds[0] = math.floor(bounds[0]*multiplier)
bounds[1] = math.floor(bounds[1]*multiplier)
bounds[2] = math.ceil(bounds[2]*multiplier)
bounds[3] = math.ceil(bounds[3]*multiplier)
print(bounds)
xs = numpy.linspace(bounds[0],bounds[2],bounds[2]-bounds[0]+1)/multiplier
ys = numpy.linspace(bounds[1],bounds[3],bounds[3]-bounds[1]+1)/multiplier
#xs = [Decimal(str(x)).quantize(Decimal('.1')) for x in numpy.arange(bounds[0],bounds[2],0.1)]
#ys = [Decimal(str(y)).quantize(Decimal('.1')) for y in numpy.arange(bounds[1],bounds[3],0.1)]
print(xs)
print(ys)

polygons = []
for i in range(len(xs)-1):
    for j in range(len(ys)-1):
        polygon = geometry.Polygon([(xs[i],ys[j]), (xs[i+1], ys[j]), (xs[i+1], ys[j+1]), (xs[i], ys[j+1])])
        if dilated.intersects(polygon):
            polygons.append( polygon )

polygons = geometry.MultiPolygon(polygons)
outF = open("myOutFile.txt", "w")
outF.write(shapely.wkt.dumps(polygons, rounding_precision=1))
print(polygons.wkt)
grid.to_file("grid.shp")
print(dilated)
"""
current_dist = 0
points = []
while current_dist < line.length:
    points.append(line.interpolate(current_dist))
    current_dist += distance
square = points[0].buffer(1, cap_style=3)
print(square)
df = geopandas.GeoDataFrame(geometry=points)
df.plot()
plt.show()

print(line)
print("\n###\n")
"""

