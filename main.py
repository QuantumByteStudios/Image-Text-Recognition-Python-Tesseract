# Install Tesseract on Linux --> sudo apt install tesseract

from fileinput import filename
import imp
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
from tkinter import filedialog
import tkinter as tk
import os
from tkinter import *
import platform
import cv2
import pytesseract

# Function Declearations


def universalClear():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def convertTuple(tup):
    st = ''.join(map(str, tup))
    return st


def uploadFile():

    f_types = [('PNG Files', '*.png'), ('Jpg Files', '*.jpg'),
               ('JPEG Files', '*.jpeg')]

    filename = tk.filedialog.askopenfilename(multiple=True, filetypes=f_types)
    filenameStr = convertTuple(filename)
    universalClear()
    image = cv2.imread(filenameStr)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    im2 = image.copy()
    text = pytesseract.image_to_string(im2)
    l4 = tk.Label(my_w, text=text, width=35, justify='center', font=my_font2)
    l4.grid(row=4, column=4, columnspan=5)
    f = open("Output.txt", 'w+')
    f.write(text)
    f.close
    universalClear()


# Main

universalClear()

my_w = tk.Tk()
my_w.geometry("470x350")
my_w.title('Image-Text Recognition')
my_font1 = ('arial', 20, 'bold')
my_font2 = ('times', 20, 'bold')

l1 = tk.Label(my_w, text=' ', width=30, font=my_font1)
l1.grid(row=0, column=0, columnspan=5)

l2 = tk.Label(my_w, text='Select an Image File', width=30, font=my_font1)
l2.grid(row=1, column=1, columnspan=5)

b1 = tk.Button(my_w, text='Browse',
               width=20, command=lambda: uploadFile())
b1.grid(row=2, column=2, columnspan=5)

l3 = tk.Label(my_w, text=' ', width=30, font=my_font1)
l3.grid(row=3, column=3, columnspan=5)

universalClear()

my_w.mainloop()
