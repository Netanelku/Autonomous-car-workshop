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
            task['event'] = latest_event_details
        else:
            task['event'] = "No events found"
        
        return JSONResponse(content=task)
    except Exception as e:
        return JSONResponse(content={'error': str(e)}, status_code=500)

# ================================
# Car Endpoints
# ================================

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

@app.get('/car/create_task', tags=['Main Operation'])
async def create_task_endpoint(target_object_id: str):
    """
    Endpoint to create a task for locating and aligning the target object.
    """
    # Load constants and config
    target_object_label = ""

    if target_object_id not in ['1', '2', '3']:
        return JSONResponse(content={'error': 'Invalid target_object_id'}, status_code=400)

    # Generate a unique task ID
    task_id = str(uuid.uuid4())
    if int(target_object_id) == 1:
        target_object_label = "can"
    elif int(target_object_id) == 2:
        target_object_label = "bottle"
    elif int(target_object_id) == 3:
        target_object_label = "deodorant"

    # Initialize the new task in tasks.yaml
    new_task = {
        'status': 'created',
        'object_label': target_object_label,
        'result': None,
        'repeats': '0/20',
        'percentage_complete': 0,
        'events': [
            {
                'action': 'task_created',
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'details': 'Task created for locating the object.',
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
    
    return JSONResponse(content={'status': 'task_created', 'task_id': task_id, 'target_object_label': target_object_label})

@app.get('/car/start_task', tags=['Main Operation'])
async def start_task_endpoint(task_id: str):
    """
    Endpoint to start the task for locating and aligning the target object.
    """
    try:
        # Load existing tasks
        with open('tasks.yaml', 'r') as file:
            tasks = yaml.safe_load(file) or {'tasks': {}}
        
        if task_id not in tasks['tasks']:
            return JSONResponse(content={'error': 'Task ID not found'}, status_code=404)

        # Retrieve the task information
        task = tasks['tasks'][task_id]
        if task['status'] != 'created':
            return JSONResponse(content={'error': 'Task is already started or completed'}, status_code=400)

        # Update task status to 'running'
        task['status'] = 'running'
        task['events'].append({
            'action': 'task_started',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'details': 'Task started for locating the object.',
            'attempt': 1
        })

        # Save updated tasks
        with open('tasks.yaml', 'w') as file:
            yaml.safe_dump(tasks, file)

        # Load constants and config
        config, constants = load_config()

        print(f"Starting task for locating the object: {task['object_label']}")
        # Locate and align the target object
        search_result = locate_and_align_object(task_id, task['object_label'], config, constants)
        if not search_result['found']:
            task['status'] = 'finish2'
            task['events'].append({
                'action': 'task_failed',
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'details': 'Failed to locate the target object.',
            })

            # Save the task with the failure status
            with open('tasks.yaml', 'w') as file:
                yaml.safe_dump(tasks, file)

            return JSONResponse(content={'found': False, 'task_id': task_id, 'status': 'failed'})

        # Locate and align the starting point
        starting_point_label = constants['starting_point_label']
        alignment_result = locate_and_align_object(task_id, starting_point_label, config, constants)

        if alignment_result['found']:
            # If successful, update the task status to 'success'
            task['status'] = 'finish1'
            task['events'].append({
                'action': 'task_completed',
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'details': 'Task completed successfully.',
            })
        else:
            # If not successful, update the task status to 'failed'
            task['status'] = 'finish2'
            task['events'].append({
                'action': 'task_failed',
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'details': 'Failed to align with the starting point.',
            })

        # Save updated tasks with the final status
        with open('tasks.yaml', 'w') as file:
            yaml.safe_dump(tasks, file)
        
        return JSONResponse(content={'status': task['status'], 'task_id': task_id, 'target_object_label': task['object_label']})
    
    except Exception as e:
        task['status'] = 'finish2'
        task['events'].append({
                'action': 'task_failed',
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'details': 'Failed to align with the starting point.',
            })

        # Save updated tasks with the final status
        with open('tasks.yaml', 'w') as file:
            yaml.safe_dump(tasks, file)
        return JSONResponse(content={'error': f'Failed to start task: {str(e)}'}, status_code=500)


# ================================
# Main Execution
# ================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",  # Replace "main" with the name of your script if it's different
        host="127.0.0.1",
        port=8080,
        workers=4,  # Number of worker processes
    )
