from ultralytics import YOLO
from PIL import Image
import cv2

model = YOLO('yolov8n.pt')
img = cv2.imread('images/objects/object_bottle15.jpg')
results = model(img)

# for index, row in boxes.iterrows():
#     print(f"Class: {row['name']}, Confidence: {row['confidence']}, Bounding Box: {row[['xmin', 'ymin', 'xmax', 'ymax']].tolist()}")
# Extract and print the bounding boxes and labels
for result in results:
    boxes = result.boxes
    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get the bounding box coordinates
        confidence = box.conf[0]  # Get the confidence score
        cls = int(box.cls[0])  # Get the class index
        label = model.names[cls]  # Get the class label

        # Draw the bounding box and label on the image
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, f'{label} {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Show the image with detections
cv2.imshow('YOLOv8 Detection', img)
cv2.waitKey(0)
cv2.destroyAllWindows()