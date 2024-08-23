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

@app.route('/car/updateRetryAttempts', methods=['POST'])
def update_retry_attempts():
    new_attempts = request.json.get('retryAttempts')
    if new_attempts is None:
        return jsonify({'error': 'No retry attempts provided'}), 400

    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    config['retry_attempts'] = new_attempts

    with open('config.yaml', 'w') as file:
        yaml.safe_dump(config, file)

    return jsonify({'message': 'Retry attempts updated successfully', 'retryAttempts': new_attempts})


@app.route('/car/currentAddress', methods=['GET'])
def car_currentAddress():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    car_address = config['car_address']
    return jsonify({'current_ip': car_address})

@app.route('/car/updateAddress', methods=['POST'])
def car_updateAddress():
    new_ip = request.json.get('new_ip')
    if not new_ip:
        return jsonify({'error': 'No IP address provided'}), 400

    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    config['car_address'] = new_ip

    with open('config.yaml', 'w') as file:
        yaml.safe_dump(config, file)

    return jsonify({'message': 'IP address updated successfully', 'new_ip': new_ip})
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
    car_address=config['car_address']
    found = -1
    image_count = 0
    detector = ObjectDetector()
    count = 0
    while found == -1:
        print(count)
        count += 1
        try:
            cropped_img = image_utils.capture_frame(frame_type="stream",frame_name=f'{count}')
            print('analyzing captured frame')
            result = detector.detect(cropped_img)
            print(result)
            if count==20:
                break
            if found == -1:  
                move_response = requests.get(f'http://{car_address}/manualDriving?dir=left&delay=150')
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
