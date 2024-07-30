from flask import Flask, request, jsonify
from flask_cors import CORS
from detection import ObjectDetector
import cv2
import json
import requests
import os
import time
import image_utils
import yaml
app = Flask(__name__)
CORS(app)


# ================================
# UI Endpoints
# ================================

@app.route('/', methods=['GET'])
def readme():
    with open('./readme.txt', 'r') as file:
        readme_content = file.read()
    return readme_content

@app.route('/car/health', methods=['GET'])
def car_health():
    pass

@app.route('/car/motion/start', methods=['GET'])
def car_motion_start():
    pass

@app.route('/car/motion/stop', methods=['GET'])
def car_motion_stop():
    pass

# ================================
# Car Endpoints
# ================================
@app.route('/health', methods=['GET'])
def health_check():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    car_address=config['car_address']
    car_server_url = f'http://{car_address}/'
    try:
        response = requests.get(car_server_url)
        if response.status_code == 200:
            return jsonify({'status': 'ok', 'message': 'Car server is live'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Car server is not reachable'}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
@app.route('/camera/detection_comp', methods=['GET'])
def detect_object():
    localizer = ObjectDetector()
    query_image_path = 'check.jpg'
    query_image = cv2.imread(query_image_path, cv2.IMREAD_GRAYSCALE)
    if query_image is None:
        return f"Error reading query image: {query_image_path}", 400
    result = localizer.find_and_localize_object(query_image)
    return json.dumps(result)

@app.route('/camera/save_object', methods=['GET'])
def save_object():
    object_name = request.args.get('name')
    if not object_name:
        return "Missing 'name' parameter", 400
    try:
        image_utils.capture_frame(frame_type="object",frame_name=f'{object_name}')
    except requests.exceptions.RequestException as e:
        return str(e), 500
    return f'{object_name} object saved successfully', 200
    
@app.route('/camera/locating_any_objects', methods=['GET'])
def detect1_object():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    car_address = config['car_address']
    found = -1
    image_count = 0
    detector = ObjectDetector()
    count = 0
    while found == -1:
        print(count)
        count += 1
        try:
            cropped_img = image_utils.capture_frame(frame_type="stream", frame_name=f'{count}')
            print('Analyzing captured frame')
            results = detector.detect(cropped_img)
            print(results)
            if count == 20:
                break

            for result in results:
                label, confidence, x1, y1, x2, y2 = result
                if confidence > 0.5:  # Adjust the confidence threshold as needed
                    found = 1
                    # Calculate the centroid of the bounding box
                    centroid_x = (x1 + x2) // 2
                    w = cropped_img.shape[1]
                    # Determine the location of the centroid with respect to the center
                    if centroid_x < w * 0.4:
                        location = "left"
                    elif centroid_x > w * 0.6:
                        location = "right"
                    else:
                        location = "middle"

                    if location == "left":
                        move_response = requests.get(f'http://{car_address}/manualDriving?dir=left&delay=150')
                    elif location == "right":
                        move_response = requests.get(f'http://{car_address}/manualDriving?dir=right&delay=150')
                    else:
                        move_response = requests.get(f'http://{car_address}/manualDriving?dir=forward&delay=150')

                    if move_response.status_code != 200:
                        print("Failed to move car:", move_response.status_code)

                    image_count += 1
                    break
        except requests.exceptions.RequestException as e:
            print("Error:", e)

    return f'found {found}'


# ================================
# Main Execution
# ================================

if __name__ == '__main__':
    app.run(debug=True, port=8080)
