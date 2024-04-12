# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask
from flask_cors import CORS

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def readme():
    with open('./readme.txt', 'r') as file:
        readme_content = file.read()
    return readme_content

@app.route('/health',methods=[ 'GET'])
def test():
	return 'TEST endpoint'

@app.route('/car/health' ,methods=[ 'GET'])
def car_health():
    pass

@app.route('/car/motion/start' ,methods=[ 'GET'])
def car_motion_start():
    pass

@app.route('/car/motion/stop' ,methods=[ 'GET'])
def car_motion_stop():
    pass

@app.route('/camera/detection' ,methods=[ 'GET'])
def detect_object():
    pass

if __name__ == '__main__':
	app.run(debug=True, port=8080)

