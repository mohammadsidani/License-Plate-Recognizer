import tkinter
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import messagebox
#create gui application using tkinter
import easyocr
import numpy as np
import time
import imutils
import cv2
#easyocr and cv2 for optical character recognition, so it can read the license plate.

#la tsewe el gui app w title ela w soora icon mn barra w geometry bta3tiya size length and width wl resizable false false ya3ne ma btekbar el gui bl size
root = Tk()
root.title( "License Plate Recognizer" )
root.iconbitmap( "icon.ico" )
root.geometry( "1000x600" )
root.resizable( False, False )
my_Canvas = Canvas( root, height=1000, width=600 ) #canvas is a tool bl tkinter la ta3ml w tersom shapes sta3mlta la ersom el rectangle bl app yali bhot el soora wl buttons. 



def Select() :
    global image3
    root.filename = filedialog.askopenfilename 
        ( initialdir="Libraries", title="Select Image",
          filetypes=(("JPG", "*.jpg"), ("PNG", "*.png")) )
    entry.configure( state='normal' )
    entry.delete( 0, END )
    entry.insert( 0, root.filename )
    root1=root.filename
    image3 = Image.open( root.filename )
    resized_img3 = image3.resize( (505, 300) )
    image3 = ImageTk.PhotoImage( resized_img3 )
    my_Canvas.create_image( 265, 115, image=image3, anchor="nw" )
    img = cv2.imread( root.filename )
    gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
    entry.configure( state='disabled' )
    btn_Recognize.configure( state="normal" ,command = lambda : Recognize( img, gray ))



def exit() :
    res = messagebox.askyesno( 'Exit', 'Do you want to exit ?' )
    if res == True :

        time.sleep( 1 )
        Tk.quit( root )

    elif res == False :
        pass
    else :
        messagebox.showerror( 'error', 'something went wrong!' )


def Copy() :
    return

def Recognize(image,gray) :


    def EdgeDetection(gray):
        global image_side1
        bfilter = cv2.bilateralFilter( gray, 11, 17, 17 )
        edged = cv2.Canny( bfilter, 30, 200 )
        image_final = Image.fromarray( edged )
        image_final = image_final.resize( (200, 100) )
        image_side1 = ImageTk.PhotoImage( image_final )
        my_Canvas.create_image( 20, 110, image=image_side1, anchor="nw" )

        return edged
    data=EdgeDetection(gray)


    def location(data):
        global image_side2
        keypoints = cv2.findContours( data, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE )
        contours = imutils.grab_contours( keypoints )
        contours = sorted( contours, key=cv2.contourArea, reverse=True )[:10]
        location = None
        for contour in contours :
            approx = cv2.approxPolyDP( contour, 10, True )
            if len( approx ) == 4 :
                location = approx
                break
        global mask
        mask = np.zeros( gray.shape, np.uint8 )
        new_image = cv2.drawContours( mask, [location], 0, 255, -1 )
        new_image1 = cv2.bitwise_and( image, image, mask=mask )
        new_image2=Image.fromarray(new_image1)
        image_final = new_image2.resize( (200, 100) )
        image_side2 = ImageTk.PhotoImage( image_final )
        my_Canvas.create_image( 20, 240, image=image_side2, anchor="nw" )

        return new_image
    data2=location(data)

    def number(gray):
        global image_side3

        (x, y) = np.where( mask == 255 )
        (x1, y1) = (np.min( x ), np.min( y ))
        (x2, y2) = (np.max( x ), np.max( y ))
        cropped_image = gray[x1 :x2 + 1, y1 :y2 + 1]
        cropped= Image.fromarray( cropped_image )
        displayCrop = cropped.resize( (200, 100) )
        image_side3 = ImageTk.PhotoImage( displayCrop )
        my_Canvas.create_image( 20, 370, image=image_side3, anchor="nw" )
        reader = easyocr.Reader( ['en'] )
        result = reader.readtext( cropped_image )

        text = result[0][-2]
        return text

    plate=number(gray)

    entry1 = tkinter.Entry( root, width=40, font="Helvetica 44 bold" )
    entry2 = tkinter.Entry( root, width=40, font="Helvetica 44 bold" )
    entry3 = tkinter.Entry( root, width=40, font="Helvetica 44 bold" )
    entry4 = tkinter.Entry( root, width=40, font="Helvetica 44 bold" )
    entry5 = tkinter.Entry( root, width=40, font="Helvetica 44 bold" )
    entry6 = tkinter.Entry( root, width=40, font="Helvetica 44 bold" )
    entry7 = tkinter.Entry( root, width=40, font="Helvetica 44 bold" )
    entry_List = [entry2, entry3, entry4, entry5, entry6,entry7]
    entry1.place(x=210,y=500,width=70,height=70)
    num=" "+plate[0]
    entry1.insert(0,num)
    entry1.configure(state="disabled")
    h = 310
    i=2
    for e in entry_List :

        e.place( x=h, y=500, width=70, height=70 )
        num=" "+plate[i]
        e.insert( 0,num )
        e.configure( state='disabled' )
        h = h + 100
        i=i+1

    my_Canvas.create_text( 110, 90, text="Edge Detection", fill="#fff", font=('Helvetica 16 bold') )

    my_Canvas.create_text( 110, 224, text="Contouring", fill="#fff", font=('Helvetica 16 bold') )

    my_Canvas.create_text( 110, 354, text="Plate", fill="#fff", font=('Helvetica 16 bold') )


img1 = Image.open( "background1.jpg" )
resized_img1 = img1.resize( (1000, 620) )
image1 = ImageTk.PhotoImage( resized_img1 )

my_Canvas.pack( fill="both", expand=True )
my_Canvas.create_image( 0, 0, image=image1, anchor="nw" )
my_Canvas.create_rectangle( 260, 110, 775, 460, fill='#fff' )



image = Image.open("Cover.jpg" )
resized_img3 = image.resize( (505, 300) )
image3 = ImageTk.PhotoImage( resized_img3 )
my_Canvas.create_image( 265, 115, image=image3, anchor="nw" )

entry = tkinter.Entry( root, width=84 )
entry.insert( 0, "Selected Image Path" )
entry.configure( state="disabled" )
my_Canvas.create_window( 515, 90, window=entry )

my_Canvas.create_text( 485, 50, text="LICENSE PLATE RECOGNIZER", fill="#fff", font=('Helvetica 20 bold') )


my_Canvas.create_text( 855, 140, text="OPTIONS", fill="#fff", font=('Helvetica 15 bold') )
my_Canvas.pack()
my_Canvas.create_rectangle( 810, 330, 910, 170, outline="#fff" )

btn_Exit = Button( root, text="Exit", width=10, height=2, bd='4', command=exit, fg="#100852",
                   font=('Helvetica 8 bold') )
#btn_Copy = Button( root, text="Copy", width=10, height=2, bd='4', command=Copy, fg="#100852", font=('Helvetica 8 bold'),
      #             state="disabled" )


btn = Button( root, text='Select The Image Of The Plate!', width=23,
              height=2, bd='4', command=Select, fg="#100852", font=('Helvetica 8 bold') )

btn.place( x=420, y=416 )
btn_Recognize = Button( root, text="Recognize", width=10, height=2, bd='4',
                        fg="#100852", font=('Helvetica 8 bold'), state="disabled" )

btn_Exit.place( x=820, y=280 )
#btn_Copy.place( x=820, y=220 )
btn_Recognize.place( x=820, y=180 )

root.mainloop()
