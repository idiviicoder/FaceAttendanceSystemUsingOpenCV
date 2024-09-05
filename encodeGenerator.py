import cv2 as cv
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    "databaseURL": "https://faceattendancesystem-8c8a8-default-rtdb.firebaseio.com/",
    "storageBucket" : "faceattendancesystem-8c8a8.appspot.com"
})

#importing the student images
folderpath = "Images"
imagePathList = os.listdir(folderpath)
imgList = []
studentIds = []
for path in imagePathList:
    imgList.append(cv.imread(os.path.join(folderpath,path)))
    studentIds.append(os.path.splitext(path)[0])
    fileName = f'{folderpath}/{path}'
    bucket = storage.bucket() 
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

    
def findEncodings(imagesList):
    encodeList = []
    for img in  imagesList:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


encodeList = findEncodings(imgList)
print(encodeList)
print("Encoding Complete")

encodeListWithIds = [encodeList, studentIds]
file = open("EncodeFile.p", "wb")
pickle.dump(encodeListWithIds, file)
file.close()
print("File Saved")
