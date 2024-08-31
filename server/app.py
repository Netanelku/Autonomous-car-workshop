from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from object_detector import ObjectDetector
import cv2
import json
import requests
import os
import time
import image_utils
import yaml
from datetime import datetime
from utils import load_config
from process_utils import locate_and_align_object
import uuid  # Import uuid for generating unique task IDs
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================================
# UI Endpoints
# ================================

@app.get('/', response_class=HTMLResponse, tags=['UI'])
def readme():
    """
    Endpoint to serve the README file content as HTML.
    """
    readme_file_path = './readme.html'  # Assuming the README file is now in HTML format
    if not os.path.exists(readme_file_path):
        return HTMLResponse(content="<h1>README file not found</h1>", status_code=404)

    with open(readme_file_path, 'r') as file:
        readme_content = file.read()

    return HTMLResponse(content=readme_content)

@app.post('/car/updateRetryAttempts', tags=['Car Configuration'])
async def update_retry_attempts(request: Request):
    """
    Endpoint to update the retry attempts in the car configuration.
    """
    try:
        new_attempts = await request.json()  # Await the JSON data
        retry_attempts = new_attempts.get('retryAttempts')
        
        if retry_attempts is None:
            return JSONResponse(content={'error': 'No retry attempts provided'}, status_code=400)

        # Read the existing configuration
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)

        # Update the retry_attempts
        config['retry_attempts'] = retry_attempts

        # Write the updated configuration back to the file
        with open('config.yaml', 'w') as file:
            yaml.safe_dump(config, file)

        return JSONResponse(content={'message': 'Retry attempts updated successfully', 'retryAttempts': retry_attempts})
    except Exception as e:
        return JSONResponse(content={'error': str(e)}, status_code=500)

@app.get('/car/currentAddress', tags=['Car Configuration'])
def car_current_address():
    """
    Endpoint to get the current IP address of the car.
    """
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    car_address = config['car_address']
    return JSONResponse(content={'current_ip': car_address})

@app.post('/car/updateAddress', tags=['Car Configuration'])
async def car_update_address(request: Request):
    """
    Endpoint to update the IP address of the car.
    """
    try:
        # Await the JSON data
        data = await request.json()
        new_ip = data.get('new_ip')
        
        if not new_ip:
            return JSONResponse(content={'error': 'No IP address provided'}, status_code=400)

        # Read the existing configuration
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)

        # Update the car_address
        config['car_address'] = new_ip

        # Write the updated configuration back to the file
        with open('config.yaml', 'w') as file:
            yaml.safe_dump(config, file)

        return JSONResponse(content={'message': 'IP address updated successfully', 'new_ip': new_ip})
    except Exception as e:
        return JSONResponse(content={'error': str(e)}, status_code=500)


def get_latest_event(events):
    """
    Get the latest event details based on the timestamp.
    """
    latest_event = max(events, key=lambda e: datetime.fromisoformat(e['timestamp'].replace('Z', '+00:00')))
    return latest_event['details']

@app.get('/task/status/{task_id}', tags=['Task Management'])
def get_task_status(task_id: str):
    """
    Endpoint to get the status of a specific task by its ID.
    """
    try:
        with open('tasks.yaml', 'r') as file:
            tasks = yaml.safe_load(file)
        
        if 'tasks' not in tasks:
            raise HTTPException(status_code=500, detail="Tasks not found in YAML file")
        
        task = tasks['tasks'].get(task_id)
        
        if not task:
            raise HTTPException(status_code=404, detail="Task ID not found")
        
        # Update the status to the latest event description
        if 'events' in task and task['events']:
            latest_event_details = get_latest_event(task['events'])
            task['status'] = latest_event_details
        else:
            task['status'] = "No events found"
        
        return JSONResponse(content=task)
    except Exception as e:
        return JSONResponse(content={'error': str(e)}, status_code=500)

# ================================
# Car Endpoints
# ================================

def update_task_status(task_id: str, status: str, percentage: int, object_label: str = None, result: str = None):
    """
    Updates the status of a specific task.
    """
    try:
        # Load existing tasks
        with open('tasks.yaml', 'r') as file:
            tasks = yaml.safe_load(file)

        if 'tasks' not in tasks:
            tasks['tasks'] = {}

        # Update task status
        tasks['tasks'][task_id] = {
            'status': status,
            'object_label': object_label,
            'result': result,
            'percentage': percentage,
            'retry_attempts': tasks['tasks'].get(task_id, {}).get('retry_attempts', 0)  # Keep existing retry attempts
        }

        # Save updated tasks
        with open('tasks.yaml', 'w') as file:
            yaml.safe_dump(tasks, file)

    except Exception as e:
        print(f"Error updating task status: {e}")

@app.get('/health', tags=['Health Check'])
def health_check():
    """
    Endpoint to check the health of the car server.
    """
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
        return JSONResponse(content={'status': 'error', 'message': str(e)}, status_code=500)

@app.get('/camera/save_object', tags=['Camera Operations'])
def save_object(name: str):
    """
    Endpoint to save an image of the specified object.
    """
    if not name:
        raise HTTPException(status_code=400, detail="Missing 'name' parameter")
    try:
        image_utils.capture_frame(frame_type="object", frame_name=name)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return PlainTextResponse(content=f'{name} object saved successfully', status_code=200)

@app.get('/camera/locating_any_objects', tags=['Main Operation'])
async def locate_and_align_object_endpoint(target_object_id: str):
    """
    Endpoint to locate and align the target object, and then locate the starting point.
    """
    # Load constants and config
    config, constants = load_config()
    target_object_label=""
    if target_object_id not in ['1', '2', '3']:
        return JSONResponse(content={'error': 'Invalid target_object_id'}, status_code=400)

    # Generate a unique task ID
    task_id = str(uuid.uuid4())
    if int(target_object_id)==1:
        target_object_label="can"
    elif int(target_object_id)==2:
        target_object_label="bottle"
    elif int(target_object_id)==3:
        target_object_label="deodorant"
    # Initialize the new task in tasks.yaml
    new_task = {
        'status': 'running',
        'object_label': target_object_label,
        'result': None,
        'repeats': '0/20',
        'percentage_complete': 0,
        'events': [
            {
                'action': 'started_search',
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'details': 'Started looking for the object.',
                'attempt': 1
            }
        ]
    }
    
    try:
        # Load existing tasks
        with open('tasks.yaml', 'r') as file:
            tasks = yaml.safe_load(file) or {'tasks': {}}

        # Add new task
        tasks['tasks'][task_id] = new_task

        # Save updated tasks
        with open('tasks.yaml', 'w') as file:
            yaml.safe_dump(tasks, file)

    except Exception as e:
        return JSONResponse(content={'error': f'Failed to create task: {str(e)}'}, status_code=500)
    
    # # Locate and align the target object
    # search_result = locate_and_align_object(task_id, target_object_label, config, constants)
    # if not search_result['found']:
    #     return JSONResponse(content={'found': False, 'task_id': task_id})

    # # Locate and align the starting point
    # starting_point_label = constants['starting_point_label']
    # locate_and_align_object(task_id, starting_point_label, config, constants)

    return JSONResponse(content={'status': 'started', 'task_id': task_id, 'target_object_label': target_object_label})

# ================================
# Main Execution
# ================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
