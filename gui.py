#!/usr/bin/python
from Tkinter import *
from tkFileDialog import askopenfilename
from PIL import Image, ImageTk  #sudo apt-get install python-imaging-tk
from expand_ptex import init as compile_me
from help_me import help_me
import ttk
import tkFileDialog
from img_proc import *
import os



"""
    *TODO: add check box for optional make title
    *TODO: move from .pack() to .grid()
    *TODO: zoom buttons for viewer frame
    *TODO: implement file save
    *TODO: redirect compile to buffer window
    *TODO: split buffer frame into buffer 75% left help 25% right
    *TODO: add 'spell check' button that runs aspell in buffer frame
"""
# s = ttk.Style()
# s.theme_use('alt')

"""
class StatusBar(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.variable = StringVar()
        self.label = Label(self, bd=1, relief=SUNKEN, anchor=W, textvariable=self.variable, font=('arial', 16, 'normal'))
        self.variable.set('Status Bar')
        self.label.grid(row=6)
        self.grid(row=6, column=0, sticky=S)
"""


class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, string):
        self.text_space.insert('end', string)
        self.text_space.see('end')


class Redirector(object):
    def __init__(self, parent):
        global twoT
        twoT = 0
        self.parent = parent
        self.text_box = Text(self.parent, bd=5)
        self.text_box.grid(row=9, column=0, rowspan=1, columnspan=6, sticky=W + E + N + S)
        self.text_box2 = Text(self.parent, bd=5)
        self.text_box2.grid(row=9, column=6, rowspan=1, columnspan=4, sticky=W + E + N + S)
        self.text_box2.insert(END, help_me())
        sys.stdout = StdoutRedirector(self.text_box)
        self.input_f = ''
        self.x = 1600
        self.y = 2000
        self.zlevel = 0 #Zoom level [-5,5]
        button = Button(self.parent, text="Compile", command=self.comp)
        button.grid(row=8,column=0,sticky=E+W)
        button = Button(self.parent, text="Terminal", command=self.term)
        button.grid(row=8,column=1,sticky=E+W)
        button = Button(self.parent, text="+", command=self.zoom_in)
        button.grid(row=8, column=4, sticky=E+W)
        button = Button(self.parent, text="-", command=self.zoom_out)
        button.grid(row=8, column=3, sticky=E+W)
        self.canvas = Canvas(self.parent, width=50, height=80, scrollregion=(0, 0, self.x, self.y))
        self.canvas.grid(row=0, column=3, rowspan=8, columnspan=7, sticky=W + E + N + S)
        #self.canvas.config(scrollregion=self.canvas.bbox(ALL))
        self.scale = 1.0
        self.orig_img = None
        self.img = None
        self.zoomcycle = 0
        self.zimg_id = None
        self.hbar = Scrollbar(self.canvas, orient=HORIZONTAL)
        self.hbar.grid(sticky=E+W, row=7, column=5)
        self.hbar.config(command=self.canvas.xview)
        self.vbar = Scrollbar(self.canvas, orient=VERTICAL)
        self.vbar.grid(sticky=S+N, row = 5, column = 9)
        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(width=50, height=80)
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        b1 = Button(root, text=str("<"), command=self.show_image1)
        b1.grid(row=8, column=6, sticky=E + W)
        b2 = Button(root, text=">", command=self.show_image2)
        b2.grid(row=8, column=7, sticky=E + W)
        self.canvas.bind("<ButtonPress-1>", self.scroll_start)
        self.canvas.bind("<B1-Motion>", self.scroll_move)
        self.canvas.bind("<Control-Button-4>", self.wheel_zoom)
        self.canvas.bind("<Control-Button-5>", self.wheel_zoom)
        

    def scroll_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def comp(self, *args):
        self.text_box = Text(self.parent, bd=5)
        self.text_box.grid(row=9, column=0, rowspan=1, columnspan=6, sticky=W + E + N + S)
        sys.stdout = StdoutRedirector(self.text_box)
        if twoT == 0:
            file_save2()
        print compile_me(self.input_f, StdoutRedirector(self.text_box))
        reverse = self.input_f[::-1]
        a = reverse.index('/')
        reverse = reverse[:a]
        reverse = reverse[::-1]
        clear_jpegs()
        pdf2jpg(reverse[:-3]+"pdf")
        global img_list
        img_list = []
        resize(self.x,self.y)
        img_list = get_jpegs()
        self.canvas.delete("all")
        self.orig_img = img_list[counter]
        self.img = ImageTk.PhotoImage(self.orig_img)
        self.canvas.create_image(0, 0, image=self.img, anchor="nw")
        self.hbar = Scrollbar(self.canvas, orient=HORIZONTAL)
        self.hbar.grid(sticky=E+W, row=7, column=5)
        self.hbar.config(command=self.canvas.xview)
        self.vbar = Scrollbar(self.canvas, orient=VERTICAL)
        self.vbar.grid(sticky=S+N, row=5, column=9)
        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(width=50, height=80)
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        #self.canvas.image = self.img

    def main_help(self):
        print help_me()

    def zoom_in(self, *args):
        #self.x = int(self.x * 1.2)
        #self.y = int(self.y * 1.2)
        #resize(self.x, self.y)
        if self.zlevel < 9: #Zoom in
            self.zlevel += 1
        zoom(self.zlevel, self.x, self.y)
        global img_list
        img_list = []
        img_list = get_jpegs()
        self.canvas.configure(scrollregion=(0, 0, self.x, self.y))
        self.canvas.delete("all")
        self.orig_img = img_list[counter]
        self.img = ImageTk.PhotoImage(self.orig_img)
        self.canvas.create_image(0, 0, image=self.img, anchor="nw")
        self.hbar = Scrollbar(self.canvas, orient=HORIZONTAL)
        self.hbar.grid(sticky=E + W, row=7, column=5)
        self.hbar.config(command=self.canvas.xview)
        self.vbar = Scrollbar(self.canvas, orient=VERTICAL)
        self.vbar.grid(sticky=S + N, row=5, column=9)
        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(width=50, height=80)
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)

    def zoom_out(self, *args):
        #self.x = int(self.x * 0.8)
        #self.y = int(self.y * 0.8)
        #resize(self.x, self.y)
        if self.zlevel > -9: #Zoom in
            self.zlevel -= 1
        zoom(self.zlevel, self.x, self.y)
        global img_list
        img_list = []
        img_list = get_jpegs()
        self.canvas.configure(scrollregion=(0, 0, self.x, self.y))
        self.canvas.delete("all")
        self.orig_img = img_list[counter]
        self.img = ImageTk.PhotoImage(self.orig_img)
        self.canvas.create_image(0, 0, image=self.img, anchor="nw")
        self.hbar = Scrollbar(self.canvas, orient=HORIZONTAL)
        self.hbar.grid(sticky=E+W, row=7, column=5)
        self.hbar.config(command=self.canvas.xview)
        self.vbar = Scrollbar(self.canvas, orient=VERTICAL)
        self.vbar.grid(sticky=S + N, row=5, column=9)
        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(width=50, height=80)
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)

    def wheel_zoom(self, event):
        if event.num == 4 and self.zlevel < 9: #Zoom in
            self.zlevel += 1
        elif event.num == 5 and self.zlevel > -9: #Zoom out
            self.zlevel -= 1
        zoom(self.zlevel, self.x, self.y)
        global img_list
        img_list = []
        img_list = get_jpegs()
        self.canvas.configure(scrollregion=(0, 0, self.x, self.y))
        self.canvas.delete("all")
        self.orig_img = img_list[counter]
        self.img = ImageTk.PhotoImage(self.orig_img)
        self.canvas.create_image(0, 0, image=self.img, anchor="nw")
        self.hbar = Scrollbar(self.canvas, orient=HORIZONTAL)
        self.hbar.grid(sticky=E + W, row=7, column=5)
        self.hbar.config(command=self.canvas.xview)
        self.vbar = Scrollbar(self.canvas, orient=VERTICAL)
        self.vbar.grid(sticky=S + N, row=5, column=9)
        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(width=50, height=80)
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)


    def InitUI(self):
        self.text_box = Text(self.parent, bd=5)
        self.text_box.grid(row=9, column=0, rowspan=1, columnspan=6, sticky=W+E+N+S)
        self.text_box2 = Text(self.parent, bd=5)
        self.text_box2.grid(row=9, column=6, rowspan=1, columnspan=4, sticky=W+E+N+S)
        self.text_box2.insert(END, help_me())
        sys.stdout = StdoutRedirector(self.text_box)

    def term(self, *args):
        self.text_box = Frame(self.parent, height=20, width=40)
        self.text_box.grid(row=9, column=0, rowspan=1, columnspan=6, sticky=W+E+N+S)
        wid = self.text_box.winfo_id()
        os.system('xterm -into %d -geometry 400x500 -sb &' % wid)

    def show_image1(self):
        """ > button """
        self.canvas.delete("all")
        global counter
        if counter == len(img_list) - 1:
            counter = 0
        else:
            counter -= 1
        image1 = ImageTk.PhotoImage(img_list[counter])
        self.canvas.create_image(0,0, anchor='nw', image=image1)
        self.canvas.image = image1

    def show_image2(self):
        """ < button """
        self.canvas.delete("all")
        global counter
        if counter == 0:
            counter = len(img_list) - 1
        else:
            counter -= 1
        #image2 = ImageTk.PhotoImage(img_list[counter].resize((800, 1100), Image.NEAREST))
        image2 = ImageTk.PhotoImage(img_list[counter])
        self.canvas.create_image(0,0, anchor='nw', image=image2)
        self.canvas.image = image2


def callback(*args):
    name = askopenfilename()
    gui.input_f = name
    L1.delete('1.0', END)
    with open(name, 'r') as x:
        content = x.read()
    L1.insert(INSERT, content)


def open_exp(*args):
    name = 'micro_exp.py'
    gui.input_f = name
    L1.delete('1.0', END)
    with open(name, 'r') as x:
        content = x.read()
    L1.insert(INSERT, content)


def file_save(*args):
    f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".txt")
    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    text2save = str(L1.get(1.0, END)) # starts from `1.0`, not `0.0`
    f.write(text2save)
    f.close() # `()` was missing.


def file_save2(*args):
    f = open(gui.input_f, 'w')
    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    text2save = str(L1.get(1.0, END)) # starts from `1.0`, not `0.0`
    f.write(text2save)
    f.close() # `()` was missing.


def two_terms(*args):
    global twoT
    twoT = 1
    t_box = Frame(root, height=60, width=40)
    t_box.grid(row=0, column=0, rowspan=8, columnspan=3, sticky=W+E+N+S)
    wid = t_box.winfo_id()
    os.system('xterm -into %d -geometry 400x500 -sb &' % wid)

counter = 0

root = Tk()
root.title("pyTex")
root.grid()
menu = Menu(root)
#d = StatusBar(root)
gui = Redirector(root)
root.config(menu=menu)
fileMenu = Menu(menu)
editMenu = Menu(menu)

for r in range(10):
    root.rowconfigure(r, weight=1)
for c in range(10):
    root.columnconfigure(c, weight=1)

menu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Open", command=callback, accelerator="Ctrl+o")
fileMenu.add_command(label="Save", command=file_save2)
fileMenu.add_command(label="Save as", command=file_save, accelerator="Ctrl+s")
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=root.quit)
menu.add_cascade(label="Edit", menu=editMenu)
editMenu.add_command(label="Micro-Exps", command=open_exp)
editMenu.add_command(label="2-terms", command=two_terms, accelerator="Ctrl+r")
root.bind_all("<Control-o>", callback)
root.bind_all("<Control-c>", gui.comp)
root.bind_all("<Control-t>", gui.term)
root.bind_all("<Control-s>", file_save)
root.bind_all("<Control-r>", two_terms)
global img_list

'''left window for text entry'''
L1 = Text(root, bd=5)
L1.grid(row=0, column=0, rowspan=8, columnspan=3, sticky=W+E+N+S)

'''open window'''
root.mainloop()





