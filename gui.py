#!/usr/bin/python
from Tkinter import *
from tkFileDialog import askopenfilename
from PIL import Image, ImageTk  #sudo apt-get install python-imaging-tk
from expand_ptex import init as compile_me
from help_me import help_me
#import ttk
import tkFileDialog
from img_proc import *
import os
import distutils.dir_util


"""
    *TODO: add pop up window asking for title and author when make_title is selected
    *TODO: add ability for user to change their default zlevel
"""

TITLE = False
twoT = 0


class StatusBar(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.variable = StringVar()
        self.label = Label(self, bd=1, relief=SUNKEN, anchor=W, textvariable=self.variable, font=('arial', 10, 'normal'))
        self.variable.set('Status Bar')
        self.label.grid(row=20, column=0, columnspan=10, sticky=W+E)
        self.grid(row=20, column=0, columnspan=10, sticky=W+E)


class Redirector(object):
    def __init__(self, parent):
        self.parent = parent
        self.status = StatusBar(parent)
        self.input_f = ''
        self.x = 1600
        self.y = 2000
        self.img_list = []
        self.counter = 0
        self.zlevel = 0 #Zoom level [-5,5]
        self.default_status()
        button = Button(self.parent, text="Compile", command=self.comp)
        button.grid(row=19, column=0, sticky=E+W)
        button = Button(self.parent, text="Help", command=self.help)
        button.grid(row=19, column=1, sticky=E+W)
        button = Button(self.parent, text="+", command=self.zoom_in)
        button.grid(row=19, column=4, sticky=E+W)
        button = Button(self.parent, text="-", command=self.zoom_out)
        button.grid(row=19, column=3, sticky=E+W)
        self.canvas = Canvas(self.parent, width=50, height=80, scrollregion=(0, 0, self.x, self.y))
        self.canvas.grid(row=0, column=3, rowspan=19, columnspan=7, sticky=W+E+N+S)
        #self.canvas.config(scrollregion=self.canvas.bbox(ALL))
        self.orig_img = None
        self.img = None
        b1 = Button(root, text=str(">"), command=self.show_image1)
        b1.grid(row=19, column=7, sticky=E+W)
        b2 = Button(root, text="<", command=self.show_image2)
        b2.grid(row=19, column=6, sticky=E+W)
        self.canvas.bind("<ButtonPress-1>", self.scroll_start)
        self.canvas.bind("<B1-Motion>", self.scroll_move)
        self.canvas.bind("<Control-Button-4>", self.wheel_zoom)
        self.canvas.bind("<Control-Button-5>", self.wheel_zoom)

    def scroll_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def comp(self, *args):
        distutils.dir_util.mkpath('./Original')
        distutils.dir_util.mkpath('./Zoom')
        if twoT == 1:
            file_save()
        if TITLE:
            print compile_me(self.input_f, 1, "Title", "Author")
        else:
            print compile_me(self.input_f)
        reverse = self.input_f[::-1]
        a = reverse.index('/')
        reverse = reverse[:a]
        reverse = reverse[::-1]
        clear_jpegs()
        pdf2jpg(reverse[:-4]+"1.pdf")
        self.img_list = []
        resize(self.x, self.y)
        self.img_list = get_jpegs()
        self.canvas.delete("all")
        self.orig_img = self.img_list[self.counter]
        self.img = ImageTk.PhotoImage(self.orig_img)
        self.canvas.create_image(0, 0, image=self.img, anchor="nw")
        self.status.variable.set('Compiled ' + self.input_f)

    def main_help(self):
        print help_me()

    def zoom_in(self, *args):
        if self.zlevel < 9: #Zoom in
            self.zlevel += 1
        self.x, self.y = zoom(self.zlevel)
        self.img_list = []
        self.img_list = get_jpegs()
        self.canvas.configure(scrollregion=(0, 0, self.x, self.y))
        self.canvas.delete("all")
        self.orig_img = self.img_list[self.counter]
        self.img = ImageTk.PhotoImage(self.orig_img)
        self.canvas.create_image(0, 0, image=self.img, anchor="nw")
        self.default_status()
    def zoom_out(self, *args):
        if self.zlevel > -9: #Zoom in
            self.zlevel -= 1
        self.x, self.y = zoom(self.zlevel)
        self.img_list = []
        self.img_list = get_jpegs()
        self.canvas.configure(scrollregion=(0, 0, self.x, self.y))
        self.canvas.delete("all")
        self.orig_img = self.img_list[self.counter]
        self.img = ImageTk.PhotoImage(self.orig_img)
        self.canvas.create_image(0, 0, image=self.img, anchor="nw")
        self.default_status()
    def wheel_zoom(self, event):
        if event.num == 4 and self.zlevel < 9: #Zoom in
            self.zlevel += 1
        elif event.num == 5 and self.zlevel > -9: #Zoom out
            self.zlevel -= 1
        self.x, self.y = zoom(self.zlevel)
        self.img_list = []
        self.img_list = get_jpegs()
        self.canvas.configure(scrollregion=(0, 0, self.x, self.y))
        self.canvas.delete("all")
        self.orig_img = self.img_list[self.counter]
        self.img = ImageTk.PhotoImage(self.orig_img)
        self.canvas.create_image(0, 0, image=self.img, anchor="nw")
        self.default_status()

    def help(self, *args):
        x = "this is a place holder"

    def show_image1(self, *args):
        """ > button """
        if self.counter == len(self.img_list) - 1:
            self.counter = 0
        else:
            self.counter += 1
        self.canvas.configure(scrollregion=(0, 0, self.x, self.y))
        self.canvas.delete("all")
        self.orig_img = self.img_list[self.counter]
        self.img = ImageTk.PhotoImage(self.orig_img)
        self.canvas.create_image(0, 0, image=self.img, anchor="nw")
        self.default_status()

    def show_image2(self, *args):
        """ < button """
        if self.counter == 0:
            self.counter = len(self.img_list) - 1
        else:
            self.counter -= 1
        self.canvas.configure(scrollregion=(0, 0, self.x, self.y))
        self.canvas.delete("all")
        self.orig_img = self.img_list[self.counter]
        self.img = ImageTk.PhotoImage(self.orig_img)
        self.canvas.create_image(0, 0, image=self.img, anchor="nw")
        self.default_status()

    def default_status(self, *args):
        vstring = ('Current Zoom Level: ' + str(self.zlevel) +
                   ' \tCurrent Page: ' + str(self.counter + 1) +
                   ' \tMake Title: ' + str(TITLE))
        for arg in args:
            vstring += str(arg)
        self.status.variable.set(vstring)


def file_open(*args):
    name = askopenfilename()
    # gui.default_status("filename: " + name)
    if isinstance(name, str) and name != '':
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


def file_save_as(*args):
    f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".txt")
    if f is None:
        return
    text2save = str(L1.get(1.0, END)) # starts from `1.0`, not `0.0`
    f.write(text2save)
    f.close() # `()` was missing.


def file_save(*args):
    f = open(gui.input_f, 'w')
    if f is None:
        return
    text2save = str(L1.get(1.0, END)) # starts from `1.0`, not `0.0`
    f.write(text2save)
    f.close()


def two_terms(*args):
    global twoT
    global L1
    if twoT == 1:
        if gui.input_f != '':
            file_save2()
        t_box = Frame(root, height=60, width=40)
        t_box.grid(row=0, column=0, rowspan=19, columnspan=3, sticky=W+E+N+S)
        wid = t_box.winfo_id()
        os.system('xterm -into %d -geometry 400x500 -sb &' % wid)
        twoT = 0
    else:
        L1 = Text(root, bd=5)
        L1.grid(row=0, column=0, rowspan=19, columnspan=3, sticky=W + E + N + S)
        twoT = 1
        if gui.input_f != '':
            L1.delete('1.0', END)
            with open(gui.input_f, 'r') as x:
                content = x.read()
            L1.insert(INSERT, content)


def make_title(*args):
    global TITLE
    if TITLE:
        TITLE = False
    else:
        TITLE = True
    gui.default_status()


root = Tk()
root.title("pyTex")
root.grid()
menu = Menu(root)

gui = Redirector(root)
root.config(menu=menu)
fileMenu = Menu(menu)
editMenu = Menu(menu)

for r in range(11):
    root.rowconfigure(r, weight=1)
for c in range(10):
    root.columnconfigure(c, weight=1)

menu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Open", command=file_open, accelerator="Ctrl+o")
fileMenu.add_command(label="Save", command=file_save, accelerator="Ctrl+s")
fileMenu.add_command(label="Save as", command=file_save_as, accelerator="Alt+s")
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=root.quit)
menu.add_cascade(label="Edit", menu=editMenu)
editMenu.add_command(label="Micro-Exps", command=open_exp)
editMenu.add_command(label="Make Title", command=make_title, accelerator="Ctrl+t")
editMenu.add_command(label="Use Terminal", command=two_terms, accelerator="Ctrl+r")
root.bind_all("<Control-o>", file_open)
root.bind_all("<Control-c>", gui.comp)
root.bind_all("<Control-h>", gui.help)
root.bind_all("<Control-s>", file_save)
root.bind_all("<Alt-s>", file_save_as)
root.bind_all("<Control-r>", two_terms)
root.bind_all("<Control-t>", make_title)
root.bind_all("<Alt-h>", gui.show_image2)
root.bind_all("<Alt-l>", gui.show_image1)
root.bind_all("<Alt-k>", gui.zoom_in)
root.bind_all("<Alt-j>", gui.zoom_out)
root.bind_all("<Alt-Left>", gui.show_image2)
root.bind_all("<Alt-Right>", gui.show_image1)
root.bind_all("<Alt-Up>", gui.zoom_in)
root.bind_all("<Alt-Down>", gui.zoom_out)
L1 = Text(root, bd=5)
two_terms()

'''open window'''
root.mainloop()





