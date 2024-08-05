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
async def detect1_object(object_label: str):
    if not object_label:
        raise HTTPException(status_code=400, detail="Missing 'object_label' parameter")
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    car_address = config['car_address']
    requests.get(f'http://{car_address}/ledon')
    detection_confidence = config['detection_confidence']
    found = 0
    image_count = 0
    detector = ObjectDetector()
    count = 0
    while found != 2:
        print(count)
        count += 1
        try:
            cropped_img = image_utils.capture_frame(frame_type="stream", frame_name=f'{count}')
            print('Analyzing captured frame')
            results = detector.detect(cropped_img)
            print(results)
            if len(results) > 0:
                for result in results:
                    label_result, confidence, x1, y1, x2, y2, distance = result
                    print(label_result, confidence, distance)
                    if confidence > detection_confidence:
                        found = label_result == object_label
                        if not found:
                            continue
                        centroid_x = (x1 + x2) // 2
                        w = cropped_img.shape[1]
                        if found and distance < 100:
                            location = "middle"
                        elif centroid_x < w * 0.4:
                            location = "left"
                        elif centroid_x > w * 0.6:
                            location = "right"
                        else:
                            location = "middle"

                        if location == "left":
                            print("left")
                            move_response = requests.get(f'http://{car_address}/manualDriving?dir=left&delay={round(distance)}')
                            
                        elif location == "right":
                            print("right")
                            move_response = requests.get(f'http://{car_address}/manualDriving?dir=right&delay={round(distance)}')
                        else:
                            print("forward")
                            found = 2
                            move_response = requests.get(f'http://{car_address}/manualDriving?dir=forward&delay={500}')
                        if move_response.status_code != 200:
                            print("Failed to move car:", move_response.status_code)
                        image_count += 1
                        break
            if count == 20:
                break
            if found == 0:
                move_response = requests.get(f'http://{car_address}/manualDriving?dir=left&delay=200')

        except requests.exceptions.RequestException as e:
            requests.get(f'http://{car_address}/ledoff')
            print("Error:", e)
    requests.get(f'http://{car_address}/ledoff')
    return JSONResponse(content=f'found {found}')

# ================================
# Main Execution
# ================================

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
