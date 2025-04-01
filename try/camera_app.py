# # camera_app.py
# import streamlit as st
# import cv2
# import numpy as np
# import requests

# st.title("Face Recognition and Attendance System")

# run = st.checkbox('Run')
# FRAME_WINDOW = st.image([])

# cap = cv2.VideoCapture(0)

# while run:
#     ret, frame = cap.read()
#     if not ret:
#         break
    
#     frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     FRAME_WINDOW.image(frame_rgb)

#     # Convert frame to bytes
#     _, img_encoded = cv2.imencode('.jpg', frame)
#     img_bytes = img_encoded.tobytes()

#     # Send image to FastAPI
#     response = requests.post("http://localhost:8000/process/", files={"file": img_bytes})
    
#     if response.status_code == 200:
#         data = response.json()
#         if data["recognized"]:
#             studentInfo = data["studentInfo"]
#             st.write("Student Info:", studentInfo)
#         else:
#             st.write("Face not recognized or no face detected")
#     else:
#         st.write("Error in processing image")

# cap.release()
