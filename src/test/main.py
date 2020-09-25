import json
import tkinter as tk
from functions import *

with open('data/rivers.json', 'r') as f:
    data = json.load(f)

class Window:
    

class River:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Input")
        self.nameLabel = tk.Label(self.parent, "Name:")
        self.nameLabel.pack()
        self.nameEntry = tk.Entry(self.parent)
        self.nameEntry.pack()
        self.dischargeLabel = tk.Label(self.parent, "Discharge:")
        self.dischargeLabel.pack()
        self.dischargeEntry = tk.Entry(self.parent)
        self.dischargeEntry.pack()
        self.multiLineLabel = tk.Label(self.parent, "MultiLineText:")
        self.multiLineLabel.pack()
        self.multiLineText = tk.Text(self.parent)
        self.multiLineText.pack()
        self.button = tk.Button(parent, text='OK', command=self.confirm)
        self.button.pack()
    def confirm(self):
        global data
        name = self.nameEntry.get(1.0, 'end-1c')
        discharge = self.dischargeEntry.get(1.0, 'end-1c')
        lineString = multiLine2Line(self.multiLineText.get(1.0, 'end-1c'))
        multiPolygonString = line2MultiPolygon(lineString)
        data[name] = {"discharge": discharge, "lineString": lineString, "multiPolygonString": multiPolygonString}
        #self.text.delete(1.0, tk.END)
        #self.text.insert(tk.END, LineString)
    

root = tk.Tk()
input = Input(root)
root.mainloop()



with open('data.json', 'w') as f:
    json.dump(data, f, indent=4)

print(json.dumps([{"danube":{"discharge": "", "line": "l_val", "multipolygon": "multi_val"}}]))


