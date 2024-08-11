from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from detection import ObjectDetector
import cv2
import json
import requests
import os
import time
import image_utils
import yaml
import uvicorn
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================================
# UI Endpoints
# ================================

@app.get("/", response_class=PlainTextResponse, tags=["UI Endpoints"])
async def readme():
    with open('./readme.txt', 'r') as file:
        readme_content = file.read()
    return readme_content

@app.get("/car/health", tags=["UI Endpoints"])
async def car_health():
    pass

@app.get("/car/motion/start", tags=["UI Endpoints"])
async def car_motion_start():
    pass

@app.get("/car/motion/stop", tags=["UI Endpoints"])
async def car_motion_stop():
    pass

# ================================
# Car Endpoints
# ================================

@app.get("/health", tags=["Car Endpoints"])
async def health_check():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    car_address = config['car_address']
    car_server_url = f'http://{car_address}/'
    try:
        response = requests.get(car_server_url)
        if response.status_code == 200:
            return JSONResponse(content={'status': 'ok', 'message': 'Car server is live'}, status_code=200)
        else:
            return JSONResponse(content={'status': 'error', 'message': 'Car server is not reachable'}, status_code=response.status_code)
    except requests.exceptions.RequestException as e:
        return JSONResponse(content={'status': 'error', 'message': 'Car server is not reachable'}, status_code=500)

# @app.get("/camera/detection_comp", tags=["Car Endpoints"])
# async def detect_object():
#     localizer = ObjectDetector()
#     query_image_path = 'check.jpg'
#     query_image = cv2.imread(query_image_path, cv2.IMREAD_GRAYSCALE)
#     if query_image is None:
#         raise HTTPException(status_code=400, detail=f"Error reading query image: {query_image_path}")
#     result = localizer.find_and_localize_object(query_image)
#     return JSONResponse(content=result)

@app.get("/camera/save_object", tags=["Car Endpoints"])
async def save_object(name: str):
    if not name:
        raise HTTPException(status_code=400, detail="Missing 'name' parameter")
     
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    car_address = config['car_address']
    try:
        requests.get(f'http://{car_address}/ledon')
        time.sleep(2)
        image_utils.capture_frame(frame_type="object", frame_name=f'{name}')
        requests.get(f'http://{car_address}/ledoff')
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return JSONResponse(content=f'{name} object saved successfully', status_code=200)


@app.get("/camera/locating_any_objects", tags=["Car Endpoints"])
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
            move_response = requests.get(f'http://{car_address}/manualDriving?dir=forward&delay={adjusted_delay}')
            if move_response.status_code != 200:
                print(f"Moving towards item - Failed to move car forward: {move_response.status_code}, Attempted delay: {adjusted_delay}")
        else:
            print("Object is within min_distance, no forward movement needed.") 
    
    def search_after_movement():
        for _ in range(3):  # Try searching left, center, and right
            cropped_img = image_utils.capture_frame(frame_type="stream", frame_name=f'search_after_move')
            results = detector.detect(cropped_img)
            if results:
                for result in results:
                    label_result, confidence, x1, y1, x2, y2, line_length = result
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
    
    def move_backwards(line_length):
        adjusted_delay = calculate_delay(move_forward_delay, line_length, min_distance)
        move_response = requests.get(f'http://{car_address}/manualDriving?dir=backward&delay={adjusted_delay}')
        if move_response.status_code != 200:
            print(f"Failed to move car backward: {move_response.status_code}, Attempted delay: {adjusted_delay}")       
                
    def move_returning_object(numOfAligns):
        move_response = requests.get(f'http://{car_address}/manualDriving?dir=left&delay={half_circle_delay}')  # Use align_left_right_delay from constants
        if move_response.status_code != 200:
                print("Failed to move car for a half of circle:", move_response.status_code)
        while numOfAligns > 0:
            numOfAligns -= 1
            move_response = requests.get(f'http://{car_address}/manualDriving?dir=forward&delay={move_forward_delay}')  # Use move_forward_delay from constans
            if move_response.status_code != 200:
                print("Moving towards item - Failed to move car forward:", move_response.status_code)              

    try:
        search_result = search_for_object()
        if not search_result['found']:
            return JSONResponse(content={'found': False})

        if search_result['found']:
            while True:
                align_result = align_with_object(search_result['centroid_x'], search_result['frame_width'], search_result['line_length'])
                if align_result['aligned']:
                    if align_result['line_length'] > min_distance:
                        move_towards_object(search_result['line_length'])
                        
                        # Search for the object after moving
                        new_search_result = search_after_movement()
                        if not new_search_result['found']:
                            print("Object lost after movement. Stopping.")
                            break
                        search_result = new_search_result
                    else:
                        print("Object reached minimum distance.")
                        break
                        
                    # Check if we've reached the desired distance and alignment
                    frame_center = search_result['frame_width'] // 2
                    if (search_result['line_length'] <= min_distance and 
                        abs(search_result['centroid_x'] - frame_center) <= search_result['frame_width'] * alignment_threshold):
                        print("Object reached, centered, and within minimum distance. Stopping movement.")
                        break
                else:
                    print("Alignment failed. Retrying.")

        return JSONResponse(content={**search_result, **align_result})
    finally:
        requests.get(f'http://{car_address}/ledoff')
               


# ================================
# Main Execution
# ================================

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)