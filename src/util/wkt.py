import tkinter as tk
import shapely.wkt
import shapely.ops
import shapely.geometry
import math
import numpy

def multiLine2Line(multiLineString):
    lineString = shapely.ops.linemerge(shapely.wkt.loads(multiLineString))
    #assert lineString.geom_type == "LineString"
    return lineString.wkt

def line2MultiPolygon(lineString):
        dilated = shapely.wkt.loads(lineString).buffer(0.05).simplify(0.01)
        bounds = list(dilated.bounds)
        multiplier = 10.0
        bounds[0] = math.floor(bounds[0]*multiplier)
        bounds[1] = math.floor(bounds[1]*multiplier)
        bounds[2] = math.ceil(bounds[2]*multiplier)
        bounds[3] = math.ceil(bounds[3]*multiplier)
        print(bounds)
        xs = numpy.linspace(bounds[0],bounds[2],bounds[2]-bounds[0]+1)/multiplier
        ys = numpy.linspace(bounds[1],bounds[3],bounds[3]-bounds[1]+1)/multiplier
        polygons = []
        for i in range(len(xs)-1):
            for j in range(len(ys)-1):
                polygon = shapely.geometry.Polygon([(xs[i],ys[j]), (xs[i+1], ys[j]), (xs[i+1], ys[j+1]), (xs[i], ys[j+1])])
                if dilated.intersects(polygon):
                    polygons.append( polygon )
        polygons = shapely.geometry.MultiPolygon(polygons)
        assert polygons.geom_type == "MultiPolygon"
        return shapely.wkt.dumps(polygons, rounding_precision=1)

