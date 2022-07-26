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

import SCxrd_Functions as fnt

class Widgets_SCxrd:
    def __init__(self):
        #place commonly needed values here
        self.Root_title='Single Crystal XRD'
        
        #numbers for padding UI elements
        self.ExFrameY=5
        
        #multi-plot file lists
        self.file_list=[]
        
        self.FileVar_ref=[]
        self.I_MultiplyVar_ref=[]
        self.PlotLabelVar_ref=[]
        
        self.LoadB_ref=[]
        self.LoadDisplayL_ref=[]
        self.I_MultiBox_ref=[]
        self.PlotLabelBox_ref=[]
        
    
    def add_file(self,new_file):
        self.file_list.append(new_file)
        
    def remove_file(self):
        if self.file_list:
            self.file_list.pop()
            
    def reset_files(self):
        self.file_list=[]
        
    def generate_fileline(self,Master,start_row):
        #creates needed load widgets for multi-plot functions
        FileVar=tk.StringVar()
        FileVar.set('')
        
        FileDisplayVar=tk.StringVar()
        FileDisplayVar.set('.....')
        
        LoadB=tk.Button(Master.MultiSettings, text='Load Data',command=lambda: fnt.Button_LoadMulti(Master,FileVar,FileDisplayVar))
        LoadDisplayL=tk.Label(Master.MultiSettings,textvariable=FileDisplayVar,bg='white')
        
        I_MultiplyVar=tk.StringVar()
        I_MultiplyVar.set(1)
        
        I_MultiBox=tk.Entry(Master.MultiSettings,textvariable=I_MultiplyVar)
        
        PlotLabelVar=tk.StringVar()
        PlotLabelVar.set('')
        
        PlotLabelBox=tk.Entry(Master.MultiSettings,textvariable=PlotLabelVar)
        
        
        
        
        #place onto screen
        LoadB.grid(row=start_row,column=0)
        LoadDisplayL.grid(row=start_row,column=1)
        I_MultiBox.grid(row=start_row,column=2)
        PlotLabelBox.grid(row=start_row,column=3)
        
        
        #package widgets for use
        Vars=[FileVar,I_MultiplyVar,PlotLabelVar]
        Widgets=[LoadB,LoadDisplayL,I_MultiBox,PlotLabelBox]
        
        
        return Vars,Widgets
    
    def add_fileline(self,Master):
        #get current data count
        dataNum=self.DataCount.get()
        row_start=dataNum+1
        
        #generate new load elements
        Vars,Widgets=self.generate_fileline(Master, row_start)
        
        #update lists
        self.FileVar_ref.append(Vars[0])
        self.I_MultiplyVar_ref.append(Vars[1])
        self.PlotLabelVar_ref.append(Vars[2])
        
        self.LoadB_ref.append(Widgets[0])
        self.LoadDisplayL_ref.append(Widgets[1])
        self.I_MultiBox_ref.append(Widgets[2])
        self.PlotLabelBox_ref.append(Widgets[3])
        
        self.DataCount.set(dataNum+1)
        print(self.DataCount.get())
        
    def remove_fileline(self):
        #check if you even can remove a file
        if self.DataCount.get():
            print('removing line')
            dataNum=self.DataCount.get()
            self.DataCount.set(dataNum-1)
            
            self.FileVar_ref.pop()
            self.I_MultiplyVar_ref.pop()
            self.PlotLabelVar_ref.pop()
            
            self.LoadB_ref[-1].grid_forget()
            self.LoadDisplayL_ref[-1].grid_forget()
            
            self.LoadB_ref.pop()
            self.LoadDisplayL_ref.pop()
            
            self.I_MultiBox_ref[-1].grid_forget()
            self.I_MultiBox_ref.pop()
            
            self.PlotLabelBox_ref[-1].grid_forget()
            self.PlotLabelBox_ref.pop()
        
    def Create_Root(self):
        self.root=tk.Tk()
        #self.root.configure(bg='#525F88')
        self.root.title(self.Root_title)
        #self.root.iconbitmap(icon)
        
    
    def Create_TopLevel(self,title):
        #controls the window for cooling and warming
        self.rootApp=tk.Toplevel()
        self.rootApp.title(title)
        #self.rootApp.iconbitmap(icon)
        self.rootApp.grab_set() #places this window as a priority for events
        
    def Create_Launcher(self,MasterTK,title,row,column):
        #creates button for launcher
        self.LaunchB=tk.Button(MasterTK,text=title)
        self.LaunchB.grid(row=row,column=column)
        
    def Create_Header(self,MasterTK,title,row,column):
        self.Header_L=tk.Label(MasterTK,text=title)
        self.Header_L.grid(row=row,column=column,pady=(0,10))
        
    def Create_LoadFrame(self,MasterTK,dataloc_i,row,column):
        #creates standard loadframe use for applications
        self.LoadFrame=tk.LabelFrame(MasterTK,text='Check/Change Loaded Data')
        self.LoadFrame.grid(row=row,column=column,padx=10,pady=self.ExFrameY,sticky=tk.W)
        
        
        #Widgets and placement
        #file and machine selection for data
        self.DataLoc=tk.StringVar()
        self.DataLoc.set(dataloc_i)
        
        self.DataDisplay=tk.StringVar()
        self.DataDisplay.set(dataloc_i[0:10]+'.......'+dataloc_i[-10:])
        
        #load data widgets
        self.Load_B=tk.Button(self.LoadFrame,text="Load data")
        
        self.Load_B.grid(row=0,column=0)
        
        self.Loadcheck_L=tk.Label(self.LoadFrame,text='File:')
        self.Loadcheck_L.grid(row=0,column=1)
        
        self.Loadcheck_E=tk.Label(self.LoadFrame,textvariable=self.DataDisplay,bg='white')
        self.Loadcheck_E.grid(row=0,column=2)
        
        #create stepper for going through data
        self.StepperB_B=tk.Button(self.LoadFrame,text='previous')
        self.StepperF_B=tk.Button(self.LoadFrame,text='next')
        
        self.StepperB_B.grid(row=1,column=0)
        self.StepperF_B.grid(row=1,column=1)
        
        
    def Create_EmptyImage(self,MasterTK,row,column):
        #create empty Image
        emptyImPic=fnt.EmptyImage()
        
        #place image in label and show
        self.XRD_Image=tk.Label(MasterTK,image=emptyImPic)
        self.XRD_Image.image=emptyImPic
        self.XRD_Image.grid(row=row,column=column)
        
        #place update button
        self.Update_Bimage=tk.Button(MasterTK,text='Update Image')
        Update_row=row+1
        self.Update_Bimage.grid(row=Update_row,column=column,sticky=tk.W)
    
    def Create_EmptyPlot(self,MasterTK,row,column,rowspan_plot,columnspan_plot):
        #create plot and put on screen. Have it empty to start
        self.canvas,self.Fig,self.Plot,self.toolbarFrame,self.cb=fnt.Empty_Plot(MasterTK)
        self.Plot.tick_params(direction='in')
        #set plot to screen
        self.canvas.get_tk_widget().grid(row=row,column=column,rowspan=rowspan_plot,columnspan=columnspan_plot)
    
        
        self.toolbarFrame.grid(row=row+rowspan_plot,column=column,columnspan=columnspan_plot)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)
        
        
    
    def Create_PlotSettings(self,MasterTK,row,column):
        #settings for controling plot area and max intensity
        
        #the frame
        self.PlotSettingFrame=tk.LabelFrame(MasterTK,text='plot window settings')
        self.PlotSettingFrame.grid(row=row,column=column)
        
        #give starting off button image
        Off=Image.open('off.png')
        OffPic=ImageTk.PhotoImage(Off)
        
        #text variables needed
        self.SettingToggle=tk.BooleanVar()
        self.SettingToggle.set(False)
        
        self.xMin=tk.DoubleVar()
        self.xMin.set(0)
        
        self.xMax=tk.DoubleVar()
        self.xMax.set(0)
        
        self.yMin=tk.DoubleVar()
        self.yMin.set(0)
        
        self.yMax=tk.DoubleVar()
        self.yMax.set(0)
        
        self.IMax=tk.DoubleVar()
        self.IMax.set(0)
        
        
        #fillable settings in frame
        self.ToggleButton=tk.Button(self.PlotSettingFrame,image=OffPic,bd=0,command=lambda: fnt.SwitchButton(self.ToggleButton, self.SettingToggle))
        self.ToggleButton.image=OffPic
        self.ToggleButton.grid(row=0,column=0)
        
        self.xMinPixel_E=tk.Entry(self.PlotSettingFrame,textvariable=self.xMin)
        self.xMinPixel_E.grid(row=1,column=0)
        
        self.xMinPixel_L=tk.Label(self.PlotSettingFrame,text='X min')
        self.xMinPixel_L.grid(row=2,column=0)
        
        self.xMaxPixel_E=tk.Entry(self.PlotSettingFrame,textvariable=self.xMax)
        self.xMaxPixel_E.grid(row=1,column=1)
        
        self.xMaxPixel_L=tk.Label(self.PlotSettingFrame,text='X max')
        self.xMaxPixel_L.grid(row=2,column=1)
        
        self.yMaxPixel_E=tk.Entry(self.PlotSettingFrame,textvariable=self.yMax)
        self.yMaxPixel_E.grid(row=3,column=1)
        
        self.yMaxPixel_L=tk.Label(self.PlotSettingFrame,text='Y max')
        self.yMaxPixel_L.grid(row=4,column=1)
        
        self.yMinPixel_E=tk.Entry(self.PlotSettingFrame,textvariable=self.yMin)
        self.yMinPixel_E.grid(row=3,column=0)
        
        self.yMinPixel_L=tk.Label(self.PlotSettingFrame,text='Y min')
        self.yMinPixel_L.grid(row=4,column=0)
        
        self.IMax_E=tk.Entry(self.PlotSettingFrame,textvariable=self.IMax)
        self.IMax_E.grid(row=5,column=0)
        
        self.IMax_L=tk.Label(self.PlotSettingFrame,text='I max')
        self.IMax_L.grid(row=6,column=0)
        
        #update button
        self.Update_Bplot=tk.Button(self.PlotSettingFrame,text='Update Plot')
        self.Update_Bplot.grid(row=7,column=1)
        
        
    def Create_MultiPlotSettings(self,MasterTK,row,column):
        
        #needed variable
        self.DataCount=tk.IntVar()
        self.DataCount.set(0)
        
        #this frame
        self.MultiSettings=tk.LabelFrame(MasterTK)
        self.MultiSettings.grid(row=row,column=column)
        
        #file settings
        self.AddFileB=tk.Button(self.MultiSettings,text='Add File')
        self.AddFileB.grid(row=0,column=0)
        
        self.RemoveFileB=tk.Button(self.MultiSettings,text='Remove File')
        self.RemoveFileB.grid(row=0,column=1)
        
    def Create_PlotButton(self,MasterTK,row,column):
        
        self.MultiPlot_B=tk.Button(MasterTK,text='Show MultiPlot')
        self.MultiPlot_B.grid(row=row,column=column)
        
        
        
        