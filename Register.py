import os
import cv2
import csv
import sys
import numpy as np
from PIL import Image, ImageTk
from tkinter import *
import PIL.Image
import tkinter as tk

path = 'data_set'
dbpath = "data/db.csv"

window=Tk()
window.title("Automated Attendance System")
photoName="bg.png"
bg_image=tk.PhotoImage(file=photoName)
w = bg_image.width()
h = bg_image.height()
window.geometry("%dx%d+50+30" % (w, h))
cv=tk.Canvas(width=w, height=h)
cv.pack(side='top', fill='both', expand='yes')
cv.create_image(0, 0, image=bg_image, anchor='nw')
cv.create_text(100, 230, text="Enter Name", fill="white", anchor='nw')
cv.create_text(630, 230, text="Enter Roll Number", fill="white", anchor='nw')


window.configure(background = 'black')

#Name Input
#button1 = Label(window, text="Enter Name", width=25, height=3, fg='white', bg='black',font=('adobe_pi_std', 15))
#button1.place(x=120,y=200)
b1 = Entry(window, width=30, bg='white', fg="black", font=('adobe_pi_std', 10))
b1.place(x=250,y=227)


#Mail Input
#button2 = Label(window, text="Enter Roll Number", width=25, height=3, fg='white', bg='black',font=('adobe_pi_std', 15))
#button2.place(x=650,y=200)
b2 = Entry(window, width=30, bg='white', fg="black", font=('adobe_pi_std', 10))
b2.place(x=780,y=227)


#Creating CSV File - Face ID, Email, Name
def writeData():
    try:   
        with open(dbpath,'r') as f:
            reader=csv.reader(f, delimiter=',')
            checkDuplicate=0
            totalrec=0
            for ids in reader:
                e_id=str(ids[1])
                totalrec+=1;
                if(e_id==b2.get()):
                    checkDuplicate=1
                else:
                    checkDuplicate=0

            if(checkDuplicate==1):
                msg=Label(window, text='User exists')
                msg.config(bg='#340390',fg='white', font=('helvetica',10))
                msg.place(x=890,y=255)
                window.after(2000,msg.destroy)
                f.close()
            else:
                with open(dbpath, 'a', newline='') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow([totalrec+1,b2.get(),b1.get()])
                    csvFile.close()
                    
                Dataset(totalrec+1)
                trainer(totalrec+1)
            
    except FileNotFoundError as err:
        f = open(dbpath, 'w')
        writeData()


#DATASET_CREATOR
def Dataset(faceID):

    name=b2.get()
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    video_capture = cv2.VideoCapture(1)	

    entrynumber=0
    while True:
        ret, frame = video_capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        for (x, y, w, h) in faces:
            entrynumber+=1;
            n=b1.get()
            cv2.imwrite("data_set/User."+str(faceID)+"."+str(entrynumber)+".jpg",gray[y:y+h,x:x+w])
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.waitKey(70)
        cv2.imshow('Video', frame)
        cv2.waitKey(1)
        if(entrynumber>24):
            msg1=Label(window, text='Face Registered Succesfully')
            msg1.config(bg='#340390',fg='white', font=('adobe_pi_std',15))
            msg1.place(x=550, y=570)
            window.after(5000,msg1.destroy)
            break

            video_capture.release()
    cv2.destroyAllWindows()




def getImagesWithID(path):
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    faces=[]
    IDs=[]
    for imagePath in imagePaths:
        if imagePath == 'data_set/.DS_Store':
            continue
        faceImg=PIL.Image.open(imagePath).convert('L')
        faceNp=np.array(faceImg)
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(faceNp)
        IDs.append(ID)
    return IDs, faces

def trainer(Face_ID):
    recognizer=cv2.face.LBPHFaceRecognizer_create();
    Ids,faces=getImagesWithID(path)
    recognizer.train(faces, np.array(Ids))
    recognizer.save('trained_data/trainer.yml')
    cv2.destroyAllWindows()




#Register Button
register = Button(window, text="Register", command = writeData ,fg="Black"  ,bg="White"  ,width=20  ,height=3,font=('adobe_pi_std', 15))
register.place(x=470, y=350)


