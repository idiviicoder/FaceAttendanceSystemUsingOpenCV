import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    "databaseURL": "https://faceattendancesystem-8c8a8-default-rtdb.firebaseio.com/"
})
ref = db.reference('Students')

data = {
    "51456":
    {
        "name" : "Jatin Adhikari",
        "course" : "Management",
        "starting_year" : 2024,
        "total_attendance" : 14,
        "standing" : "Good",
        "year" : 1,
        "last_attendance_time" : "2024-09-04 00:54:34" 
    },

    "61456":
    {
        "name" : "Shreshtha Kumar Gupta",
        "course" : "MCA",
        "starting_year" : 2023,
        "total_attendance" : 17,
        "standing" : "Good",
        "year" : 2,
        "last_attendance_time" : "2024-09-04 01:24:14" 
    },

    "71456":
    {
        "name" : "Divyansh Magan",
        "course" : "MCA",
        "starting_year" : 2024,
        "total_attendance" : 20,
        "standing" : "Good",
        "year" : 1,
        "last_attendance_time" : "2024-09-03 12:54:34" 
    }
    
}

for key, value in data.items():
    ref.child(key).set(value)