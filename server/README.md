ESP32 Camera Car Server
This folder contains the main server application for connecting the UI to the ESP32 camera car. The server facilitates communication and provides important endpoints for controlling the car and performing object detection.

Table of Contents
Installation
Usage
Endpoints
GET /
GET /health
GET /car/health
GET /car/motion/start
GET /car/motion/stop
GET /camera/detection_comp
GET /camera/save_object
GET /camera/locating_any_objects
Helper Functions
rotate_image
License
Installation
Clone the repository:
bash
Copy code
git clone <repository_url>
Navigate to the server directory:
bash
Copy code
cd <repository_name>/server
Install the required Python packages:
bash
Copy code
pip install -r requirements.txt
Usage
To start the server, run:

bash
Copy code
python app.py
The server will start on http://localhost:8080.

Endpoints
GET /
Returns the content of the readme.txt file.

GET /health
Returns a simple 'TEST endpoint' message to verify the server is running.

GET /car/health
This endpoint is reserved for future implementation to check the health status of the car.

GET /car/motion/start
This endpoint is reserved for future implementation to start the motion of the car.

GET /car/motion/stop
This endpoint is reserved for future implementation to stop the motion of the car.

GET /camera/detection_comp
Performs object detection on a predefined image check.jpg.

Response:

200 OK with JSON result of the object detection.
400 Bad Request if there is an error reading the query image.
GET /camera/save_object
Captures an image from the car's camera, processes it, and saves it locally as a grayscale image.

Parameters:

name (required): The name to save the object as.
Response:

200 OK with a success message.
400 Bad Request if required parameters are missing.
500 Internal Server Error if there is an error during the request.
GET /camera/locating_any_objects
Continuously captures images from the car's camera, processes them, and tries to locate any objects until one is found.

Response:

200 OK with the index of the best match.
Helper Functions
rotate_image
Rotates an image by a given angle.

Parameters:

image: The image to be rotated.
angle: The angle to rotate the image by.
Returns:

The rotated image.
License
This project is licensed under the MIT License. See the LICENSE file for details.
