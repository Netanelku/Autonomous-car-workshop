
# ESP32 Camera Car Server

This folder contains the main server application for connecting the UI to the ESP32 camera car.
The server facilitates communication and provides important endpoints for controlling the car and performing object detection.

## Table of Contents
- [Installation](#Installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Helper Functions](#helper-functions)
- [License](#license)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Netanelku/Autonomous-car-workshop
2. Navigate to the server directory:
   ```bash
   cd https://github.com/Netanelku/Autonomous-car-workshop/server
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
4. Usage
   To start the server, run:
   ```bash
   python app.py
  The server will start on http://localhost:8080.

## Endpoints
1. GET /: Returns the content of the readme.txt file.
2. GET /health: Returns 'TEST endpoint' to verify the server is running.
3. GET /car/health: Reserved for future implementation to check the health status of the car.
4. GET /car/motion/start: Reserved for future implementation to start the car's motion.
5. GET /car/motion/stop: Reserved for future implementation to stop the car's motion.
6. GET /camera/detection_comp: Performs object detection on a predefined image check.jpg.
7. GET /camera/save_object: Captures an image from the car's camera, processes it, and saves it locally as a grayscale image. Requires a name parameter.
8. GET /camera/locating_any_objects: Continuously captures images from the car's camera, processes them, and tries to locate any objects until one is found.
## Helper Functions
rotate_image: Rotates an image by a given angle.
## License
This project is licensed under the MIT License. See the LICENSE file for details.
