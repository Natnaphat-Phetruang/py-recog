import math
import cv2
import cvzone
from ultralytics import YOLO

class FaceCheckwahummanjinba:
    def __init__(self, model_path, confidence_threshold=0.3):
        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold
        self.class_names = ["fake", "real"]

    def check_face(self, img):
        results = self.model(img, stream=True, verbose=False)
        for r in results:
            boxes = r.boxes
            for box in boxes:
                conf = math.ceil((box.conf[0] * 100)) / 100
                cls = int(box.cls[0])
                if conf > self.confidence_threshold:
                    if self.class_names[cls] == 'fake':
                        return True
                    else:
                        cvzone.putTextRect(img, f'{self.class_names[cls].upper()} {int(conf*100)}%',
                                           (max(0, int(box.xyxy[0][0])), max(35, int(box.xyxy[0][1]))), scale=2, thickness=4,
                                           colorR=(0, 0, 255), colorB=(0, 0, 255))
        return False
