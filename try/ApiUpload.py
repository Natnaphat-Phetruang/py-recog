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
import numpy as np
from newendcode import FaceEncodingSystem

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

# Initialize Firebase
# cred = credentials.Certificate("path/to/serviceAccountKey.json")
# firebase_admin.initialize_app(cred, {
#     'storageBucket': "face-recognition-3e9a6.appspot.com"
# })

bucket = storage.bucket()
face_system = FaceEncodingSystem()

def upload_to_firebase_storage(file_path: str, student_id: str, extension: str):
    """Upload file to Firebase Storage and return public URL"""
    destination_blob_name = f"student_images/{student_id}{extension}"
    blob = bucket.blob(destination_blob_name)
    
    blob.upload_from_filename(file_path)
    blob.make_public()  # If you want the image to be publicly accessible
    
    return blob.public_url

def load_student_image(student_id: str) -> tuple:
    """Load student image from Firebase Storage"""
    try:
        # Try both jpg and png extensions
        for ext in ['.jpg', '.png']:
            blob = bucket.blob(f'student_images/{student_id}{ext}')
            if blob.exists():
                # Download the image data
                image_data = blob.download_as_bytes()
                # Convert to numpy array
                nparr = np.frombuffer(image_data, np.uint8)
                # Decode the image
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                if img is not None:
                    # Resize if necessary
                    if img.shape[:2] != (216, 216):
                        img = cv2.resize(img, (216, 216))
                    return img, None
                
        return None, "ไม่พบรูปภาพของนักศึกษา"
    
    except Exception as e:
        return None, f"เกิดข้อผิดพลาดในการโหลดรูปภาพ: {str(e)}"

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
                temp_path = os.path.join("temp_images", file.filename)
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

                # Get file extension
                _, extension = os.path.splitext(file.filename)
                
                # Upload to Firebase Storage
                image_url = upload_to_firebase_storage(temp_path, student_id, extension)
                
                # Clean up temporary file
                os.remove(temp_path)

                successful_uploads.append({
                    "filename": file.filename,
                    "url": image_url
                })

            except Exception as e:
                failed_uploads.append({"filename": file.filename, "error": str(e)})
                continue

        # Store upload record in Realtime Database (optional, for tracking purposes)
        upload_record = {
            'studentId': student_id,
            'timestamp': datetime.now().isoformat(),
            'successful_uploads': successful_uploads,
            'failed_uploads': failed_uploads
        }
        
        # Run face encoding process if any files were successfully uploaded
        if successful_uploads:
            try:
                face_system.run()
            except Exception as e:
                print(f"Error during face encoding: {str(e)}")

        return {
            "message": "Upload process completed",
            "successful_uploads": successful_uploads,
            "failed_uploads": failed_uploads
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)