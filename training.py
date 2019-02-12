#import scipy.io
import numpy as py
import matplotlib.pyplot as plt
import cv2
import glob
from PIL import Image

import os
import time

#%matplotlib inline
def main():

    #root = '/Users/elite/Desktop/Data Science Project/data'

    #normalImages = [cv2.imread(file) for file in glob.glob('/Users/elite/Desktop/Data Science Project/data/train/normal/*.jpeg')]

    #sklearn.datasets.load_files()


    i = Image.open('data/train/normal/IM-0115-0001.jpeg')
    iar = py.asarray(i)
    i2 = Image.open('data/train/normal/IM-0117-0001.jpeg')
    iar2 = py.array(i2)
    i3 = Image.open('data/train/normal/IM-0119-0001.jpeg')
    iar3 = py.array(i3)
    i4 = Image.open('data/train/normal/IM-0122-0001.jpeg')
    iar4 = py.array(i4)

    fig = plt.figure()
    ax1 = plt.subplot2grid((8,6),(0,0), rowspan=4, colspan=3)
    ax2 = plt.subplot2grid((8,6),(4,0), rowspan=4, colspan=3)
    ax3 = plt.subplot2grid((8,6),(0,3), rowspan=4, colspan=3)
    ax4 = plt.subplot2grid((8,6),(4,3), rowspan=4, colspan=3)


    ax1.imshow(iar)
    ax2.imshow(iar2)
    ax3.imshow(iar3)
    ax4.imshow(iar4)

    plt.show()



if __name__ == "__main__":
    main()
