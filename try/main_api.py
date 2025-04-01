from fastapi import FastAPI, WebSocket, Depends, HTTPException, Request
import jwt
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
import time
from face_checker import FaceCheckwahummanjinba
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
import base64
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, ImageDraw, ImageFont
import json
from fastapi.websockets import WebSocketState

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="C:/Users/natna/OneDrive/Desktop/Project_fimalcomsic/templates")

# Initialize Firebase
cred = credentials.Certificate("C:/Users/natna/OneDrive/Desktop/Project_fimalcomsic/try/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-recognition-3e9a6-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket': "face-recognition-3e9a6.appspot.com"
})

bucket = storage.bucket()

# Load Background and Modes
imgBackground = cv2.imread('C:/Users/natna/OneDrive/Desktop/Project_fimalcomsic/Resources/background.png')
if imgBackground is None:
    raise ValueError("Background image not found or failed to load.")

folderModePath = 'C:/Users/natna/OneDrive/Desktop/Project_fimalcomsic/Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    img = cv2.imread(os.path.join(folderModePath, path))
    if img is None:
        raise ValueError(f"Mode image {path} not found or failed to load.")
    imgModeList.append(img)

# Load Encode File
print("Loading Encode File ...")
with open('C:\\Users\\natna\\OneDrive\\Desktop\\Project_fimalcomsic\\EncodeFile.p', 'rb') as file:
    ListKnownWithIds = pickle.load(file)
encodeListKnown, studentIds = ListKnownWithIds

# Initialize FaceChecker
face_checker = FaceCheckwahummanjinba("C:/Users/natna/OneDrive/Desktop/Project_fimalcomsic/model/l_version_1_300.pt")

# Initialize Variables
modeType = 0
counter = 0
id = -1
imgStudent = []
standings = []

# Secret Key for JWT
SECRET_KEY = "API_KEY_2024"

def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token หมดอายุแล้ว")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token ไม่ถูกต้อง")

def load_student_image(studentId, bucket):
    try:
        print(f"Student ID: {studentId}")
        studentInfo = db.reference(f'Students/{studentId}').get()
        if not studentInfo:
            return None, f"ไม่พบข้อมูลนักเรียนรหัส {studentId}"

        blob = bucket.get_blob(f'{studentId}.jpg') or bucket.get_blob(f'{studentId}.png')
        print(f"Blob found: {blob}")
        if not blob:
            return None, f"ไม่พบรูปภาพสำหรับนักเรียนรหัส {studentId}"

        array = np.frombuffer(blob.download_as_string(), np.uint8)
        imgStudent = cv2.imdecode(array, cv2.IMREAD_COLOR)

        if imgStudent is None or imgStudent.size == 0:
            return None, f"ไม่สามารถถอดรหัสรูปภาพสำหรับนักเรียนรหัส {studentId}"

        if imgStudent.shape[:2] != (216, 216):
            imgStudent = cv2.resize(imgStudent, (216, 216))

        return imgStudent, None
    except Exception as e:
        return None, f"เกิดข้อผิดพลาดในการโหลดรูปภาพ: {str(e)}"

def process_image_frame(img, classroomId, websocket):
    global imgBackground, modeType, counter, imgStudent
    imgBackground = np.copy(imgBackground)
    
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    
    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
    attendance_data = None
    websocket_data = None
     
    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:
        is_real = face_checker.check_face(imgBackground[162:162 + 480, 55:55 + 640])
        if is_real:
            for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                    imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                    studentId = studentIds[matchIndex]

                    if counter == 0:
                        cvzone.putTextRect(imgBackground, "Loading", (275, 300))
                        counter = 1
                        modeType = 1

                    if counter == 1:
                        attendance_ref = db.reference(f'rooms/{classroomId}/members/{studentId}')
                        attendance_data = attendance_ref.get()

                        if attendance_data is not None:
                            today = datetime.now().date()
                            current_time = datetime.now()

                            start_time_str = attendance_data['startTime']
                            end_time_str = attendance_data['endTime']
                            startTime = datetime.combine(today, datetime.strptime(start_time_str, "%H:%M:%S").time())
                            endTime = datetime.combine(today, datetime.strptime(end_time_str, "%H:%M:%S").time())
                            time_diff = (current_time - startTime).total_seconds() / 60

                            if current_time >= endTime:
                                standings = 'ขาดเรียน'
                            elif time_diff < 0:
                                standings = 'ยังไม่ถึงเวลา'
                            elif time_diff <= 15:
                                standings = 'มาตรงเวลา'
                            elif time_diff <= (endTime - startTime).total_seconds() / 60:
                                standings = 'มาสาย'
                            else:
                                standings = 'ขาดเรียน'

                            if 'last_attendance_time' in attendance_data:
                                datetimeObject = datetime.strptime(attendance_data['last_attendance_time'], 
                                        "%Y-%m-%d %H:%M:%S")
                            else:
                                datetimeObject = current_time

                            secondsElapsed = (current_time - datetimeObject).total_seconds()
                            
                            if secondsElapsed > 30:
                                current_total_attendance = attendance_data.get('total_attendance', 0) + 1
                                attendance_ref.update({
                                    'total_attendance': current_total_attendance,
                                    'last_attendance_time': current_time.strftime("%Y-%m-%d %H:%M:%S"),
                                    'standing': standings
                                })

                                websocket_data = {
                                    'studentId': studentId,
                                    'total_attendance': current_total_attendance,
                                    'standing': standings,
                                    'classroomId': classroomId,
                                }

                        imgStudent, error_message = load_student_image(studentId, bucket)
                        if error_message:
                            print(error_message)
                            modeType = 3
                            counter = 0
                            imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                            return imgBackground, websocket_data

                    if modeType != 3:
                        if 10 < counter < 20:
                            modeType = 2

                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                        if counter <= 10 and attendance_data:
                            cv2.putText(imgBackground, str(attendance_data.get('total_attendance', 0)), (861, 125),
                                      cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                            cv2.putText(imgBackground, str(attendance_data.get('major', 'N/A')), (1006, 550),
                                      cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                            cv2.putText(imgBackground, str(studentId), (1006, 493),
                                      cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                            cv2.putText(imgBackground, str(attendance_data.get('standing', 'N/A')), (910, 625),
                                      cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                            name = f"{attendance_data.get('fname', '')} {attendance_data.get('lname', '')}"
                            (w, h), _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                            offset = (414 - w) // 2
                            cv2.putText(imgBackground, name, (808 + offset, 445),
                                      cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                            if imgStudent is not None:
                                imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

                        counter += 1

                        if counter >= 20:
                            counter = 0
                            modeType = 0
                            attendance_data = None
                            imgStudent = None
                            imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0

    return imgBackground, websocket_data

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws/{classroomId}")
async def websocket_endpoint(websocket: WebSocket, classroomId: str, token: str = Depends(verify_jwt_token)):
    await websocket.accept()
    cap = cv2.VideoCapture(0)

    retries = 5
    try:
        while retries > 0:
            try:
                if not cap.isOpened():
                    cap.open(0)

                while True:
                    if websocket.client is None:
                        print("WebSocket is closed, exiting loop.")
                        break
                    
                    success, img = cap.read()
                    if not success:
                        raise ValueError("Failed to read image from camera")

                    imgBackground, websocket_data = process_image_frame(img, classroomId, websocket)

                    _, img_encoded = cv2.imencode('.jpg', imgBackground)
                    img_base64 = base64.b64encode(img_encoded).decode('utf-8')
                    
                    await websocket.send_text(img_base64)

                    if websocket_data and websocket.client_state == WebSocketState.CONNECTED:
                        await websocket.send_text(json.dumps(websocket_data))
                        print(f"Sent data to WebSocket: {websocket_data}")

            except (ValueError, ConnectionResetError) as e:
                print(f"Error occurred: {e}. Retrying...")
                retries -= 1
                time.sleep(2)
                if retries == 0:
                    print("Failed to connect after several retries.")
                    await websocket.close()
    finally:
        cap.release()

@app.get("/process", response_class=FileResponse)
async def process_image():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    success, img = cap.read()
    imgBackground, _ = process_image_frame(img, None, None)

    output_path = "static/images/processed_image.png"
    cv2.imwrite(output_path, imgBackground)

    return output_path