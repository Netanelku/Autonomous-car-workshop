from flask import Flask, request
from flask_cors import CORS
from detection import ObjectLocalizer
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

@app.route('/health', methods=['GET'])
def test():
    return 'TEST endpoint'

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

@app.route('/camera/detection_comp', methods=['GET'])
def detect_object():
    localizer = ObjectLocalizer()
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
        image_utils.capture_frame(frame_type="object",frame_name={object_name})
    except requests.exceptions.RequestException as e:
        return str(e), 500

    return f'{object_name} object saved successfully', 200
    
@app.route('/camera/locating_any_objects', methods=['GET'])
def detect1_object(save_path='images'):
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    car_address=config['car_address']
    found = -1
    image_count = 0
    localizer = ObjectLocalizer()
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    count = 0
    while found == -1:
        print(count)
        count += 1
        try:
            cropped_img = image_utils.capture_frame(frame_type="stream",frame_name=f'{count}')
            print('analyzing captured frame')
            result = localizer.find_and_localize_object(cropped_img)
            found = result["best_match_index"]
            if found == -1:  
                move_response = requests.get(f'http://{car_address}/manualDriving?dir=left&delay=450')
                time.sleep(0.5)
                if move_response.status_code != 200:
                    print("Failed to move camera:", move_response.status_code)
                image_count += 1
        except requests.exceptions.RequestException as e:
            print("Error:", e)
    return f'found {found}'

# ================================
# Main Execution
# ================================

if __name__ == '__main__':
    app.run(debug=True, port=8080)
