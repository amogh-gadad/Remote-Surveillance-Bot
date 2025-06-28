# Raspberry Pi Camera Tank

## Overview
The **Raspberry Pi Camera Tank** is a remote-controlled robotic vehicle designed for **real-time video streaming** and **interactive control** over a web interface. Built using a Raspberry Pi, USB camera, motor driver, and electromechanical firing system, this platform serves as an educational project in **robotics, IoT, and embedded systems**.  

---

## Features
✅ Wireless control over the internet or LAN  
✅ Live MJPEG video streaming  
✅ Tank locomotion: forward, backward, left, right  
✅ Electromechanical firing mechanism control  
✅ Snapshot capture and download  
✅ Modular design for future AI integration  

---

## System Architecture

**Hardware Components:**
- Raspberry Pi (central controller)
- L298N Motor Driver
- DC Motors (movement)
- Electromechanical Firing Motor
- USB Camera (video feed)
- Power Supply

**Software Stack:**
- **Python 3**
- **Flask Framework** (web interface & HTTP server)
- **OpenCV** (video capture & MJPEG streaming)
- **RPi.GPIO** (GPIO pin control)
- **Multithreading** (smooth parallel video streaming)

---

## Functional Workflow

1. The Raspberry Pi initializes all components.
2. The Flask web server hosts the control dashboard.
3. User sends commands:
   - Movement control
   - Firing trigger
   - Snapshot capture
4. Raspberry Pi processes the commands:
   - Sends GPIO signals to motors and firing mechanism
   - Streams live video feed
5. User receives real-time video and control feedback.

---

## Design Specifications

**Inputs:**
- User commands via Flask web app
- Live camera feed (USB webcam)

**Outputs:**
- DC Motor movement (PWM signals)
- Firing motor control
- Live MJPEG video stream
- Captured image snapshots

**Protocols & Libraries:**
- HTTP (Flask)
- GPIO + PWM (RPi.GPIO)
- MJPEG streaming (OpenCV)
- Multithreading (Python `threading`)

---

## Results
✅ Real-time video streaming verified  
✅ Responsive robot movement control  
✅ Successful firing mechanism activation  
✅ Image capture and download functionality  
✅ Stable web interface with minimal latency  

![Final](https://github.com/user-attachments/assets/7229cc9a-3eb1-45fb-adef-8ac01277aa5c)

---

## Tech Stack
- **Language:** Python 3
- **Frameworks:** Flask, OpenCV
- **Libraries:** RPi.GPIO, threading
- **Platform:** Raspberry Pi OS (Linux)

---

## Safety Precautions
- Ensure proper motor driver wiring to avoid shorts.
- Verify the power supply ratings before connecting motors.
- Test firing mechanism carefully in a controlled environment.

---

## Future Work
- Integrate autonomous navigation with AI object detection.
- Add obstacle avoidance sensors.
- Develop a mobile app interface.
- Improve video streaming performance over WAN.

---

## Authors
- Amogh M. Gadad 
- Amruta R. Biradarpatil 
- Ashtami Hosapeti 
- Naman Timmapur

Department of Electronics and Communication Engineering  
KLE Technological University, Dr. M.S. Sheshgiri Campus, Belagavi, India
