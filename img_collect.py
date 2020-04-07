''''
Image Collection for machine learning purposes.
Version 0.01a
@author Jeraldy

TODO
- Document Code
- Optimization
- Better UI

'''
import os
import PIL
from PIL import Image,ImageTk
import pytesseract
import cv2
from tkinter import *
from tkinter import filedialog as fd
import tkinter as tk
import time
from threading import Thread


#OpenCV Webcam Setup
width, height = 50, 50
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)



#Initialize Tkinter Window
root = Tk()
root.geometry('600x400')
root.resizable(0,0)
root.bind('<Escape>', lambda e: root.quit())


#Methods


#create variables
savetoDir = ""
name = ""
width = 0
height = 0
countImages = 0

def openDir(entries):
    #Sets Variables for next buttons
    global savetoDir
    global name
    global width
    global height
    global countImages
    dir_name = fd.askdirectory()
    savetoDir = dir_name

    store = []
    for entry in entries:
        store.append(entry[1].get())
    name = store[0]
    countImages = int(store[1])
    width = int(store[2])
    height = int(store[3])


def testBtn():
    global savetoDir
    print(savetoDir)


def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = PIL.Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)

def fetch(entries):
    _, frame = cap.read()
    store = []
    for entry in entries:
        store.append(entry[1].get())
    width = store[2]
    height = store[3]
    #Create images
    for x in range(int(store[1])):
        output = cv2.resize(frame, (int(width), int(height)), interpolation = cv2.INTER_AREA)
        cv2.imwrite("{}/{}_{}.jpg".format(savetoDir, store[0], x), output)
        print("{}/{}_{}.jpg made".format(savetoDir, store[0], x))
        _, frame = cap.read()
        


def makeform(root, fields):
    entries = []
    for field in fields:
        row = tk.Frame(root)
        lab = tk.Label(row, width=15, text=field, anchor='w')
        ent = tk.Entry(row)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries.append((field, ent))
    return entries

running = False


def start_motor(event):
    # Create and start the new thread
    global running
    running = True
    t = Thread(target = burstShot, args = ())
    t.start()

def stop_motor(event):
    global running
    running = False

counter = 0
def burstShot():
    _, frame = cap.read()
    #Create images
    global counter
    global name
    global savetoDir
    while running and counter < countImages:
        output = cv2.resize(frame, (int(width), int(height)), interpolation = cv2.INTER_AREA)
        cv2.imwrite("{}/{}_{}.jpg".format(savetoDir, name, counter), output)
        print("{}/{}_{}.jpg made".format(savetoDir, name, counter))
        _, frame = cap.read()
        counter+=1



#Tkinter GUI layout
lmain = Label(root)
lmain.pack( side = LEFT )



rightFrame = Frame(root)
rightFrame.pack( side = RIGHT )

#Fields Constructor
fields = 'Name', 'Amount', 'Width', 'Height'
ents = makeform(rightFrame, fields)



#Save to Directory
saveToDir = Button(rightFrame, text="Save To", command=(lambda e=ents: openDir(e)))
saveToDir.pack()

#Burst Fire
testBtn = Button(rightFrame, text="Burst Fire", command=(lambda e=ents: fetch(e)))
testBtn.pack()

#burst test
button = Button(rightFrame, text ="forward")
button.pack()
button.bind('<ButtonPress-1>',start_motor)
button.bind('<ButtonRelease-1>',stop_motor)

#Quit
b2 = tk.Button(rightFrame, text='Quit', command=root.quit)
b2.pack()









show_frame()
root.mainloop()