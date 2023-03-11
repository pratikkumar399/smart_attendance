from tkinter import *
from tkinter import ttk
from functools import partial
from tkinter import messagebox
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from datetime import date

# Attendance marking Code

cap = cv2.VideoCapture(0)

x = str(date.today())

# Image Encoding


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

# Marking attendance in csv file


def markAttendance(name):
    with open("E:\python\smart-attendane-system-using-python-main\pythonProject\Attendance/"+combo.get()+"_"+x+".csv", 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

# FOR CAPTURING SCREEN RATHER THAN WEBCAM
# def captureScreen(bbox=(300,300,690+300,530+300)):
#     capScr = np.array(ImageGrab.grab(bbox))
#     capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
#     return capScr

# Face Capture


def startprogram():

    cap = cv2.VideoCapture(0)

    path = 'E:\python\smart-attendane-system-using-python-main\pythonProject\ImagesAttendance'
    images = []
    classNames = []
    myList = os.listdir(path)
    print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)

    encodeListKnown = findEncodings(images)
    print('Encoding Complete')

    f = open("E:\python\smart-attendane-system-using-python-main\pythonProject\Attendance/" +
             combo.get()+"_"+x+".csv", 'w')
    f.write("Name,Timestamp")
    f.close()
    while True:
        success, img = cap.read()
        # img = captureScreen()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(
                encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(
                encodeListKnown, encodeFace)
            # print(faceDis)
            matchIndex = np.argmin(faceDis)

            if faceDis[matchIndex] < 0.50:
                name = classNames[matchIndex].upper()
                markAttendance(name)
            else:
                name = 'Unknown'
            # print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2),
                          (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('Webcam', img)


# To stop the attendance
        if cv2.waitKey(1) & 0xFF == ord('F'):
            cap.release()
            cv2.destroyAllWindows()
            break

# GUI CODE

# closing attendance window


def on_closing2():
    tkWindow2.withdraw()
    tkWindow.deiconify()

# closing main login window


def on_closing1():
    x = messagebox.askquestion('askquestion', 'Do you wan t to exit ?')
    if x == 'yes':
        tkWindow.destroy()
        tkWindow2.destroy()

# attendance page show


def New_Window():
    tkWindow.withdraw()
    tkWindow2.deiconify()

# login button method


def validateLogin(username, password):
    if username.get() == "user":
        if password.get() == "user":
            print("LOGGED IN SUCCESSFULY")
            usernameEntry.delete(0, END)
            passwordEntry.delete(0, END)
            New_Window()
        else:
            messagebox.showwarning(
                "showwarning", "Wrong username or password !")
            usernameEntry.delete(0, END)
            passwordEntry.delete(0, END)
    else:
        messagebox.showwarning("showwarning", "Wrong username or password !")
        usernameEntry.delete(0, END)
        passwordEntry.delete(0, END)
    return

# attendance button method


def finalPage():
    print("Attendance Marked")
    startprogram()
    messagebox.showinfo("showinfo", "Attendance Recorded !")


# window1
tkWindow = Tk()
tkWindow.geometry('300x300')
tkWindow.title('Attendance System')
tkWindow.protocol("WM_DELETE_WINDOW", on_closing1)

# window2
tkWindow2 = Tk()
tkWindow2.geometry('300x300')
tkWindow2.withdraw()
tkWindow2.title('MCOE-AIML Attendance System')
tkWindow2.protocol("WM_DELETE_WINDOW", on_closing2)

# username label and text entry box
usernameLabel = Label(tkWindow, text="User Name").place(x=17, y=20)
username = StringVar()
usernameEntry = Entry(tkWindow, textvariable=username)
usernameEntry.place(x=90, y=20)

# password label and password entry box
passwordLabel = Label(tkWindow, text="Password").place(x=20, y=50)
password = StringVar()
passwordEntry = Entry(tkWindow, textvariable=password, show='*')
passwordEntry.place(x=90, y=50)

validateLogin = partial(validateLogin, username, password)

# login button
loginButton = Button(tkWindow, text="Login",
                     command=validateLogin).place(x=100, y=100)

# attendance button
attendancebutton = Button(
    tkWindow2, text="Start Attendance", command=finalPage).place(x=77, y=105)

subjects = Label(tkWindow2, text="Select the subject :").place(x=87, y=45)

# create a drop down list
sizes = [
    "C++", "Java", "Python", "JavaScript", "Rust", "GoLang"
]

combo = ttk.Combobox(tkWindow2, values=sizes, state="readonly")
combo.place(x=45, y=71)
combo.current(0)


# stop attendance
quitLable = Label(
    tkWindow2, text="Press F to stop attendance").place(x=68, y=135)

tkWindow.mainloop()
