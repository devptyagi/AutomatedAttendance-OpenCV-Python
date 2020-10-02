from datetime import datetime

import cv2
import sys
import csv
from tkinter import *
from time import strftime
import threading
import tkinter as tk
from PIL import Image, ImageTk


root = Tk()
root.configure(background='black')
status='Present'
dbpath = "data/db.csv"
'''photoName="bg.png"
background_image=tk.PhotoImage(file=photoName)
background_label = tk.Label(root,image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)'''
photoName="bg.png"
bg_image=tk.PhotoImage(file=photoName)
w = bg_image.width()
h = bg_image.height()
root.geometry("%dx%d+50+30" % (w, h))
cv=tk.Canvas(width=w, height=h)
cv.pack(fill='both', expand='yes')
cv.create_image(0, 0, image=bg_image, anchor='nw')




def facerecog():
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    video_capture = cv2.VideoCapture(0)	

    rec = cv2.face.LBPHFaceRecognizer_create()
    rec.read("trained_data/trainer.yml")


    id=0
    count = 0
    font=cv2.FONT_HERSHEY_TRIPLEX
    fontScale = 2
    thickness = 2
    loopcheck=True
    while loopcheck:
        
        ret, frame = video_capture.read(0)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30, 30),flags=cv2.CASCADE_SCALE_IMAGE)

        for (x, y, w, h) in faces:
            id,conf=rec.predict(gray[y:y+h,x:x+w])
            
            print (conf)

            name=''
            if(conf<60):
                print ("Face Matched")
                hh, ww, _ = frame.shape
                resize = cv2.resize(frame, (int(ww/4), int(hh/4)))
                cv2.imwrite('temp/display.png', resize)
                #cv2.imwrite('temp/display.png', frame[y:y+h,x:x+w])
                loopcheck = False
                loadImage = Image.open('temp/display.png')
                print(loadImage)
                render = ImageTk.PhotoImage(loadImage)
                img = Label(root, image = render)
                img.image = render
                img.place(x = 340, y = 50)
                

                
                with open('data/db.csv','r') as f:
                    reader=csv.reader(f, delimiter=',')
                    for ids in reader:
                        if(str(id) == ids[0]):
                            name = ids[2]
                alreadyMarked=0
                
                with open('Attendance-db/attendance.csv', 'a+', newline='') as csvFile:
                    csvFile.seek(0,0)
                    reader=csv.reader(csvFile, delimiter=',')
                    for ids in reader:
                        count = count + 1
                        roll=str(ids[0])
                        if(str(id) == roll):
                            alreadyMarked=1
                            break
                        else:
                            alreadyMarked=0
                    print("Already Marked? : "+ str(alreadyMarked))
                    if(alreadyMarked==0):
                        strTime = datetime.datetime.now().strftime("%H:%M:%S")
                        if hour >= 0 and hour < 12:
                            daytime = "Morning"
                        elif hour >= 12 and hour < 18:
                            daytime = "Afternoon"
                        else:
                            daytime = "Evening"
                        strTime = strTime + ' ' + daytime
                        writer = csv.writer(csvFile)
                        writer.writerow([id,name,status,strTime])
                    csvFile.close()

                if(alreadyMarked == 0):
                    msg = Label(root, text='Attendance Marked for ' + name)
                else:
                    msg = Label(root, text='Attendance for '+name+' has already been marked')
                msg.config(bg = 'black',fg = 'white', font = ('helvetica',10))
                msg.place(x=450,y=350)
                dbpath="Attendance-db/attendance.csv"
                msg.after(3000, msg.destroy)
                img.after(3000, img.destroy)

                
                
            break
    print(id)

def countStudent():
    with open('Attendance-db/attendance.csv', 'a+', newline='') as csvFile:
        csvFile.seek(0,0)
        reader=csv.reader(csvFile, delimiter=',')
        count=0
        for ids in reader:
            count=count+1
        countText = Label(root, text=str(count))
        countText.place(x=540,y=580)



login = Button(root, text="Mark", command = facerecog  ,fg = "black"  ,bg="grey"  ,width=20  ,height=3,font=('verdana', 18), borderwidth=1, relief='flat')
login.place(anchor = 'center', x=550, y=420)
countButton = Button(root, text="Student Present Count", command = countStudent  ,fg = "black"  ,bg="grey"  ,width=20  ,height=3,font=('verdana', 18), borderwidth=1, relief='flat')
countButton.place(anchor = 'center', x=550, y=520)

root.mainloop()


