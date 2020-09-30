import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog
import os
import cv2 as cv
import numpy as np

class Window:
    def __init__(self, parent):
        self._job = None
        self.parent = parent
        self.parent.title("Pairs editor")
        self.dir = filedialog.askdirectory()
        self.rgb_dir = os.path.join(self.dir,"rgb")
        self.ir_dir = os.path.join(self.dir,"ir")
        self.mask_dir = os.path.join(self.dir,"mask")
        self.names = [os.path.splitext(name)[0] for name in os.listdir(self.rgb_dir)]
        self.left = tk.Label(self.parent)
        self.right = tk.Label(self.parent)
        self.next_btn = tk.Button(self.parent, text="Next")
        self.prev_btn = tk.Button(self.parent, text="Previous")
        #self.slider = tk.Scale(self.parent, from_=0, to=255, orient="horizontal", command=self.updateValue)
        #self.slider.pack()
        #self.win2 = tk.Toplevel(self.parent)
        self.load(0)
    def load(self, n):
        rgb = Image.open(os.path.join(self.rgb_dir,self.names[n]+".jpg"))
        rgb = rgb.resize((600, 600), Image.ANTIALIAS)
        rgb = ImageTk.PhotoImage(rgb)
        self.left.configure(image=rgb)
        self.left.image = rgb
        self.left.grid(row=0,column=0)
        #self.ir_arr = cv.imread(os.path.join(ir_dir,self.names[n]+".png"))
        #th, mask = mask(self.ir_arr, -1)
        #self.slider.set(th)
        ir = Image.open(os.path.join(self.mask_dir,self.names[n]+".png"))#Image.fromarray(mask)#
        ir = ir.resize((600, 600), Image.ANTIALIAS)
        ir = ImageTk.PhotoImage(ir)
        self.right.configure(image=ir)
        self.right.image = ir
        self.right.grid(row=0,column=1)
        self.next_btn.configure(command= lambda: self.load(n+1))
        self.next_btn.grid(row=1,column=1)
        self.prev_btn.configure(command= lambda: self.load(n-1))
        self.prev_btn.grid(row=1,column=0)
    """
    def mask(im, th=-1)
        if th == -1:
            hist, bins = np.histogram(im.flatten(),bins = range(256))
            #histogram = [x + y for x, y in zip(histogram, hist)]
            start = 13
            stop = 73
            cut = hist[start:stop]
            th = cut.index(min(cut))+start
            return cv.threshold(im,th,255,cv.THRESH_BINARY_INV)
        else:
            return cv.threshold(im,th,255,cv.THRESH_BINARY_INV)
        th = histogram.index(min(histogram))
    
    def updateValue(self, event):
        if self._job:
            self.parent.after_cancel(self._job)
        self._job = self.root.after(500, self.updateMask)
    def updateMask(self):
        self._job = None
        th = self.slider.get()
        mask_arr = mask(self.ir_arr,th)
        mask = Image.fromarray(mask)
        self.right.configure(image=mask)
        self.right.image = mask
        self.right.grid(row=0,column=1)
    """
root = tk.Tk()
window = Window(root)
root.mainloop()