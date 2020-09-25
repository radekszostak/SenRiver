import tkinter as tk
import shapely.wkt
import shapely.ops
import shapely.geometry
import math
import numpy

class Input:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Input")
        self.text = tk.Text(self.parent)
        self.text.pack()
        self.button = tk.Button(parent, text='OK', command=self.confirm)
        self.button.pack()
    def confirm(self):
        LineString = self.text.get(1.0, 'end-1c')
        
        dilated = shapely.wkt.loads(LineString).buffer(0.05).simplify(0.01)
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
               
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, shapely.wkt.dumps(polygons, rounding_precision=1))


root = tk.Tk()
input = Input(root)
root.mainloop()