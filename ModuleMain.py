import cv2 as cv
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    "databaseURL": "https://faceattendancesystem-8c8a8-default-rtdb.firebaseio.com/",
    "storageBucket" : "faceattendancesystem-8c8a8.appspot.com"
})


capture = cv.VideoCapture(0)

#import the encoding file
file = open("EncodeFile.p","rb")
encodeListWithIds = pickle.load(file)
file.close()
encodeList, studentIds = encodeListWithIds
# print(studentIds)


counter = 0
id = -1
while True:
    success, frame = capture.read()

    imgS = cv.resize(frame,(0,0),None,0.25,0.25)
    imgS = cv.cvtColor(imgS, cv.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)#we are passing the locations along the image as we dont want the encoding of the whole image we just need it for the fface

    for encoFace,  faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeList, encoFace)
        faceDist = face_recognition.face_distance(encodeList, encoFace)
        # print("Matches: ", matches)
        # print("FaceDistance: ", faceDist)

        matchindex = np.argmin(faceDist)
        # print("Match Index ", matchindex)

        if matches[matchindex]:
            # print("Student's ID: ", studentIds[matchindex])
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cvzone.cornerRect(frame, bbox=(x1,y1, x2-x1, y2-y1), rt=0)
            id = studentIds[matchindex] 
            if counter == 0:
                counter = 1
        if counter != 0:
            if counter == 1:
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)
            counter += 1


    # displaying each frame
    cv.imshow('webcam',  frame)
    if cv.waitKey(20) & 0xFF==ord('d'):#if the letter d is pressed then break the loop and stop this video
        break
capture.release()
cv.destroyAllWindows()
