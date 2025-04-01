import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import cv2
import numpy as np

# Initialize Firebase
cred = credentials.Certificate("try/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-recognition-3e9a6-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket': "face-recognition-3e9a6.appspot.com"
})

# Access the storage bucket
bucket = storage.bucket()

# List all files in the storage bucket
blobs = bucket.list_blobs()
print("Files in storage bucket:")

for blob in blobs:
    # Check if the file is an image (JPG or PNG)
    if blob.name.endswith(('.jpg', '.png')):
        # Download the image file as a byte array
        image_bytes = blob.download_as_string()
        
        # Convert the byte array to a numpy array
        np_array = np.frombuffer(image_bytes, np.uint8)
        
        # Decode the numpy array as an image
        image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        
        # Check if the image is 216x216
        if image is not None:
            height, width, _ = image.shape
            if height == 216 and width == 216:
                print(f"{blob.name} is 216x216")
            else:
                print(f"{blob.name} is not 216x216, its size is {width}x{height}")
        else:
            print(f"Failed to decode {blob.name}")
