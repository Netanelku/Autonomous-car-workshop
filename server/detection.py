import cv2
import numpy as np
import os
import glob
from ultralytics import YOLO

class ObjectLocalizer:
    def __init__(self, objects_path='objects'):
        self.sift = cv2.SIFT_create()
        self.image_collection = []
        image_pattern = os.path.join(objects_path, 'grayscale_*.jpg')
        image_files = glob.glob(image_pattern)
        
        for file in image_files:
            print(f'Reading {file}')
            image = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
            if image is not None:
                self.image_collection.append(image)
        print(f'Loaded {len(self.image_collection)} images from {objects_path}')

    def find_and_localize_object(self, query_image):
        # Detect keypoints and descriptors for the query image
        kp1, des1 = self.sift.detectAndCompute(query_image, None)

        # Initialize variables to store the best match
        best_match_index = -1
        best_match_score = 0

        # Set a threshold for match score
        threshold = 12  # Adjust as needed

        # Iterate through the image collection
        for i, img in enumerate(self.image_collection):
            # Detect keypoints and descriptors for the current image
            kp2, des2 = self.sift.detectAndCompute(img, None)

            # Create FLANN matcher
            FLANN_INDEX_KDTREE = 0
            index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
            search_params = dict(checks=50)
            flann = cv2.FlannBasedMatcher(index_params, search_params)

            # Match descriptors
            matches = flann.knnMatch(des1, des2, k=2)

            # Ratio test to find good matches
            good_matches = []
            for m, n in matches:
                if m.distance < 0.7 * n.distance:
                    good_matches.append(m)

            # Calculate the match score
            match_score = len(good_matches)

            # Print match score for each image
            print(f"Match score for image {i + 1}: {match_score}, Threshold: {threshold}, Best match score: {best_match_score}")

            # Update the best match if the current image has a higher number of good matches
            if match_score > best_match_score and match_score > threshold:
                best_match_score = match_score
                best_match_index = i

                # Store the best matches and keypoints for visualization
                best_matches = good_matches
                best_kp2 = kp2

        # If a suitable match is found, localize the object in the query image
        if best_match_index != -1:
            # Get keypoints coordinates of good matches
            train_pts = np.float32([best_kp2[m.trainIdx].pt for m in best_matches]).reshape(-1, 2)

            # Calculate the centroid of matched keypoints
            centroid = np.mean(train_pts, axis=0)
            # Get dimensions of the image
            h, w = query_image.shape[:2]
            # Calculate distance from centroid to center of the image
            center_image = (w // 2, h // 2)
            centroid_point = (int(centroid[0]), int(centroid[1]))
            distance_to_center = centroid_point[0] - center_image[0]
            
            # Determine the location of the centroid with respect to the center
            if distance_to_center < -w * 0.1:
                location = "left"
            elif distance_to_center > w * 0.1:
                location = "right"
            else:
                location = "middle"

            # Draw matches
            img_matches = cv2.drawMatches(query_image, kp1, self.image_collection[best_match_index], best_kp2, best_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

            # Draw the centroid point and the center of the image
            cv2.circle(img_matches, centroid_point, 5, (0, 255, 0), -1)
            cv2.circle(img_matches, center_image, 5, (255, 0, 0), -1)
            cv2.line(img_matches, center_image, centroid_point, (255, 0, 255), 2)

            # Add text annotations
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            color = (255, 255, 255)
            thickness = 1
            cv2.putText(img_matches, 'Centroid of Features', (centroid_point[0] + 10, centroid_point[1]), font, font_scale, color, thickness, cv2.LINE_AA)
            cv2.putText(img_matches, 'Center of Frame', (center_image[0] + 10, center_image[1]), font, font_scale, color, thickness, cv2.LINE_AA)
            
            # Annotate the distance
            mid_point = ((center_image[0] + centroid_point[0]) // 2, (center_image[1] + centroid_point[1]) // 2)
            cv2.putText(img_matches, f'{abs(distance_to_center):.2f}px', mid_point, font, font_scale, (255, 255, 0), thickness, cv2.LINE_AA)

            # Save the image with matches
            result_image_path = f'images/result_image_{best_match_index + 1}.jpg'
            os.makedirs('images', exist_ok=True)
            cv2.imwrite(result_image_path, img_matches)
            print(f"Result image saved as {result_image_path}")

            return {"best_match_index": best_match_index, "distance_to_center": distance_to_center, "location": location}

        else:
            print("No suitable match found.")
            return {"best_match_index": -1}


import cv2
from ultralytics import YOLO

import cv2
import math
from ultralytics import YOLO

class ObjectDetector:
    def __init__(self):
        self.model = YOLO('yolov8n.pt')
        self.counter = 0

    def detect(self, image):
        results = self.model(image)
        self.counter += 1
        return_value = []

        # Get image dimensions
        height, width, _ = image.shape
        # Calculate the center of the frame
        center_frame_x, center_frame_y = width // 2, height // 2

        # Draw the center point of the frame
        cv2.circle(image, (center_frame_x, center_frame_y), 5, (255, 0, 0), -1)

        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get the bounding box coordinates
                confidence = box.conf[0]  # Get the confidence score
                cls = int(box.cls[0])  # Get the class index
                label = self.model.names[cls]  # Get the class label

                # Calculate the center of the object
                center_object_x, center_object_y = (x1 + x2) // 2, (y1 + y2) // 2

                # Calculate the length of the line
                line_length = math.sqrt((center_frame_x - center_object_x) ** 2 + (center_frame_y - center_object_y) ** 2)

                return_value.append((label, confidence, x1, y1, x2, y2, line_length))

                # Draw the bounding box and label on the image
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(image, f'{label} {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Draw the center point of the object
                cv2.circle(image, (center_object_x, center_object_y), 5, (0, 0, 255), -1)

                # Draw a line between the center of the frame and the center of the object
                cv2.line(image, (center_frame_x, center_frame_y), (center_object_x, center_object_y), (255, 255, 0), 2)

                # Optionally, draw the line length on the image
                midpoint_x = (center_frame_x + center_object_x) // 2
                midpoint_y = (center_frame_y + center_object_y) // 2
                cv2.putText(image, f'{line_length:.2f}', (midpoint_x, midpoint_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # Save the image with drawn points and lines
        cv2.imwrite(f'images/results/result-{self.counter}.jpg', image)
        
        return return_value



# image_path='milk.jpg'
# A1=ObjectDetector()
# A1.detect(image_path)