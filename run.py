import os
os.environ['OPENCV_LOG_LEVEL'] = 'SILENT'

# libraries installed using propmts in terminal
from flask import Flask, render_template, Response, send_file # communication between user and the main server
import RPi.GPIO as GPIO			# Rasp Pi GPIO pins
import time				# to calculate delay
import cv2   				# video footage capturing
from datetime import datetime		# used to calculate latency				
import threading			# frame the capture video footage

# Setup Flask app
app = Flask(__name__)

# GPIO pins for motor control (connected to L298N IN pins)
m11 = 18  # Motor 1 Forward (IN1)
m12 = 23  # Motor 1 Backward (IN2)
m21 = 24  # Motor 2 Forward (IN3)
m22 = 25  # Motor 2 Backward (IN4)

# GPIO pins for firing DC motor
fire_m1 = 22  # Fire motor forward
fire_m2 = 17  # Fire motor backward

# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(m11, GPIO.OUT)
GPIO.setup(m12, GPIO.OUT)
GPIO.setup(m21, GPIO.OUT)
GPIO.setup(m22, GPIO.OUT)

# Setup fire motor pins
GPIO.setup(fire_m1, GPIO.OUT)
GPIO.setup(fire_m2, GPIO.OUT)

# Shared variable for video frames
frame_lock = threading.Lock()
current_frame = None

# Camera initialization
camera = cv2.VideoCapture(0)

# Thread to continuously read frames
def capture_frames():
    global current_frame
    while True:
        success, frame = camera.read()
        if success:
            with frame_lock:
                current_frame = frame

# Start frame capture thread
frame_thread = threading.Thread(target=capture_frames, daemon=True)
frame_thread.start()

# Function to generate video frames for streaming
def generate_frames():
    global current_frame
    while True:
        with frame_lock:
            if current_frame is None:
                continue
            success, buffer = cv2.imencode('.jpg', current_frame)  # originally saved in H.264 or M4V format
            frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# Function to capture an image
@app.route('/capture_image')
def capture_image():
    global current_frame
    with frame_lock:
        if current_frame is not None:
            filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"
            filepath = os.path.join("./images", filename)
            os.makedirs("./images", exist_ok=True)
            cv2.imwrite(filepath, current_frame)
            return send_file(filepath, as_attachment=True)
    return "Failed to capture image", 500

# Routes for motor control
@app.route('/')
def index():
    return render_template('robot.html')

# Function to stop all motors
def stop_motors():
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)
    GPIO.output(fire_m1, 0)
    GPIO.output(fire_m2, 0)

@app.route('/left_side')
def left_side():
    stop_motors()  # Stop any current movement
    GPIO.output(m11, 0)
    GPIO.output(m12, 1)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)
    return 'true'

@app.route('/right_side')
def right_side():
    stop_motors()  # Stop any current movement
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 1)
    return 'true'

@app.route('/up_side')
def up_side():
    stop_motors()  # Stop any current movement
    GPIO.output(m11, 0)
    GPIO.output(m12, 1)
    GPIO.output(m21, 0)
    GPIO.output(m22, 1)
    return 'true'

@app.route('/down_side')
def down_side():
    stop_motors()  # Stop any current movement
    GPIO.output(m11, 1)
    GPIO.output(m12, 0)
    GPIO.output(m21, 1)
    GPIO.output(m22, 0)
    return 'true'

@app.route('/stop')
def stop():
    stop_motors()  # Immediately stop all motors
    return 'true'

# Route for firing DC motor
@app.route('/fire')
def fire():
    stop_motors()  # Stop any current movement before firing
    # Run motor in one direction for a short time
    GPIO.output(fire_m1, 0)
    GPIO.output(fire_m2, 1)
    time.sleep(2)  # Adjust duration as needed
    # Stop the motor
    GPIO.output(fire_m1, 0)
    GPIO.output(fire_m2, 0)
    return 'true'

# Route for video feed
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Main entry point
if __name__ == "__main__":
    print('Start')
    try:
        app.run(host='192.168.216.59', port=5010, debug=False)
    finally:
        GPIO.cleanup()
        camera.release()
        print("Resources released. Program terminated.")
