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
import SCxrd_Data as data
import SCxrdApp_MultiPlot as multi

if __name__=='__main__':
    
    
    #Generate root window
    UI=ui.Widgets_SCxrd()
    UI.Create_Root()
    
    #create header
    UI.Create_Header(UI.root, 'Single Crystal XRD viewer', 0,0)
    
    #create load window
    UI.Create_LoadFrame(UI.root,'      No Data Loaded      ', 1, 0)
    
    UI.Load_B.configure(command=lambda: fnt.Button_LoadImage(UI, DataCL))
    
    UI.StepperF_B.configure(command=lambda: fnt.Button_NextFile(UI, DataCL,
                                                                'Forward'))
    UI.StepperB_B.configure(command=lambda: fnt.Button_NextFile(UI, DataCL,
                                                                'Back'))
    
    #create empty image
    UI.Create_EmptyImage(UI.root, 2, 0)
    
    
    #create empty plot
    UI.Create_EmptyPlot(UI.root, 2, 1, 1, 1)
    
    #create plot settings
    UI.Create_PlotSettings(UI.root, 2, 2)
    
    UI.Update_Bplot.configure(command=lambda: fnt.Button_ShowPlot(UI, DataCL))
    
    #create launch button for multiplot
    UI.Create_Launcher(UI.root, 'MultiPlot', 3, 2)
    UI.LaunchB.configure(command=lambda: multi.App_MultiPlot())
    
    #Generate data
    DataCL=data.SCxrd_Data(UI.DataLoc)
    
    #Run Window
    UI.root.mainloop()