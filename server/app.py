# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, request
from flask_cors import CORS
from detection import find_and_localize_object
import cv2
import json
import numpy as np

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
    return find_and_localize_object(cv2.imread('query.jpeg',0))

@app.route('/camera/detection_car', methods=['POST'])
def detect1_object():
    if 'image' not in request.files:
        return "No image provided", 400
    image_file = request.files['image']
    image_np = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
    result = find_and_localize_object(image_np)
    
    return result
if __name__ == '__main__':
	app.run(debug=True, port=8080)





