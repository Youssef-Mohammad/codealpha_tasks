import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import cv2
import numpy as np
from ultralytics import YOLO
from sort import Sort

# Load YOLO model
model = YOLO("yolov8n.pt")

# Class names
names = model.names

# Initialize tracker
tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)

# Webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)[0]

    detections = []

    for box in results.boxes:
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
        conf = box.conf[0].cpu().numpy()
        cls = int(box.cls[0].cpu().numpy())
        label = names[cls]

        detections.append([x1, y1, x2, y2, conf])

    detections = np.array(detections)

    # Update tracker
    tracks = tracker.update(detections)

    for track in tracks:
        x1, y1, x2, y2, track_id = map(int, track)

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
        cv2.putText(
            frame,
            f"ID {track_id} - {label}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0,255,0),
            2
        )

    cv2.imshow("Object Detection & Tracking", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()