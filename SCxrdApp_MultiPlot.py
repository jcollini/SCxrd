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


def App_MultiPlot():
    
    #create app ojects
    UI=ui.Widgets_SCxrd()
    UI.Create_TopLevel('MultiPlot')
    
    UI.Create_Header(UI.rootApp, 'Plot multiple XRD scans in same detector position', 0, 0)
    
    UI.Create_MultiPlotSettings(UI.rootApp,1,0)
    UI.AddFileB.configure(command=lambda: fnt.Button_AddMultiLine(UI))
    UI.RemoveFileB.configure(command=lambda: fnt.Button_RemoveMultiLine(UI))
    
    UI.Create_PlotSettings(UI.rootApp, 2, 0)
    
    UI.Create_PlotButton(UI.rootApp,2,1)
    UI.MultiPlot_B.configure(command=lambda: fnt.Button_PlotMulti(UI))
    
    
