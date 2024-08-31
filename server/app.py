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
from fastapi.responses import JSONResponse

app = Flask(__name__)
CORS(app)

# Global variable to store task status
task_status = {
    'current_task': None,
    'status': 'idle'  # possible values: idle, running, completed, error
}

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
    car_address = config['car_address']
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
        image_utils.capture_frame(frame_type="object", frame_name=f'{object_name}')
    except requests.exceptions.RequestException as e:
        return str(e), 500
    return f'{object_name} object saved successfully', 200


@app.route("/camera/locating_any_objects", tags=["Car Endpoints"])
async def locate_and_align_object(object_label: str):
    if not object_label:
        raise HTTPException(status_code=400, detail="Missing 'object_label' parameter")

    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    with open('constants.yaml', 'r') as file:
        constants = yaml.safe_load(file)

    car_address = config['car_address']
    requests.get(f'http://{car_address}/ledon')
    detection_confidence = config['detection_confidence']
    detector = ObjectDetector()
    count = 0

    num_of_aligns = constants['num_of_aligns']
    max_search_attempts = constants['max_search_attempts']
    max_distance = constants['max_distance']
    min_distance = constants['min_distance']
    alignment_threshold = constants['alignment_threshold']
    min_distance_forward_delay = constants['min_distance_forward_delay']
    move_forward_delay = constants['move_forward_delay']
    align_left_right_delay = constants['align_left_right_delay']
    search_left_delay = constants['search_left_delay']
    half_circle_delay = constants['180_degree_turn_delay']

    def move_to_search_object():
        move_response = requests.get(f'http://{car_address}/manualDriving?dir=left&delay={search_left_delay}')  # Use move_forward_delay from constans
        if move_response.status_code != 200:
            print("Failed to move car to left for searching:", move_response.status_code)              
                
    def search_for_object():
        nonlocal count
        while count < max_search_attempts:  # Use max_search_attempts from constants
            count += 1
            try:
                cropped_img = image_utils.capture_frame(frame_type="stream", frame_name=f'{count}')
                results = detector.detect(cropped_img)

                if results:
                    for result in results:
                        label_result, confidence, x1, y1, x2, y2, line_length = result
                        print(f'Label result:{label_result}, Confidence:{confidence}, Line Length:{line_length}')
                        if confidence > detection_confidence and label_result == object_label:
                            centroid_x = (x1 + x2) // 2
                            return {'found': True, 'centroid_x': centroid_x, 'frame_width': cropped_img.shape[1], 'line_length': line_length}
                
                move_to_search_object()

            except requests.exceptions.RequestException as e:
                print("Error:", e)
                break

        return {'found': False}

    def calculate_delay(base_delay, line_length, min_distance):
        if line_length == 0:
            return base_delay
        # Calculate a factor between 0 and 1 based on how close the object is
        distance_factor = max(0, min(1, (line_length - min_distance) / line_length))
        # Calculate the adjusted delay
        return int(base_delay * distance_factor)

    def align_with_object(centroid_x, frame_width, line_length):
        frame_center = frame_width // 2
        
        if abs(centroid_x - frame_center) > frame_width * alignment_threshold:
            # Calculate the adjusted delay based on line_length
            adjusted_delay = calculate_delay(align_left_right_delay, line_length, min_distance)
            
            if centroid_x < frame_center:
                move_response = requests.get(f'http://{car_address}/manualDriving?dir=left&delay={adjusted_delay}')
            else:
                move_response = requests.get(f'http://{car_address}/manualDriving?dir=right&delay={adjusted_delay}')
            
            if move_response.status_code != 200:
                print(f"Failed to move car: {move_response.status_code}, Attempted delay: {adjusted_delay}")
                return {'aligned': False, 'line_length': line_length}
        
        return {'aligned': True, 'line_length': line_length}

    def move_towards_object(line_length):
        if line_length > min_distance:
            # Calculate move delay based on line_length
            adjusted_delay = calculate_delay(move_forward_delay, line_length, min_distance)
        else:
            # Use the minimum forward delay when at or below min_distance
            adjusted_delay = min_distance_forward_delay
        
        move_response = requests.get(f'http://{car_address}/manualDriving?dir=forward&delay={adjusted_delay}')
        if move_response.status_code != 200:
            print(f"Moving towards item - Failed to move car forward: {move_response.status_code}, Attempted delay: {adjusted_delay}")
        else:
            print(f"Moved forward with delay: {adjusted_delay}")
        
        return adjusted_delay  # Return the delay used for movement
    
    def search_after_movement():
        for _ in range(3):  # Try searching left, center, and right
            cropped_img = image_utils.capture_frame(frame_type="stream", frame_name=f'search_after_move')
            results = detector.detect(cropped_img)
            if results:
                for result in results:
                    label_result, confidence, x1, y1, x2, y2, line_length = result
                    print(f'Label result:{label_result}, Confidence:{confidence}, Line Length:{line_length}\n')
                    if confidence > detection_confidence and label_result == object_label:
                        return {
                            'found': True,
                            'centroid_x': (x1 + x2) // 2,
                            'frame_width': cropped_img.shape[1],
                            'line_length': line_length
                        }
            # If not found, move slightly to the right
            requests.get(f'http://{car_address}/manualDriving?dir=right&delay={align_left_right_delay}')
        return {'found': False} 
    
    def backward(line_length):
        adjusted_delay = calculate_delay(move_forward_delay, line_length, min_distance)
        move_response = requests.get(f'http://{car_address}/manualDriving?dir=backward&delay={adjusted_delay}')
        if move_response.status_code != 200:
            print(f"Failed to move car backward: {move_response.status_code}, Attempted delay: {adjusted_delay}")       
                
    def prepare_for_pick_up():
        move_response = requests.get(f'http://{car_address}/manualDriving?dir=left&delay={half_circle_delay}')  # Use align_left_right_delay from constants
        if move_response.status_code != 200:
                print("Failed to move car for a half of circle:", move_response.status_code)     
        move_response = requests.get(f'http://{car_address}/manualDriving?dir=backward&delay={min_distance_forward_delay}')  # Use move_forward_delay from constans
        if move_response.status_code != 200:
            print("Moving towards item - Failed to move car backward:", move_response.status_code)              

    try:
        search_result = search_for_object()
        if not search_result['found']:
            return JSONResponse(content={'found': False})

        if search_result['found']:
            while True:
                align_result = align_with_object(search_result['centroid_x'], search_result['frame_width'], search_result['line_length'])
                if align_result['aligned']:
                    moved_delay = move_towards_object(search_result['line_length'])
                    
                    # Search for the object after moving
                    new_search_result = search_after_movement()
                    if not new_search_result['found']:
                        print("Object lost after movement. Stopping.")
                        break
                    search_result = new_search_result
                    
                    # Check if we've reached the desired alignment and made the minimum movement
                    frame_center = search_result['frame_width'] // 2
                    print("centroid_x - frame_center: ", abs(search_result['centroid_x'] - frame_center))
                    print("Threshold: ", search_result['frame_width'] * alignment_threshold)
                    print("Moved Delay: ", moved_delay)
                    if (abs(search_result['centroid_x'] - frame_center) <= search_result['frame_width'] * alignment_threshold
                        and search_result['line_length'] <= min_distance):
                        prepare_for_pick_up()
                        print("Object reached, centered, and minimum forward movement made. Stopping movement.")
                        break
                else:
                    print("Alignment failed. Retrying.")

        return JSONResponse(content={**search_result, **align_result})
    finally:
        requests.get(f'http://{car_address}/ledoff')
     

@app.route('/task/status', methods=['GET'])
def get_task_status():
    return jsonify(task_status)

# ================================
# Main Execution
# ================================

if __name__ == '__main__':
    app.run(debug=True, port=8080)
