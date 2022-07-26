"""
Imports needed for all applications
"""

import tkinter as tk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from tkinter import filedialog
from scipy.optimize import curve_fit
from random import randint
from PIL import Image,ImageTk
from numpy.linalg import inv
import tifffile as tiff 
import matplotlib.colors as colors


#load file location
file_location='::{B4BFCC3A-DB2C-424C-B029-7FE99A87C641}'
filename=filedialog.askopenfilename(initialdir=file_location,title='Select a file')

#read file and show
im=Image.open(filename)
im.show()

#make into array
imarray=np.array(im)
shape_im=imarray.shape
print(shape_im)
print(shape_im[0])
#print(im.size)
#print(imarray)

#grab intensity value
x,y=5,5
intensity=im.getpixel((shape_im[1]-1,shape_im[0]-1))
#print(intensity)
#print(np.max(imarray))

#show empty image
#size=imarray.shape
#empty=np.zeros(size)
#zeroimage=Image.fromarray(empty)
#zeroimage.show()

#show filled array image
#imarray_im=Image.fromarray(imarray)
#imarray_im.show()

