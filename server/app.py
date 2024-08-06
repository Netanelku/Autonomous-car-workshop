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
    car_address = config['car_address']
    requests.get(f'http://{car_address}/ledon')
    detection_confidence = config['detection_confidence']
    detector = ObjectDetector()
    count = 0

    def search_for_object():
        nonlocal count
        while count < 20:  # Limit to 20 attempts
            count += 1
            try:
                cropped_img = image_utils.capture_frame(frame_type="stream", frame_name=f'{count}')
                results = detector.detect(cropped_img)

                if results:
                    for result in results:
                        label_result, confidence, x1, y1, x2, y2, distance = result
                        print(f'Label result:{label_result}, Confidence:{confidence}, Distance:{distance}')
                        if confidence > detection_confidence and label_result == object_label:
                            centroid_x = (x1 + x2) // 2
                            return {'found': True, 'centroid_x': centroid_x, 'frame_width': cropped_img.shape[1], 'distance': distance}
                
                move_response = requests.get(f'http://{car_address}/manualDriving?dir=left&delay=200')
                if move_response.status_code != 200:
                    print("Failed to move car:", move_response.status_code)

            except requests.exceptions.RequestException as e:
                print("Error:", e)
                break

        return {'found': False}

    def align_with_object(centroid_x, frame_width, distance):
        count = 0
        while (distance) > 50 and count < 3:  # Adjust the threshold as necessary
            if centroid_x < frame_width * 0.4:
                move_response = requests.get(f'http://{car_address}/manualDriving?dir=left&delay=50')
            elif centroid_x > frame_width * 0.6:
                move_response = requests.get(f'http://{car_address}/manualDriving?dir=right&delay=50')
            else:
                if move_response.status_code != 200:
                    print("Failed to move car:", move_response.status_code)
                break

            # Capture a new frame and re-calculate the centroid
            cropped_img = image_utils.capture_frame(frame_type="stream")
            results = detector.detect(cropped_img)
            if results:
                for result in results:
                    label_result, confidence, x1, y1, x2, y2, distance = result
                    print(f'Label result:{label_result}, Confidence:{confidence}, Distance:{distance}')
                    if confidence > config['detection_confidence']:
                        centroid_x = (x1 + x2) // 2
            count+=1
            
        return {'aligned': True}

    def move_towards_object(distance):
        if distance < 100:
            move_response = requests.get(f'http://{car_address}/manualDriving?dir=forward&delay=500')
            if move_response.status_code != 200:
                print("Failed to move car forward:", move_response.status_code)

    try:
        search_result = search_for_object()
        if not search_result['found']:
            return JSONResponse(content={'found': False})

        align_result = align_with_object(search_result['centroid_x'], search_result['frame_width'], search_result['distance'])
        if align_result['aligned']:
            move_towards_object(search_result['distance'])

        return JSONResponse(content={**search_result, **align_result})
    finally:
        requests.get(f'http://{car_address}/ledoff')






# ================================
# Main Execution
# ================================

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)