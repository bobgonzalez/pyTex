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
	Description: Convert a single/multi-page PDF document into JPEGs saved in the ./TMP directory.
	Parameters: 1
		filepath: String, Path to PDF document 
	Return: 0
		-:-
	"""
	try:
		with wandImage(filename=filepath) as img:
			img.save(filename="./TMP/"+filepath[:-3]+"jpg")
	except MissingDelegateError:
		print("\n\nFile entered is not a pdf file!\nOr imagemagick is not installed: brew install imagemagick\n\n")
	
def resize(x, y):
	"""
	Description: Resize all JPEGs currently in the ./TMP directory.
	Parameters: 2
		x: INT, desired x dimension 
		y: INT, desired y dimension		
	Return: 0
		-:-
	"""
	try:
		for file in os.listdir("./TMP"):
			img = wandImage(filename="./TMP/"+file)
			img.resize(x,y)
			img.save(filename="./TMP/"+file) 
	except:
		print("Error resizing.")

def get_jpegs():
	"""
	Description: Gather all JPEGs currently in the ./TMP directory.
	Parameters: 0
		-:-
	Return: 1
		-: List containing PIL.image Image objects for each JPEG 
	"""
	return [pilImage.open("./TMP/"+file) for file in listdir("./TMP") ]

def clear_jpegs():
	"""
	Description:Remove all JPEGs currently in the ./TMP directory.
	Parameters: 0
		-:-
	Return: 0
		-:-
	"""
	for file in os.listdir("./TMP"):
		remove("./TMP/"+file)
'''--------------------------FUNCTIONS--------------------------'''


'''--------------------------DEBUGGING--------------------------'''
def debug():
	print("\nDebugging...\n")	
	#Insert function calls here
	pdf2jpg("./BITSCTF_Mis_Labour_20_Feb17.pdf")
	print get_jpegs()
	print("\n...Done debugging.\n")	
		
if __name__ == "__main__":
	debug()
'''--------------------------DEBUGGING--------------------------'''
		