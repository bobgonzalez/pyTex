#!/usr/bin/python

'''
Project: pyTex
File: pdf2jpg.py
Description: Convert PDF files into JPEG images
'''

'''---------------------------IMPORTS---------------------------'''
# brew install imagemagick
# pip install wand
from wand.image import Image as wandImage
from wand.exceptions import *	
from os import listdir, remove
from PIL import Image as pilImage
'''---------------------------IMPORTS---------------------------'''


'''--------------------------FUNCTIONS--------------------------'''


def pdf2jpg(filepath):
    """
    Description: Convert a single/multi-page PDF document into JPEGs saved in the ./Original and ./Zoom directories.
    Parameters: 1
        filepath: String, Path to PDF document
    Return: 0
        -:-
    """
    try:
        with wandImage(filename=filepath, resolution=300) as img:
            img.compression_quality = 99
            img.save(filename="./Original/"+filepath[:-3]+"jpg")
            img.save(filename="./Zoom/"+filepath[:-3]+"jpg")
    except MissingDelegateError:
        print("\n\nFile entered is not a pdf file!\nOr imagemagick is not installed: brew install imagemagick\n\n")


def resize(x, y):
    """
    Description: Resize all JPEGs currently in the ./Original and ./Zoom directories.
    Parameters: 2
        x: INT, desired x dimension
        y: INT, desired y dimension
    Return: 0
        -:-
    """
    try:
        for file in listdir("./Original"):
            img = wandImage(filename="./Original/"+file, resolution=300)
            img.compression_quality = 99
            img.resize(x,y)
            img.save(filename="./Original/"+file)
            img.save(filename="./Zoom/"+file)
    except:
        print("Error resizing.")


def zoom(zlevel):
    """
    Description: Resize all JPEGs currently in the ./Zoom directory.
    Parameters: 3
        zlevel: desired level of zoom between -9 and 9
        x: INT, current x dimension
        y: INT, current y dimension
    Return: 0
        -:-
    """
    x = 1600
    y = 2000
    level = {-9: 0.1, -8: 0.2, -7: 0.3, -6: 0.4, -5: 0.5, -4: 0.6, -3: 0.7, -2: 0.8, -1: 0.9, 0: 1.0,
             1: 1.1, 2: 1.2, 3: 1.3, 4: 1.4, 5: 1.5, 6: 1.6, 7: 1.7, 8: 1.8, 9: 1.9}
    try:
        for file in listdir("./Original"):
            img = wandImage(filename="./Original/"+file, resolution=300)
            img.compression_quality = 99
            img.resize(int(x*level[zlevel]), int(y*level[zlevel]))
            img.save(filename="./Zoom/"+file)
        return int(x*level[zlevel]), int(y*level[zlevel])
    except:
        print("Error zooming.")


def get_jpegs():
    """
    Description: Gather all JPEGs currently in the ./Zoom directory.
    Parameters: 0
        -:-
    Return: 1
        -: List containing PIL.image Image objects for each JPEG
    """
    return [pilImage.open("./Zoom/"+file) for file in listdir("./Zoom")]


def clear_jpegs():
    """
    Description:Remove all JPEGs currently in the ./Original and ./Zoom directories.
    Parameters: 0
        -:-
    Return: 0
        -:-
    """
    for file in listdir("./Original"):
        remove("./Original/"+file)
    for file in listdir("./Zoom"):
        remove("./Zoom/"+file)
'''--------------------------FUNCTIONS--------------------------'''


'''--------------------------DEBUGGING--------------------------'''


def debug():
    print("\nDebugging...\n")
    #Insert function calls here
    print("\n...Done debugging.\n")

if __name__ == "__main__":
    debug()
'''--------------------------DEBUGGING--------------------------'''
