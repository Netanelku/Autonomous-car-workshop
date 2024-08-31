import yaml
from process_utils import update_task_status, locate_and_align_object

def load_config():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    with open('constants.yaml', 'r') as file:
        constants = yaml.safe_load(file)
    return config, constants
