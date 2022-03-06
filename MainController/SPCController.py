from calendar import month
from doctest import master
from multiprocessing.sharedctypes import Value
from scipy.stats import norm
from turtle import bgcolor, color, left, width
from  datetime import date
from tkinter import ttk
import mysql.connector
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.image as mpimg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
from numpy import arange, sin, pi


#meta data variable
metaData = []

list = Listbox



def getGraphData(queryToexecute):
    #graph variables
    TCWL =[]
    TCWR=[]
    BCWL=[]
    BCWR=[]
    TotalThickness=[]
    TotalWidth=[]
    totalParams=[]
    cnx = mysql.connector.connect(user='root', password='jagapathi',
                              host='192.168.1.3',
                              port='3306',
                              database='lmwind')
    cur=cnx.cursor()
    print(queryToexecute)
    cur.execute(queryToexecute)
    for i in cur:
        TCWL.append(float(i[0]))
        TCWR.append(float(i[1]))
        BCWL.append(float(i[2]))
        BCWR.append(float(i[3]))
        TotalThickness.append(float(i[4]))
        TotalWidth.append(float(i[5]))
    totalParams.append(TCWL)
    totalParams.append(TCWR)
    totalParams.append(BCWL)
    totalParams.append(BCWR)
    totalParams.append(TotalThickness)
    totalParams.append(TotalWidth)
    return totalParams

def getMetaData(nonEmptyData):
    
    cnx = mysql.connector.connect(user='root', password='jagapathi',
                              host='192.168.1.3',
                              port='3306',
                              database='lmwind')
    cur=cnx.cursor()
    query = "SELECT ID,Mode, BladeType, BladeID, CoilID,BatchNumber,Operator,Date FROM `metadata` where "

    for fields in nonEmptyData:
        query += fields[0] + "='"+ fields[1] +"' and "

    finalquery = query[:-4]
    cur.execute(finalquery)
    for i in cur:
        metaData.append(i)
    if(len(metaData)>0):
        return metaData
    else:
        messagebox.showwarning("No data", "No data available for seleted option")


def graphView(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    currentData=metaData[index]
    plankPrefix = "00000"
    plankId = plankPrefix[:-len(str(currentData[0]))] + str(currentData[0])
    queryToExecute = "select TCWL,TCWR,BCWL,BCWR,TotalThickness,FinalTotalWidth from plank_"+plankId
    totalParams =getGraphData(queryToExecute)
    for widget in ctr_right.winfo_children():
        widget.destroy()

    scrollable_frame = ScrolledText(ctr_right,height=int(screen_height-55))
    scrollable_frame.pack(fill=BOTH)

    #---------------------------------------------
    Figure(figsize = (7,7),dpi = 100)
    y = totalParams[0]
    mu, std = norm.fit(y)
    fig = plt.figure(figsize=(9.5,6.5))
    plt.title('Top Champher Left', fontdict={'fontsize':20})
    plt.xlabel('TCWL', fontsize=18)
    plt.ylabel('Frequency', fontsize=16)
    plt.yticks([])
    plt.hist(y, bins=5, density=True, alpha=0)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    canvas = FigureCanvasTkAgg(fig, master=ctr_right)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=X, expand=1,anchor='ne')
    scrollable_frame.window_create(END, window=canvas.get_tk_widget())
    scrollable_frame.insert(END, '\n')

    #---------------------------------------------
    Figure(figsize = (7,7),dpi = 100)
    y = totalParams[1]
    mu, std = norm.fit(y)
    fig = plt.figure(figsize=(9.5,6.5))
    plt.title('Top Champher Right', fontdict={'fontsize':20})
    plt.xlabel('TCWR', fontsize=18)
    plt.ylabel('Frequency', fontsize=16)
    plt.yticks([])
    plt.hist(y, bins=5, density=True, alpha=0)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    canvas = FigureCanvasTkAgg(fig, master=ctr_right)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=X, expand=1)
    scrollable_frame.window_create(END, window=canvas.get_tk_widget())
    scrollable_frame.insert(END, '\n')
    #---------------------------------------------
    Figure(figsize = (7,7),dpi = 100)
    y = totalParams[2]
    mu, std = norm.fit(y)
    fig = plt.figure(figsize=(9.5,6.5))
    plt.title('Bottom champher Left', fontdict={'fontsize':20})
    plt.xlabel('BCWL', fontsize=18)
    plt.ylabel('Frequency', fontsize=16)
    plt.yticks([])
    plt.hist(y, bins=5, density=True, alpha=0)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    canvas = FigureCanvasTkAgg(fig, master=ctr_right)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=X, expand=1)
    scrollable_frame.window_create(END, window=canvas.get_tk_widget())
    scrollable_frame.insert(END, '\n')
    #---------------------------------------------
    Figure(figsize = (7,7),dpi = 100)
    y = totalParams[3]
    mu, std = norm.fit(y)
    fig = plt.figure(figsize=(9.5,6.5))
    plt.title('Bottom Champher Right', fontdict={'fontsize':20})
    plt.xlabel('BCWR', fontsize=18)
    plt.ylabel('Frequency', fontsize=16)
    plt.yticks([])
    plt.hist(y, bins=5, density=True, alpha=0)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    canvas = FigureCanvasTkAgg(fig, master=ctr_right)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=X, expand=1)
    scrollable_frame.window_create(END, window=canvas.get_tk_widget())
    scrollable_frame.insert(END, '\n')
    #---------------------------------------------
    Figure(figsize = (7,7),dpi = 100)
    y = totalParams[4]
    mu, std = norm.fit(y)
    fig = plt.figure(figsize=(9.5,6.5))
    plt.title('Total Thickness', fontdict={'fontsize':20})
    plt.xlabel('Total Thickness', fontsize=18)
    plt.ylabel('Frequency', fontsize=16)
    plt.yticks([])
    plt.hist(y, bins=5, density=True, alpha=0)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    canvas = FigureCanvasTkAgg(fig, master=ctr_right)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=X, expand=1)
    scrollable_frame.window_create(END, window=canvas.get_tk_widget())
    scrollable_frame.insert(END, '\n')
    #---------------------------------------------
    Figure(figsize = (7,7),dpi = 100)
    y = totalParams[5]
    mu, std = norm.fit(y)
    fig = plt.figure(figsize=(9.5,6.5))
    plt.title('Total Width', fontdict={'fontsize':20})
    plt.xlabel('Total Width', fontsize=18)
    plt.ylabel('Frequency', fontsize=16)
    plt.yticks([])
    plt.hist(y, bins=5, density=True, alpha=0)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    canvas = FigureCanvasTkAgg(fig, master=ctr_right)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=X, expand=1)
    scrollable_frame.window_create(END, window=canvas.get_tk_widget())
    scrollable_frame.insert(END, '\n')
    
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        

root.protocol("WM_DELETE_WINDOW", on_closing)


root.mainloop()
