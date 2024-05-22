# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, request
from flask_cors import CORS
from detection import find_and_localize_object
import cv2
import json
import numpy as np
import requests
from matplotlib import pyplot as plt
import os
import time
# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def readme():
    with open('./readme.txt', 'r') as file:
        readme_content = file.read()
    return readme_content

@app.route('/health',methods=[ 'GET'])
def test():
	return 'TEST endpoint'

@app.route('/car/health' ,methods=[ 'GET'])
def car_health():
    pass

@app.route('/car/motion/start' ,methods=[ 'GET'])
def car_motion_start():
    pass

@app.route('/car/motion/stop' ,methods=[ 'GET'])
def car_motion_stop():
    pass

@app.route('/camera/detection_comp' ,methods=[ 'GET'])
def detect_object():
    return find_and_localize_object(cv2.imread('check.jpg',0))

@app.route('/camera/locating_any_objects', methods=['GET'])
def detect1_object(save_path='images'):
    found = -1
    image_count = 0

    # Ensure the save directory exists
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    while found == -1:
        try:
            response = requests.get('http://10.0.0.11/left')
            
            if response.status_code == 200:
                # Retrieve image data as bytes
                image_data = response.content
                
                # Decode image data using OpenCV
                image_np = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
                

                
                # Rotate the image
                angle = -90  # You can change this angle as needed
                rotated_image = rotate_image(image_np, angle)

                # Convert the rotated image to grayscale
                gray_image = cv2.cvtColor(rotated_image, cv2.COLOR_BGR2GRAY)
                
                # Save the grayscale image
                grayscale_image_path = os.path.join(save_path, f'grayscale_{image_count}.jpg')
                cv2.imwrite(grayscale_image_path, gray_image)
                
                # Process the image to find and localize the object
                result = find_and_localize_object(gray_image)
                found = result["best_match_index"]
                
                # If the object is not found, send a request to move the camera
                if found == -1:  
                    move_response = requests.get('http://10.0.0.11/go?dir=left&delay=300')
                    time.sleep(0.5)
                    if move_response.status_code != 200:
                        print("Failed to move camera:", move_response.status_code)
                
                image_count += 1
            else:
                print("Failed to retrieve image:", response.status_code)
        
        except requests.exceptions.RequestException as e:
            print("Error:", e)
    
    return f'found {found}'
def rotate_image(image, angle):
    # Get the dimensions of the image
    (h, w) = image.shape[:2]
    # Calculate the center of the image
    center = (w / 2, h / 2)
    
    # Get the rotation matrix
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    # Calculate the sine and cosine of the angle
    abs_cos = abs(M[0, 0])
    abs_sin = abs(M[0, 1])
    
    # Compute the new bounding dimensions of the image
    new_w = int(h * abs_sin + w * abs_cos)
    new_h = int(h * abs_cos + w * abs_sin)
    
    # Adjust the rotation matrix to account for the new dimensions
    M[0, 2] += (new_w / 2) - center[0]
    M[1, 2] += (new_h / 2) - center[1]
    
    # Perform the rotation
    rotated = cv2.warpAffine(image, M, (new_w, new_h), borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
    return rotated

if __name__ == '__main__':
	app.run(debug=True, port=8080)
    # detect1_object()





