#!/usr/bin/python
from Tkinter import *
from tkFileDialog import askopenfilename
from PIL import Image, ImageTk                   #sudo apt-get install python-imaging-tk
from expand_ptex import init as compile_me
from help_me import help_me
#import tkFileDialog
"""
    *TODO: add check box for optional make title
    *TODO: move from .pack() to .grid()
    *TODO: zoom buttons for viewer frame
    *TODO: file open concatenates the new file to the end of the old file in the editor
    *TODO: implement file save
    *TODO: redirect compile to buffer window
    *TODO: split buffer frame into buffer 75% left help 25% right
"""


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
        self.input_f = ''
        button = Button(self.parent, text="Compile", command=self.main)
        button.pack(side=BOTTOM)
        button = Button(self.parent, text="Help", command=self.main_help)
        button.pack(side=BOTTOM)

    def main(self):
        print compile_me(self.input_f)

    def main_help(self):
        print help_me()

    def InitUI(self):
        self.text_box = Text(self.parent, bd=5)
        self.text_box.pack(side=BOTTOM, fill=BOTH, expand=YES)
        sys.stdout = StdoutRedirector(self.text_box)


def callback():
    name = askopenfilename()
    gui.input_f = name
    with open(name, 'r') as x:
        content = x.read()
    L1.insert(INSERT, content)

"""
def file_save():
    f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".txt")
    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    text2save = str(text.get(1.0, END)) # starts from `1.0`, not `0.0`
    f.write(text2save)
    f.close() # `()` was missing.
"""

root = Tk()
menu = Menu(root)
gui = Redirector(root)
root.config(menu=menu)
fileMenu = Menu(menu)
menu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Open", command=callback)
#fileMenu.add_command(label="Save", command=file_save)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=root.quit)


'''left window for text entry'''
L1 = Text(root, bd=5)
L1.pack(side=LEFT, fill=BOTH, expand=YES)

'''right window for jpeg (just test file right now)'''
''' TODO : create buttons for zooming in and out '''
img1 = Image.open("test.jpg")
img1 = img1.resize((500, 800), Image.ANTIALIAS)
img = ImageTk.PhotoImage(img1)
panel = Label(root, image=img)
panel.pack(side=RIGHT, fill=BOTH, expand=YES)

'''open window'''
root.mainloop()




