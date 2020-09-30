import os
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import json

dir = "D:\Doktorat\SenRiver\SenRiver\data\pairs\Danube"
ir_dir = os.path.join(dir,"ir")
mask_dir = os.path.join(dir,'mask')
if not os.path.exists(mask_dir):
    os.makedirs(mask_dir)
names = os.listdir(ir_dir)
l = str(len(names))
histogram = np.array([0]*256)
for i, name in enumerate(names):
    print(str(i)+"/"+l)
    ir = cv.imread(os.path.join(ir_dir,name))
    hist, bins = np.histogram(ir.flatten(),bins = range(256))
    histogram = [x + y for x, y in zip(histogram, hist)]

center = 22
histogram[254]=0
start = histogram[:center].index(max(histogram[:center]))
stop = histogram[center:].index(max(histogram[center:]))+center
#start = 13
#stop = 73
cut = histogram[start:stop]
th = cut.index(min(cut))+start
plt.axvline(x=th, color='red')
plt.axvline(x=start, color='yellow')
plt.axvline(x=stop, color='yellow')
plt.axvline(x=center, color='yellow')
plt.hist(range(255),range(256), weights = histogram)
plt.savefig(os.path.join(dir,"histogram.png"))
plt.show()
dump = json.dumps({'histogram': str(histogram), 'start': start, 'stop': stop, 'threshold': th})
with open(os.path.join(dir,"dump.json"),"w+") as file:
    file.writelines(dump)

for i, name in enumerate(names):
    print(str(i)+"/"+l)
    ir = cv.imread(os.path.join(ir_dir,name))
    thr, mask = cv.threshold(ir,th,255,cv.THRESH_BINARY_INV)
    cv.imwrite(os.path.join(mask_dir,name),mask)