# Main
import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

cred = credentials.Certificate("try/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-recognition-3e9a6-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket': "face-recognition-3e9a6.appspot.com"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("ไม่สามารถเปิดกล้องได้")
    exit()

cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')
file_path = 'EncodeFile.p'
print(f"Loading encode file from: {os.path.abspath(file_path)}")
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = [cv2.imread(os.path.join(folderModePath, path)) for path in modePathList]

# Load encode
print("Loading Encode File ...")
try:
    with open('EncodeFile.p', 'rb') as file:
        ListKnownWithIds = pickle.load(file)
    encodeListKnown, studentIds = ListKnownWithIds
    print(f"Successfully loaded {len(studentIds)} encodings")
except Exception as e:
    print(f"Error loading encode file: {str(e)}")
    exit()

modeType = 0
counter = 0
id = -1
imgStudent = []

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    
    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
    
    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
   
    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = studentIds[matchIndex]
                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (275, 300))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:
            if counter == 1:
                # Get the Data
                studentInfo = db.reference(f'Students/{id}').get()
                
                # Check if student info exists
                if studentInfo is None:
                    print(f"No data found for student ID: {id}")
                    modeType = 3  # Error mode
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                    continue

                # Get the Image from the storage
                blob_jpg = bucket.get_blob(f'{id}.jpg')
                blob_png = bucket.get_blob(f'{id}.png')
                        
                blob = blob_png if blob_png else blob_jpg
                        
                if blob:
                    array = np.frombuffer(blob.download_as_string(), np.uint8)
                    imgStudent = cv2.imdecode(array, cv2.IMREAD_COLOR)
                    if imgStudent is None or imgStudent.size == 0:
                        print(f"Failed to decode image for student ID {id}")
                    elif imgStudent.shape[:2] != (216, 216):
                        print(f"Image size for student ID {id} is not 216x216")
                        imgStudent = []
                else:
                    print(f"No image found for student ID {id}")
                    imgStudent = []

                # Check if last_attendance_time exists
                if 'last_attendance_time' not in studentInfo:
                    studentInfo['last_attendance_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    db.reference(f'Students/{id}').update({
                        'last_attendance_time': studentInfo['last_attendance_time']
                    })

                # Update data of attendance
                try:
                    datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                                     "%Y-%m-%d %H:%M:%S")
                    secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                    
                    if secondsElapsed > 30:
                        ref = db.reference(f'Students/{id}')
                        if 'total_attendance' not in studentInfo:
                            studentInfo['total_attendance'] = 0
                        studentInfo['total_attendance'] += 1
                        ref.child('total_attendance').set(studentInfo['total_attendance'])
                        ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                        modeType = 3
                        counter = 0
                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                except Exception as e:
                    print(f"Error updating attendance: {str(e)}")
                    modeType = 3
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if modeType != 3:
                if 10 < counter < 20:
                    modeType = 2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 10:
                    # Default values for missing fields
                    default_info = {
                        'total_attendance': 0,
                        'major': 'N/A',
                        'standing': 'N/A',
                        'year': 'N/A',
                        'starting_year': 'N/A',
                        'name-lastname': 'Unknown'
                    }
                    
                    # Update studentInfo with default values for missing fields
                    for key, value in default_info.items():
                        if key not in studentInfo:
                            studentInfo[key] = value

                    cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
                              cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
                              cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493),
                              cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
                              cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                              cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                              cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    (w, h), _ = cv2.getTextSize(studentInfo['name-lastname'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(studentInfo['name-lastname']), (808 + offset, 445),
                              cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    if len(imgStudent):
                        imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0

    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)