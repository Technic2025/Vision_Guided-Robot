import socket
import picamera
import picamera.array
import numpy as np
import pickle

HEADERSIZE = 10

HOST = "10.0.0.238"
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