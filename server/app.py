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

@app.route('/camera/detection_car', methods=['POST'])
def detect1_object():
    try:
        response = requests.get('http://192.168.43.240/left')
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
                # Now you can process the image_np as needed

        else:
                print("Failed to retrieve image:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error:", e)
    result = find_and_localize_object(gray_image)
    
    #return result

def rotate_image(image, angle):
    # Get the dimensions of the image
    (h, w) = image.shape[:2]
    # Calculate the center of the image
    center = (w / 2, h / 2)
    
    # Get the rotation matrix
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    # Perform the rotation
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated

if __name__ == '__main__':
	# app.run(debug=True, port=8080)
    detect1_object()





