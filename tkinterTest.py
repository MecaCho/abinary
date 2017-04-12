#-*-coding=UTF-8-*-
import Tkinter
from Tkinter import *

top = Tkinter.Tk()
top.title('Python Title')
top.geometry('400x300')
top.resizable(width=True,height=True)

aLabel = Tkinter.Label(top,text='This is a Label')
aLabel.grid(column = 0,row = 0)

action = Tkinter.Button(top,text='Click')
action.grid(column = 1,row = 1)


# Code to add widgets will go here...
top.mainloop()