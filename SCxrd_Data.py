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

import SCxrd_UI as ui
import SCxrd_Functions as fnt



class SCxrd_Data():
    
    def __init__(self,DataLocTK):
        #initial data
        self.data=pd.DataFrame() #for all array type data
        self.filenameTK=DataLocTK #location of data on disk
        
    
    def load_image(self):
        self.data_image=fnt.Load_Image(self.filenameTK.get())
        
    def load_DF(self):
        self.data_DF=fnt.Load_DF(self.filenameTK.get())
    
    def load_array(self):
        self.data_array=fnt.Load_Array(self.filenameTK.get())
        
    def get_pixels(self):
        DF=self.data_DF
        
        #get values as individual series
        x=DF['x']
        y=DF['y']
        I=DF['Intensity']
        
        #save DF to file to check
        #base_file_path = filedialog.asksaveasfilename(filetypes=(('Enter one name',''),('Enter one name','')))
        #DF.to_csv(base_file_path+'.csv',index=False)
        
        return x,y,I
        
        
        
        