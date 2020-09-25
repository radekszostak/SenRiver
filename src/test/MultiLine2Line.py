import tkinter as tk
import shapely.wkt
import shapely.ops

class Input:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Input")
        self.text = tk.Text(self.parent)
        self.text.pack()
        self.button = tk.Button(parent, text='OK', command=self.confirm)
        self.button.pack()
    def confirm(self):
        LineString = shapely.ops.linemerge(shapely.wkt.loads(self.text.get(1.0, 'end-1c'))).wkt
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, LineString)


root = tk.Tk()
input = Input(root)
root.mainloop()