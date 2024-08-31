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
        return_value = None  # Initialize as None to store the closest object

        # Get image dimensions
        height, width, _ = image.shape
        # Calculate the center of the frame
        center_frame_x, center_frame_y = width // 2, height // 2

        # Draw the center point of the frame
        cv2.circle(image, (center_frame_x, center_frame_y), 5, (255, 0, 0), -1)

        min_line_length = float('inf')  # Initialize to infinity for comparison

        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get the bounding box coordinates
                confidence = box.conf[0]  # Get the confidence score
                cls = int(box.cls[0])  # Get the class index
                label = self.model.names[cls]  # Get the class label

                # Calculate the width and height of the bounding box
                box_width = x2 - x1
                box_height = y2 - y1

                # Check if the width is greater than the height
                if object_label != "board":
                    if box_width > box_height:
                        continue  # Skip this detection if width is greater than height

                # Calculate the center of the object
                center_object_x = (x1 + x2) // 2
                center_object_y = y2  # The bottom center of the object

                # Calculate the length of the line from the bottom center of the object to the bottom of the image
                bottom_center_x, bottom_center_y = center_object_x, height
                line_length = math.sqrt((center_object_x - bottom_center_x) ** 2 + (center_object_y - bottom_center_y) ** 2)

                # Keep track of the object with the smallest line_length
                if line_length < min_line_length:
                    min_line_length = line_length
                    return_value = (label, confidence, x1, y1, x2, y2, line_length)

        # Draw the closest object on the image
        if return_value:
            label, confidence, x1, y1, x2, y2, line_length = return_value
            
            # Draw the bounding box and label on the image
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, f'{label} {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Draw the center point of the object
            center_object_x = (x1 + x2) // 2
            center_object_y = y2
            cv2.circle(image, (center_object_x, center_object_y), 5, (0, 0, 255), -1)

            # Draw a line from the bottom center of the object to the bottom of the image
            cv2.line(image, (center_object_x, center_object_y), (center_object_x, height), (0, 255, 255), 2)

            # Optionally, draw the line length on the image
            midpoint_x = (center_object_x + bottom_center_x) // 2
            midpoint_y = (center_object_y + bottom_center_y) // 2
            cv2.putText(image, f'{line_length:.2f}', (midpoint_x, midpoint_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # Ensure the 'results' directory exists
        results_dir = 'images/results'
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        # Save the image with drawn points and lines
        result_image_path = os.path.join(results_dir, f'result-{self.counter}.jpg')
        cv2.imwrite(result_image_path, image)
        if os.path.exists(result_image_path):
            print(f'Image successfully saved to {result_image_path}')
        else:
            print(f'Failed to save image to {result_image_path}')
        
        # Return the closest detected object
        return [return_value] if return_value else []
