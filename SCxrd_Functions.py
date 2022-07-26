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


def Button_LoadImage(MasterTK,DataCL):
    #button to grab datafile location
    #objects needed:
    DataLocTK=MasterTK.DataLoc
    DataDisplayTK=MasterTK.DataDisplay
    XRD_ImageTK=MasterTK.XRD_Image
    Plot_PLT=MasterTK.Plot
    Fig_PLT=MasterTK.Fig
    canvas_PLT=MasterTK.canvas
    cb_PLT=MasterTK.cb
        
    #Start at desktop
    file_location='::{B4BFCC3A-DB2C-424C-B029-7FE99A87C641}'
    MasterTK.filename=filedialog.askopenfilename(initialdir=file_location,title='Select a file')
    fn=MasterTK.filename
    
    #update the entry with the new file. Clear it first
    DataLocTK.set(fn)
    DataDisplayTK.set(fn[-40:])
    
    #show image and plot immediately
    Button_QuickShowImage(MasterTK,XRD_ImageTK,DataCL)
    Button_ShowPlot3(MasterTK,Plot_PLT,Fig_PLT,canvas_PLT,cb_PLT,DataCL)
    
def Button_LoadMulti(Master,FileVar,FileDisplay):
    #button to grab datafile location
        
    #Start at desktop
    file_location='::{B4BFCC3A-DB2C-424C-B029-7FE99A87C641}'
    Master.filename=filedialog.askopenfilename(initialdir=file_location,title='Select a file')
    fn=Master.filename
    
    #update the entry with the new file. Clear it first
    FileVar.set(fn)
    FileDisplay.set(fn[-40:])
    
    
def Button_AddMultiLine(Master):
    #adds file line to multiplot UI
    
    Master.add_fileline(Master)
    
def Button_RemoveMultiLine(Master):
    
    Master.remove_fileline()
    
    
    
    
def Button_QuickShowImage(MasterTK,XRD_ImageTK,DataCL):
    #load curent image
    DataCL.load_image()
    
    #place image into label
    XRD_ImageTK.configure(image=DataCL.data_image)
    XRD_ImageTK.image=DataCL.data_image
    
    
    
def Button_ShowPlot2(MasterTK,Plot_PLT,Fig_PLT,canvas_PLT,cb_PLT,DataCL):
    #load current image as DF
    DataCL.load_DF()
    
    #get pixels and intensities
    x,y,I=DataCL.get_pixels()
    
    #set scale limit on I
    ScaleLimit=1.0
    Imax=I.max()*ScaleLimit
    Imin=60000
    
    #clear plot
    Plot_PLT.clear()
    
    #create plot
    axes=Plot_PLT.scatter(x,y,c=I,linewidths=0,cmap='viridis')
    
    Plot_PLT.tick_params(axis="y",direction="in",color='white',left=True,right=True)
    Plot_PLT.tick_params(axis="x",direction="in",color='white',top=True,bottom=True)
    Fig_PLT.colorbar(axes)
    canvas_PLT.draw()
    

def Button_ShowPlot3(MasterTK,Plot_PLT,Fig_PLT,canvas_PLT,cb_PLT,DataCL):
    #load current image as array
    DataCL.load_array()
    data_array=DataCL.data_array
    
    #clear plot
    Plot_PLT.clear()
    
    #create plot
    axes=Plot_PLT.imshow(data_array,norm=colors.LogNorm(),cmap='viridis')
    
    Plot_PLT.tick_params(axis="y",direction="in",color='white',left=True,right=True)
    Plot_PLT.tick_params(axis="x",direction="in",color='white',top=True,bottom=True)
    cb_PLT.mappable.set_clim(vmin=np.min(data_array),vmax=np.max(data_array))
    cb_PLT.draw_all()
    canvas_PLT.draw()
    

def Button_ShowPlot(Master,DataCL):
    #load current image as array
    DataCL.load_array()
    data_array=DataCL.data_array
    
    #needed variables
    Plot_PLT=Master.Plot
    cb_PLT=Master.cb
    canvas_PLT=Master.canvas
    
    #clear plot
    Plot_PLT.clear()
    
    #check if setting toggle is on. If so, make plot in a specific way
    #print(Master.SettingToggle.get())
    if Master.SettingToggle.get():
        #create plot
        #axes=Plot_PLT.imshow(data_array,norm=colors.LogNorm(),vmax=Master.IMax.get(),cmap='viridis')
        axes=Plot_PLT.imshow(data_array,vmax=Master.IMax.get(),cmap='viridis')
        Plot_PLT.axis([Master.xMin.get(),Master.xMax.get(),Master.yMin.get(),Master.yMax.get()])
    
        Plot_PLT.tick_params(axis="y",direction="in",color='white',left=True,right=True)
        Plot_PLT.tick_params(axis="x",direction="in",color='white',top=True,bottom=True)
        cb_PLT.mappable.set_clim(vmin=np.min(data_array),vmax=Master.IMax.get())
        cb_PLT.draw_all()
        canvas_PLT.draw()
        
    else:
        #create plot
        axes=Plot_PLT.imshow(data_array,norm=colors.LogNorm(),cmap='viridis')
        
        Plot_PLT.tick_params(axis="y",direction="in",color='white',left=True,right=True)
        Plot_PLT.tick_params(axis="x",direction="in",color='white',top=True,bottom=True)
        cb_PLT.mappable.set_clim(vmin=np.min(data_array),vmax=np.max(data_array))
        cb_PLT.draw_all()
        canvas_PLT.draw()
    
def Button_PlotMulti(Master):
    #grab how many meshes needed
    dataNum=len(Master.FileVar_ref)
    im=[]
    
    #generate plot
    
    #calculate appropriate fig size if Toggle On
    if Master.SettingToggle.get():
        xsize=np.absolute(Master.xMax.get()-Master.xMin.get())
        ysize=np.absolute(Master.yMax.get()-Master.yMin.get())
        
        xOvery=xsize/ysize
        
        # #fix y size size at 6. calculate xsize based on ratio
        # fig_height=12
        # fig_width=int(fig_height*xOvery)
        
        fig_height=12
        fig_width=12
    else:
        fig_width=12
        fig_height=12
        
        
    fig,axs=plt.subplots(dataNum,1,figsize=(fig_width,fig_height),sharex=True,sharey=True)
    
    #update each plot with data
    for j in range(dataNum):
        data=Load_Array(Master.FileVar_ref[j].get())
        if Master.SettingToggle.get():
            im.append(Add_MultiPlot_ToggleOn(axs, data, 
                                              Master.xMin.get(),
                                              Master.xMax.get(),
                                              Master.yMin.get(),
                                              Master.yMax.get(),
                                              Master.IMax.get(),
                                              Master.I_MultiplyVar_ref[j].get(),
                                              Master.PlotLabelVar_ref[j].get(),
                                              j))
        else:
            im.append(Add_MultiPlot_ToggleOff(axs, data, j))
            
        axs=axs.ravel()
        
            
            
    cb=fig.colorbar(im[0],ax=axs.tolist(),location='right',pad=-0.5)
    fig.tight_layout()
    #cb.ax.locator_params(nbins=3)
    #fig.supxlabel('pixel x')
    #fig.supylabel('pixel y')
        
    

def Add_MultiPlot_ToggleOn(axes,data,xmin,xmax,ymin,ymax,IMax,I_Multiply,PlotLabel,SubPlotNum):
    
    
    
    #im=axes[SubPlotNum].imshow(data,norm=colors.LogNorm(),vmax=IMax,cmap='viridis')
    im=axes[SubPlotNum].imshow(data*float(I_Multiply),norm=colors.LogNorm(vmax=IMax),cmap='viridis')
    axes[SubPlotNum].axis([xmin,xmax,ymin,ymax])
    axes[SubPlotNum].tick_params(axis="y",direction="in",color='white')
    axes[SubPlotNum].tick_params(axis="x",direction="in",color='white')
    
    #calc aspect ratio
    aspectR=np.absolute((xmax-xmin)/(ymax-ymin))
    print(aspectR)
    # aspectR=np.ceil(aspectR)
    # print(aspectR)
    axes[SubPlotNum].set_aspect(aspectR)
    
    #put in PlotLabelVar
    #place in top right corner (10% off from maxn in each x and y)
    
    x_text=int(np.absolute(xmax-xmin)*0.85+xmin)
    y_text=int(np.absolute(ymax-ymin)*0.85+ymin)
    
    
    
    t=axes[SubPlotNum].text(x_text,y_text,PlotLabel,color='black',size=10)
    t.set_bbox(dict(facecolor='red', alpha=0.5, edgecolor='red'))
    
    
    return im

def Add_MultiPlot_ToggleOff(axes,data,SubPlotNum):
    
    
    im=axes[SubPlotNum].imshow(data,norm=colors.LogNorm(),cmap='viridis')
    axes[SubPlotNum].tick_params(axis="y",direction="in",color='white')
    axes[SubPlotNum].tick_params(axis="x",direction="in",color='white')
    
    return im
    
    
def Button_NextFile(MasterTK,DataCL,direction):
   
    #objects needed:
    DataLocTK=MasterTK.DataLoc
    DataDisplayTK=MasterTK.DataDisplay
    XRD_ImageTK=MasterTK.XRD_Image
    Plot_PLT=MasterTK.Plot
    Fig_PLT=MasterTK.Fig
    canvas_PLT=MasterTK.canvas
    cb_PLT=MasterTK.cb
    
   #get next image name
    new_filename=Next_Image(DataLocTK.get(),direction)
    
    #update display and location
    DataDisplayTK.set(new_filename[-40:])
    DataLocTK.set(new_filename)
    
    #check file exists?? to do
    
    #update image on screen
    Button_QuickShowImage(MasterTK,XRD_ImageTK,DataCL)
    Button_ShowPlot(MasterTK,DataCL)
    

def Load_Image(filename):
    #open image at file location
    im=Image.open(filename)
    
    #resize image
    im=im.resize((521,491))
    
    #prepare for tkinter
    imPic=ImageTk.PhotoImage(im)
    
    return imPic

def Next_Image(filename,direction):
    #find number of current image
    number_str=filename[-7:-4]
    
    #create new image number and name for next image
    if direction=='Forward':
        number_int=int(number_str)
        new_number_int=number_int+1
        
    if direction=='Back':
        number_int=int(number_str)
        new_number_int=number_int-1
    
    if new_number_int<10:
        new_number_str='00'+str(new_number_int)
    if 10<=new_number_int<100:
        new_number_str='0'+str(new_number_int)
    if new_number_int>=100:
        new_number_str=str(new_number_int)
        
    #name for next image
    new_filename=filename[0:-7]+new_number_str+'.tif'
    
    return new_filename
    
    
    

def EmptyImage():
    #zeros for image size expected
    emptyArray=np.zeros((1043, 981))
    
    #convert array to image and return
    emptyIm=Image.fromarray(emptyArray)
    
    #resize image smaller for screen
    emptyIm=emptyIm.resize((521,491))
    
    #prepare image for tkinter
    emptyImPic=ImageTk.PhotoImage(emptyIm)
    #emptyIm.show()
    return emptyImPic

def Load_DF(filename):
    #open image at file location
    im=Image.open(filename)
    
    #convert image to pd dataframe
    imageDF=Image_to_DF(im)
    
    return imageDF

def Load_Array(filename):
    #open image at file location
    im=Image.open(filename)
    
    #convert image to pd dataframe
    imageArray=Image_to_Array(im)
    
    return imageArray

def Empty_Plot(MasterTK):
    #creates a blank plot for use on a screen for a given Master
    #generate figure 
    fig=Figure()
    
    ax=fig.add_subplot()
    empty=ax.imshow(np.zeros((5,5)))
    cb=fig.colorbar(empty)
    canvas=FigureCanvasTkAgg(fig,master=MasterTK)
    canvas.draw()
    
    toolbarFrame = tk.Frame(MasterTK)
    
    
    return canvas,fig,ax,toolbarFrame,cb

def Image_to_DF(im):
    #convert to array
    imarray=np.array(im)
    #grab shape needed for loop
    imshape=imarray.shape
    
    #step through each point (x,y) and save x,y,intensity
    x=np.zeros(imshape[0]*imshape[1])
    y=np.zeros(imshape[0]*imshape[1])
    I=np.zeros(imshape[0]*imshape[1])
    
    index=0
    
    for i in range(imshape[1]-1):
        for j in range(imshape[0]-1):
            #print([i,j])
            I_current=im.getpixel((i,j))
            
            x[index]=i
            y[index]=j
            I[index]=I_current
            
            index+=1
            
    
    #save result as dataframe
    imData={'x':x,
            'y':y,
            'Intensity':I}
    
    imDF=pd.DataFrame(imData)
    print(imDF['Intensity'].max())
    print(imDF['x'].max())
    print(imDF['y'].max())
    
    return imDF

def Image_to_Array(im):
     #convert to array
    imarray=np.array(im)
    
    return imarray

def SwitchButton(ButtonTK,ToggleTK):
    
    #give on and off button images
    On=Image.open('on.png')
    OnPic=ImageTk.PhotoImage(On)
    
    Off=Image.open('off.png')
    OffPic=ImageTk.PhotoImage(Off)
    
    #switch toggle depending on current state
    toggle=ToggleTK.get()
    
    if toggle:
        ButtonTK.config(image=OffPic,fg='grey')
        ButtonTK.image=OffPic
        ToggleTK.set(False)
    else:
        ButtonTK.config(image=OnPic,fg='green')
        ButtonTK.image=OnPic
        ToggleTK.set(True)
        


            
            
    
    