from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn
import os
import json
import shutil
from datetime import datetime
import cv2
import face_recognition
import firebase_admin
from firebase_admin import credentials, storage, db
from newendcode  import FaceEncodingSystem  # Import the FaceEncodingSystem class

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:3000",
    "http://localhost:3333"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Firebase and FaceEncodingSystem
# # cred = credentials.Certificate("C:/Users/natna/OneDrive/Desktop/Project_fimalcomsic/try/serviceAccountKey.json")
# firebase_admin.initialize_app(cred, {
#     'databaseURL': "https://face-recognition-3e9a6-default-rtdb.asia-southeast1.firebasedatabase.app/",
#     'storageBucket': "face-recognition-3e9a6.appspot.com"
# })

# Create necessary directories
UPLOAD_DIR = "Files/Images"
TEMP_DIR = "temp_images"
PROCESSED_DIR = "processed_images"

for directory in [UPLOAD_DIR, TEMP_DIR, PROCESSED_DIR]:
    os.makedirs(directory, exist_ok=True)

face_system = FaceEncodingSystem()

@app.post("/upload/")
async def upload_files(
    files: List[UploadFile] = File(...),
    metadata: str = Form(...)
):
    try:
        # Parse metadata
        metadata_dict = json.loads(metadata)
        student_id = metadata_dict.get('studentId')
        
        if not student_id:
            raise HTTPException(status_code=400, detail="Student ID is required")

        successful_uploads = []
        failed_uploads = []

        # Process each uploaded file
        for file in files:
            try:
                # Save temporary file
                temp_path = os.path.join(TEMP_DIR, file.filename)
                with open(temp_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)

                # Read and check image
                img = cv2.imread(temp_path)
                if img is None:
                    failed_uploads.append({"filename": file.filename, "error": "Invalid image file"})
                    continue

                # Check for face in image
                face_locations = face_recognition.face_locations(img)
                if not face_locations:
                    failed_uploads.append({"filename": file.filename, "error": "No face detected"})
                    continue

                # Save to Images directory for encoding
                final_filename = f"{student_id}.jpg"
                final_path = os.path.join(UPLOAD_DIR, final_filename)
                shutil.copy2(temp_path, final_path)

                # Clean up temporary file
                os.remove(temp_path)

                successful_uploads.append(file.filename)

            except Exception as e:
                failed_uploads.append({"filename": file.filename, "error": str(e)})
                continue

        # Run face encoding process if any files were successfully uploaded
        if successful_uploads:
            try:
                face_system.run()
            except Exception as e:
                print(f"Error during face encoding: {str(e)}")
                # Continue anyway as files were uploaded successfully

        # Update database with upload record
        ref = db.reference('uploads')
        upload_record = {
            'studentId': student_id,
            'timestamp': datetime.now().isoformat(),
            'successful_uploads': successful_uploads,
            'failed_uploads': failed_uploads
        }
        ref.push(upload_record)

        return {
            "message": "Upload process completed",
            "successful_uploads": successful_uploads,
            "failed_uploads": failed_uploads
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)