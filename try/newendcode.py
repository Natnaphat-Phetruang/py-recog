import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import shutil
from datetime import datetime
import numpy as np
import sys

class FaceEncodingSystem:
    def __init__(self):
        # Set console encoding for Windows
        if sys.platform.startswith('win'):
            sys.stdout.reconfigure(encoding='utf-8')
            
        # Initialize Firebase
        cred = credentials.Certificate("C:/Users/natna/OneDrive/Desktop/Project_fimalcomsic/try/serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': "https://face-recognition-3e9a6-default-rtdb.asia-southeast1.firebasedatabase.app/",
            'storageBucket': "face-recognition-3e9a6.appspot.com"
        })
        
        # Create necessary directories
        self.directories = {
            'images': 'Files/Images',
            'processed': 'processed_images',
            'temp': 'temp_images',
            'backup': 'encoding_backups'
        }
        self.create_directories()
        
        self.bucket = storage.bucket()
        
    def create_directories(self):
        for directory in self.directories.values():
            os.makedirs(directory, exist_ok=True)
            
    def backup_existing_encoding(self):
        if os.path.exists("EncodeFile.p"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(self.directories['backup'], f'EncodeFile_{timestamp}.p')
            shutil.copy2("EncodeFile.p", backup_path)
            return True
        return False

    def load_existing_encoding(self):
        if os.path.exists("EncodeFile.p"):
            with open("EncodeFile.p", 'rb') as file:
                return pickle.load(file)
        return None

    def preprocess_image(self, image):
        """Improve image quality before encoding"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Enhance contrast using CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced_gray = clahe.apply(gray)
        
        # Convert back to BGR for face_recognition
        enhanced_bgr = cv2.cvtColor(enhanced_gray, cv2.COLOR_GRAY2BGR)
        
        return enhanced_bgr, enhanced_gray

    def find_encoding(self, image, student_id):
        """Find encoding for a single image with quality checks"""
        # Process image with grayscale
        enhanced_bgr, enhanced_gray = self.preprocess_image(image)
        
        # Use enhanced image for face detection
        face_locations = face_recognition.face_locations(enhanced_bgr)
        
        if not face_locations:
            print(f"No face found in image: {student_id}")
            return None, None
            
        if len(face_locations) > 1:
            print(f"Multiple faces found in image: {student_id}")
            return None, None
            
        try:
            # Use enhanced image for encoding
            encoding = face_recognition.face_encodings(enhanced_bgr, face_locations)[0]
            
            if np.any(np.isnan(encoding)):
                print(f"Invalid encoding for image: {student_id}")
                return None, None
                
            return encoding, face_locations[0]
        except Exception as e:
            print(f"Error encoding image {student_id}: {str(e)}")
            return None, None

    def crop_face(self, image, face_location, size=(216, 216)):
        """Crop and resize face image"""
        top, right, bottom, left = face_location
        face_image = image[top:bottom, left:right]
        return cv2.resize(face_image, size)

    def process_images(self):
        """Process all images"""
        print("Loading existing encodings...")
        existing_data = self.load_existing_encoding()
        existing_encodings = {}
        if existing_data:
            encodings, ids = existing_data
            existing_encodings = dict(zip(ids, encodings))
            print(f"Loaded {len(existing_encodings)} existing encodings")

        path_list = os.listdir(self.directories['images'])
        new_encodings = {}
        processed_files = []
        
        print(f"Processing {len(path_list)} new images...")
        for idx, path in enumerate(path_list, 1):
            student_id = os.path.splitext(path)[0]
            img_path = os.path.join(self.directories['images'], path)
            
            try:
                # Read original image
                original_img = cv2.imread(img_path)
                if original_img is None:
                    print(f"Cannot read image: {path}")
                    continue

                print(f"Processing image {idx}/{len(path_list)}: {path}")
                encoding, face_location = self.find_encoding(original_img, student_id)
                if encoding is not None:
                    new_encodings[student_id] = encoding

                    # Crop face from original image (color)
                    if face_location:
                        face_img = self.crop_face(original_img, face_location)
                        processed_path = os.path.join(self.directories['processed'], path)
                        cv2.imwrite(processed_path, face_img)

                        # Upload color image to Firebase
                        blob = self.bucket.blob(path)
                        blob.upload_from_filename(processed_path)
                        print(f"Successfully uploaded {path} to Firebase")

            except Exception as e:
                print(f"Error processing image {path}: {str(e)}")

        # Combine old and new encodings
        combined_encodings = {**existing_encodings, **new_encodings}
        
        # Save encoding file
        encode_data = [list(combined_encodings.values()), list(combined_encodings.keys())]
        with open("EncodeFile.p", 'wb') as file:
            pickle.dump(encode_data, file)

        return len(new_encodings), len(combined_encodings)

    def run(self):
        """Start the entire process"""
        print("Starting face encoding process...")
        
        if self.backup_existing_encoding():
            print("Successfully backed up existing encodings")
            
        new_count, total_count = self.process_images()
        
        print(f"Added {new_count} new encodings")
        print(f"Total encodings: {total_count}")
        print("Processing complete")

# Usage
if __name__ == "__main__":
    system = FaceEncodingSystem()
    system.run()