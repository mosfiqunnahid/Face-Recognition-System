import cv2
import numpy as np
import sqlite3

cam = cv2.VideoCapture(0)
# to use phones Cameras
# address="https://192.168.43.1:8080/video"
# cam.read(address)
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def insertOrUpdate(Id, Name, Age, Gender, JobPosition):
    conn = sqlite3.connect("FaceHub.db")
    cmd = "SELECT * FROM People WHERE ID=" + str(Id)
    cursor = conn.execute(cmd)
    isRecordExist = 0
    for row in cursor:
        isRecordExist = 1
    if isRecordExist == 1:

        cmd = "UPDATE People SET Name=" + str(Name) + " WHERE ID=" + str(Id)
    else:
        cmd = "INSERT INTO People(ID,Name,Age,Gender,JobPosition) Values(" + str(Id) + "," + str(Name) + "," + str(
            Age) + "," + str(Gender) + "," + str(JobPosition) + ")"
    conn.execute(cmd)
    conn.commit()
    conn.close()


Id = input('Enter your id: ')
Name = input('Enter Your Name: ')
Age = input('Enter Your Age: ')
Gender = input('Enter Your Gender: ')
JobPosition = input('Enter Your Job Position: ')
insertOrUpdate(Id, Name, Age, Gender, JobPosition)

sampleNum = 0
while (True):
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # incrementing sample number
        sampleNum = sampleNum + 1
        # saving the captured face in the dataset folder
        cv2.imwrite("dataSet/User." + Id + '.' + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])

        cv2.imshow('Ganerate Data', img)
    # wait for 100 miliseconds
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
    # break if the sample number is morethan 20
    elif sampleNum > 20:
        break
cam.release()
cv2.destroyAllWindows()
