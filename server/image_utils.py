import cv2
import requests
import yaml
import os
import time
import numpy as np
from datetime import datetime

def rotate_image(image, angle=90):
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    abs_cos = abs(M[0, 0])
    abs_sin = abs(M[0, 1])
    new_w = int(h * abs_sin + w * abs_cos)
    new_h = int(h * abs_cos + w * abs_sin)
    M[0, 2] += (new_w / 2) - center[0]
    M[1, 2] += (new_h / 2) - center[1]
    rotated = cv2.warpAffine(image, M, (new_w, new_h), borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
    return rotated

def capture_frame(frame_type,frame_name=""):
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    if frame_type == "stream":
        image_filename = f'{frame_type}_frame_{frame_name} {formatted_time}.jpg'
        save_directory = config['image_paths']['stream_path']
    else:
        image_filename = f'object_{frame_name}.jpg'
        save_directory = config['image_paths']['objects_path']

    car_address = config['car_address']
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    print('Fetching image from car address...')
    try: 
        requests.get(f'http://{car_address}/ledon')
        time.sleep(2)
        response = requests.get(f'http://{car_address}/left')
        requests.get(f'http://{car_address}/ledoff')
        print('image fetched')
        if response.status_code == 200:
            image_data = response.content
            image_np = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
            if image_np is not None:
                    print('Image successfully fetched and decoded.')         
                    rotated_image = rotate_image(image_np)
                    gray_image = cv2.cvtColor(rotated_image, cv2.COLOR_BGR2GRAY)        
                    image_path = os.path.join(save_directory,image_filename)
                    # height, width = gray_image.shape[:2]
                    # new_height = int(height * 0.4)
                    # cropped_img = gray_image[new_height:height, 0:width]
                    cv2.imwrite(image_path, gray_image)
                    if os.path.exists(image_path):
                        print(f'Image successfully saved to {image_path}')
                    else:
                        print(f'Failed to save image to {image_path}')
                    return cropped_img
            else:
                print('Error: Decoded image is None.')
        else:
            print(f'Error fetching image. Status code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print("Request error:", e)
    except Exception as e:
        print("Unexpected error:", e)

    return None
