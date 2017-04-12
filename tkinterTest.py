#-*-coding=UTF-8-*-
import Tkinter
from Tkinter import *

top = Tk()
top.title('Python Title')
top.geometry('400x300')
top.resizable(width=True,height=True)

aLabel = Tkinter.Label(top,text='This is a Label')
aLabel.grid(column = 0,row = 0)

action = Tkinter.Button(top,text='Click')
action.grid(column = 1,row = 1)

label1 = Label(top,text='hello world!!!!!!',justify=RIGHT,padx=10)
#label1.pack(side=BOTTOM)
label1.grid()

imageFilepath = PhotoImage(file="1.gif")
imgLabel = Label(top,image=imageFilepath)
#imgLabel.pack(side=RIGHT)
imgLabel.grid()


# Code to add widgets will go here...
top.mainloop()