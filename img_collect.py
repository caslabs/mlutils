''''
Image Collection for machine learning purposes.
Version 0.01a
@author Jeraldy

TODO
  * Optimization
  * Better UI
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
from tkinter import messagebox
from threading import Thread
import tkinter.scrolledtext as tkscrolled

#Thread for burst shots
running = False

#create variables
savetoDir = ""
name = ""
width = 0
height = 0
countImages = 0




#OpenCV Webcam Setup
width, height = 50, 50
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)



#Initialize Tkinter Window
root = Tk()
root.title("img collect")
root.geometry('600x400')
root.resizable(0,0)
root.bind('<Escape>', lambda e: root.quit())

#Tkinter GUI layout
lmain = Label(root)
lmain.pack( side = LEFT )
rightFrame = Frame(root)
rightFrame.pack( side = RIGHT )

def openDir(entries):
    """
    Saves Users Input and Initiates Burst Feature.

    Keyword Arguments
    entries --Form Entries Data
    """
    global savetoDir
    global name
    global width
    global height
    global countImages

    #Gets Value inputs and stores in array
    store = []
    for entry in entries:
        store.append(entry[1].get())

    #Enable Burst Photo Feature
    print(not name)
    print(not store[1])
    if ((store[0]) and (store[1]) and (store[2]) and (store[3])):
        dir_name = fd.askdirectory()
        savetoDir = dir_name
        burstBtn['state'] = NORMAL
        #Saves input in global variables
        name = store[0]
        countImages = int(store[1])
        width = int(store[2])
        height = int(store[3])

    else:
        tk.messagebox.showerror(title="Error", message="Please Fill out Form")


def show_frame():
    """
    Shows opencv-python image frame.

    """
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = PIL.Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)

def fetch(entries):
    """
    Burst Mode Feature - Iterates through n amount 

    Keyword Arguments:
    entries -- Form Entries Data
    
    """
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
    """
    Constructs Customized Forms based on Field Constructor

    Keyword Arguments:
    root -- Tkinter Root Window
    fields -- Custom fields

    """
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



def onHold(event):
    """
    Initialize Thread to spy on Button Hold

    Keyword Arguments:
    event -- Corresponding Button

    """
    
    global running
    running = True
    t = Thread(target = burstShot, args = ())
    t.start()


def offHold(event):
    """
    Deactivates the running thread..

    Keyword Arguments:
    event -- Corresponding Button

    """
    global running
    running = False

#Record Burst Shot Amounts
counter = 0
def burstShot():
    """
    Takes and saves screenshots of cam image while button is on hold.

    """
    _, frame = cap.read()
    global counter
    global name
    global savetoDir

    #On button hold, resize and save cam image to the targeted directory until reach desired amount
    while running and counter < countImages:
        output = cv2.resize(frame, (int(width), int(height)), interpolation = cv2.INTER_AREA)
        cv2.imwrite("{}/{}_{}.jpg".format(savetoDir, name, counter), output)
        print("{}/{}_{}.jpg made".format(savetoDir, name, counter))
        TKScrollTXT.insert(1.0, "{}/{}_{}.jpg made\n".format(savetoDir, name, counter))
        _, frame = cap.read()
        counter+=1
        if (counter == countImages):
            TKScrollTXT.insert(1.0, "Done!\n")


def quitWindow():
    """
    Quits the Window.
    """
    result =  tk.messagebox.askquestion("Delete", "Are You Sure?", icon='warning')
    if result == 'yes':
        root.quit()



#Form Fields Constructor
fields = 'Name', 'Amount', 'Width', 'Height'
ents = makeform(rightFrame, fields)


#Save to Directory UI
saveToDir = Button(rightFrame, text="Save To", command=(lambda e=ents: openDir(e)))
saveToDir.pack()


#Burst Button UI
burstBtn = Button(rightFrame, text ="Burst Fire")
burstBtn.pack()
burstBtn.bind('<ButtonPress-1>',onHold)
burstBtn.bind('<ButtonRelease-1>',offHold)
burstBtn['state'] = DISABLED

#Quit
b2 = tk.Button(rightFrame, text='Quit', command=quitWindow)
b2.pack()

#Initiate Text Scroll Component
default_text = 'Waiting for Burst Fire'
widthS, heightS = 50,10
TKScrollTXT = tkscrolled.ScrolledText(rightFrame, width=widthS, height=heightS, wrap='word')

# set default text if desired
TKScrollTXT.insert(1.0, default_text)
TKScrollTXT.pack()

show_frame()
root.mainloop()