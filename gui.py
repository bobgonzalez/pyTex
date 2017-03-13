#!/usr/bin/python
import sys
from Tkinter import *
import os
from tkFileDialog import askopenfilename
from PIL import Image, ImageTk                   #sudo apt-get install python-imaging-tk


class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, string):
        self.text_space.insert('end', string)
        self.text_space.see('end')

class Redirector(object):
    def __init__(self, parent):
        self.parent = parent
        self.InitUI()
        button = Button(self.parent, text="Refresh", command=self.main)
        button.pack(side=BOTTOM)

    def main(self):
        st = os.popen("ls").read()
        print st

    def InitUI(self):
        self.text_box = Text(self.parent, bd=5)
        self.text_box.pack(side=BOTTOM, fill=BOTH, expand=YES)
        sys.stdout = StdoutRedirector(self.text_box)


def callback():
    name = askopenfilename()
    with open(name, 'r') as x:
        content = x.read()
    L1.insert(INSERT, content)


root = Tk()
menu = Menu(root)
gui = Redirector(root)
root.config(menu=menu)
fileMenu = Menu(menu)
menu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Open", command=callback)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=root.quit)


'''left window for text entry'''
L1 = Text(root, bd=5)
L1.pack(side=LEFT, fill=BOTH, expand=YES)

'''right window for jpeg (just test file right now)'''
img = ImageTk.PhotoImage(Image.open("/home/ub/Pictures/test"))
panel = Label(root, image=img)
panel.pack(side=RIGHT, fill=BOTH, expand=YES)

'''open window'''
root.mainloop()




