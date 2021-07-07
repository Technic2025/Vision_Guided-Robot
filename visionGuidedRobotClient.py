import socket
import picamera
import picamera.array
import numpy as np
import pickle
import RPi.GPIO as gpio
import time
import random

gpio.setmode(gpio.BCM)

gpio.setup(17, gpio.OUT)

gpio.setup(26, gpio.OUT)
gpio.setup(19, gpio.OUT)
gpio.setup(13, gpio.OUT)
gpio.setup(6, gpio.OUT)

gpio.output(17, False)

gpio.output(26, False)
gpio.output(19, False)
gpio.output(13, False)
gpio.output(6, False)

HEADERSIZE = 10

def drive_forward():
    gpio.output(26, False)
    gpio.output(19, True)
    gpio.output(13, True)
    gpio.output(6, False)
    
def turn():
    gpio.output(26, False)
    gpio.output(19, False)
    gpio.output(13, False)
    gpio.output(6, False)
    
    t = random.uniform(-.5, .5)
    
    if t < 0:
        gpio.output(26, False)
        gpio.output(19, True)
        gpio.output(13, False)
        gpio.output(6, True)
    else:
        gpio.output(26, True)
        gpio.output(19, False)
        gpio.output(13, True)
        gpio.output(6, False)
        
    time.sleep(abs(t))
    
    gpio.output(26, False)
    gpio.output(19, False)
    gpio.output(13, False)
    gpio.output(6, False)

def run_command(command):
    print(command)
    if "lights_on" in command:
        gpio.output(17, True)
        print("on")
    elif "lights_off" in command:
        gpio.output(17, False)
        print("off")
    if "turn" in command:
        pass
        turn()
        #move back, turn random direction approx 45-180 in either direction
    elif "drive_forward" in command:
        drive_forward()

HOST = "10.0.0.27"
PORT = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as output:
        camera.resolution = (320, 240)
        while True:
            image = np.empty((240, 320, 3), dtype = np.uint8)
            camera.capture(image, "rgb")
            msg = pickle.dumps(image)
            msg = bytes(f"{len(msg):<{HEADERSIZE}}", "utf-8") + msg
            s.send(msg)
            command = s.recv(1024)
            run_command(command.decode("utf-8"))
