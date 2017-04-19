import time
import Tkinter

ls = ['1','2','3','4']
print ls
ls.pop()
print ls
def showHwnd():
    top = Tkinter.Tk()
    top.title('Python Title')
    top.geometry('400x300')
    top.resizable(width=True, height=True)

    aLabel = Tkinter.Label(top, text='This is a Label')
    aLabel.grid(column=0, row=0)

    action = Tkinter.Button(top, text='Click')
    action.grid(column=1, row=1)

    # Code to add widgets will go here...
    top.mainloop()

showHwnd()
top = Tkinter.Tk()
label1 = Tkinter.Label(top,text = 'helloworld')
label1.pack()
Tkinter.mainloop()