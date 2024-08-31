import numpy as np
import os
from ultralytics import YOLO
import cv2
import math

class ObjectDetector:
    def __init__(self):
        self.model = YOLO('updateWeights.pt')
        self.counter = 0

    def detect(self, image, object_label):
        results = self.model(image)
        self.counter += 1
        return_value = None

        height, width, _ = image.shape
        center_frame_x, center_frame_y = width // 2, height // 2
        cv2.circle(image, (center_frame_x, center_frame_y), 5, (255, 0, 0), -1)

        min_line_length = float('inf')

        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = box.conf[0]
                cls = int(box.cls[0])
                label = self.model.names[cls]

                box_width = x2 - x1
                box_height = y2 - y1

                if object_label != "Start" and box_width > box_height:
                    continue

                center_object_x = (x1 + x2) // 2
                center_object_y = y2
                bottom_center_x, bottom_center_y = center_object_x, height
                line_length = math.sqrt((center_object_x - bottom_center_x) ** 2 + (center_object_y - bottom_center_y) ** 2)

                if line_length < min_line_length:
                    min_line_length = line_length
                    return_value = (label, confidence, x1, y1, x2, y2, line_length)

        if return_value:
            label, confidence, x1, y1, x2, y2, line_length = return_value
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, f'{label} {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            center_object_x = (x1 + x2) // 2
            center_object_y = y2
            cv2.circle(image, (center_object_x, center_object_y), 5, (0, 0, 255), -1)
            cv2.line(image, (center_object_x, center_object_y), (center_object_x, height), (0, 255, 255), 2)

        # Create subfolder for each object label
        results_dir = os.path.join('images/results', object_label)
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        result_image_path = os.path.join(results_dir, f'result-{self.counter}.jpg')
        cv2.imwrite(result_image_path, image)
        
        if os.path.exists(result_image_path):
            print(f'Image successfully saved to {result_image_path}')
        else:
            print(f'Failed to save image to {result_image_path}')
        
        return [return_value] if return_value else []
