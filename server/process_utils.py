import requests
import image_utils
from object_detector import ObjectDetector
import yaml
import time
from datetime import datetime


def update_task_status(task_id: str, status: str, percentage: int, object_label: str = None, result: str = None):
    try:
        with open('tasks.yaml', 'r') as file:
            tasks = yaml.safe_load(file)
        if 'tasks' not in tasks:
            tasks['tasks'] = {}
        
        # Retrieve existing task or create a new one if it doesn't exist
        task = tasks['tasks'].get(task_id, {
            'status': status,
            'object_label': object_label,
            'result': result,
            'percentage_complete': 0,
            'repeats': '0/20',
            'events': []
        })

        # Update task details
        task['status'] = status
        task['object_label'] = object_label if object_label else task.get('object_label')
        task['result'] = result
        task['percentage_complete'] = task.get('percentage_complete', 0) + percentage

        # Add an event to the task
        event = {
            'action': status,
            'details': result if result else 'Status updated',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'attempt': task.get('repeats', '0/20').split('/')[0]
        }
        task['events'].append(event)

        # Save the updated task
        tasks['tasks'][task_id] = task
        with open('tasks.yaml', 'w') as file:
            yaml.safe_dump(tasks, file)
    except Exception as e:
        print(f"Error updating task status: {e}")

def locate_and_align_object(task_id, object_label, config, constants):
    car_address = config['car_address']
    detection_confidence = constants['objects_confidence'][object_label]
    detector = ObjectDetector()
    count = 0
    num_of_aligns = constants['num_of_aligns']
    num_of_divisions_for_backward_delay = constants['num_of_divisions_for_backward_delay']
    max_search_attempts = constants['max_search_attempts']
    min_distance = constants['min_distance']
    alignment_threshold = constants['alignment_threshold']
    min_distance_forward_delay = constants['min_distance_forward_delay']
    move_forward_delay = constants['move_forward_delay']
    align_left_right_delay = constants['align_left_right_delay']
    align_right_before_forward_delay = constants['align_right_before_forward_delay']
    extra_turn_left_delay = constants['extra_turn_left_delay'][object_label]
    search_left_delay = constants['search_left_delay']
    half_circle_delay = constants['180_degree_turn_delay']
    starting_point_label = constants['starting_point_label']

    def move_to_search_object():
        response = requests.get(f'http://{car_address}/manualDriving?dir=left&delay={search_left_delay}')
        if response.status_code != 200:
            print("Failed to move car left for searching:", response.status_code)

    def search_for_object():
        nonlocal count
        while count < max_search_attempts:
            count += 1
            try:
                cropped_img = image_utils.capture_frame(frame_type="stream", frame_name=f'{count}')
                results = detector.detect(cropped_img, object_label)
                if results:
                    for result in results:
                        label_result, confidence, x1, y1, x2, y2, line_length = result
                        if confidence > detection_confidence and label_result == object_label:
                            centroid_x = (x1 + x2) // 2
                            return {'found': True, 'centroid_x': centroid_x, 'frame_width': cropped_img.shape[1], 'line_length': line_length}
                move_to_search_object()
            except requests.exceptions.RequestException as e:
                print("Error:", e)
                break
        return {'found': False}

    def calculate_delay(base_delay, line_length):
        if line_length == 0:
            return base_delay
        distance_factor = max(0, min(1, (line_length - min_distance) / line_length))
        return int(base_delay * distance_factor)

    def align_with_object(centroid_x, frame_width, line_length):
        frame_center = frame_width // 2
        if abs(centroid_x - frame_center) > frame_width * alignment_threshold:
            adjusted_delay = calculate_delay(align_left_right_delay, line_length)
            direction = 'left' if centroid_x < frame_center else 'right'
            response = requests.get(f'http://{car_address}/manualDriving?dir={direction}&delay={adjusted_delay}')
            if response.status_code != 200:
                print(f"Failed to move car {direction}: {response.status_code}, Attempted delay: {adjusted_delay}")
                return {'aligned': False, 'line_length': line_length}
        return {'aligned': True, 'line_length': line_length}

    def move_towards_object(line_length):
        adjusted_delay = calculate_delay(move_forward_delay, line_length) if line_length > min_distance else min_distance_forward_delay
        move_response = requests.get(f'http://{car_address}/manualDriving?dir=right&delay={align_right_before_forward_delay}')
        if move_response.status_code != 200:
            print(f"Moving towards item - Failed to align car to the right: {move_response.status_code}, Attempted delay: {align_right_before_forward_delay}")
        else:
            print(f"Moving towards item - Moved to the right with delay: {align_right_before_forward_delay}")  
        move_response = requests.get(f'http://{car_address}/manualDriving?dir=forward&delay={adjusted_delay}')
        if move_response.status_code != 200:
            print(f"Moving towards item - Failed to move car forward: {move_response.status_code}, Attempted delay: {adjusted_delay}")
        else:
            print(f"Moving towards item - Moved forward with delay: {adjusted_delay}")

    def search_after_movement():
        for i in range(num_of_aligns):
            cropped_img = image_utils.capture_frame(frame_type="stream", frame_name=f'search_after_move-{i}')
            results = detector.detect(cropped_img, object_label)
            if results:
                for result in results:
                    label_result, confidence, x1, y1, x2, y2, line_length = result
                    if confidence > detection_confidence and label_result == object_label:
                        return {'found': True, 'centroid_x': (x1 + x2) // 2, 'frame_width': cropped_img.shape[1], 'line_length': line_length}
        return {'found': False}

    def move_backward():
        response = requests.get(f'http://{car_address}/manualDriving?dir=backward&delay={min_distance_forward_delay}')
        if response.status_code != 200:
            print(f"Failed to move car backward: {response.status_code}, Attempted delay: {min_distance_forward_delay}")

    def prepare_for_pick_up(backward_delay):        
            move_response = requests.get(f'http://{car_address}/manualDriving?dir=left&delay={half_circle_delay + extra_turn_left_delay}')                        
            if move_response.status_code != 200:
                        print("Failed to move car for a half of circle:", move_response.status_code)
                                           
            divided_backward_delay = int(backward_delay/num_of_divisions_for_backward_delay)   
            for i in range(num_of_divisions_for_backward_delay):         
                move_response = requests.get(f'http://{car_address}/manualDriving?dir=backward&delay={divided_backward_delay}')
                if move_response.status_code != 200:
                    print("Moving towards item - Failed to move car backward:", move_response.status_code)    
                time.sleep(1)
    
    try:
        search_result = search_for_object()
        if not search_result['found']:
            return {'found': False}

        update_task_status(task_id, 'running', 25, object_label)

        if search_result['found']:
            while True:
                align_result = align_with_object(search_result['centroid_x'], search_result['frame_width'], search_result['line_length'])
                if align_result['aligned']:
                    move_towards_object(search_result['line_length'])
                    new_search_result = search_after_movement()
                    if not new_search_result['found']:
                        move_backward()
                        prepare_for_pick_up(min_distance_forward_delay * 3)
                        update_task_status(task_id, '', 25, object_label, 'Object successfully picked up')
                        break
                    search_result = new_search_result
                    
                    frame_center = search_result['frame_width'] // 2
                    if (abs(search_result['centroid_x'] - frame_center) <= search_result['frame_width'] * alignment_threshold
                        and search_result['line_length'] <= min_distance):
                        move_towards_object(search_result['line_length'])
                        prepare_for_pick_up(min_distance_forward_delay * 2)
                        update_task_status(task_id, '', 25, object_label, 'Object successfully picked up')
                        break
                else:
                    print("Alignment failed. Retrying.")
        return {**search_result, **align_result}
    finally:
        requests.get(f'http://{car_address}/ledoff')
