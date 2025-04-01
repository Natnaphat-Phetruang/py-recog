import cv2
import sys
sys.path.append("\users\natna\appdata\local\packages\pythonsoftwarefoundation.python.3.12_qbz5n2kfra8p0\localcache\local-packages\python312\site-packages\cv2")



# เปิดกล้องเว็บแคม
cap = cv2.VideoCapture(0)  # 0 หมายถึงการใช้กล้อง default ของระบบ, ถ้ามีกล้องเพิ่มเติมให้ใช้ 1, 2, 3, ...

while True:
    # อ่านภาพจากกล้อง
    ret, frame = cap.read()

    # แสดงภาพบนหน้าต่าง
    cv2.imshow('Webcam', frame)

    # หยุดการทำงานเมื่อกด 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ปิดกล้องเว็บแคมและหน้าต่าง
cap.release()
cv2.destroyAllWindows()
