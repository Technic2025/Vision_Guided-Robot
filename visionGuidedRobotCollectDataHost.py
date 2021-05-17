#This program runs as host and is used to collect training images. There is a corresponding program for the robot. 
#Images are saved to the host computer.

import socket
import pickle
from PIL import Image as im

#Connect to socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 12345))
s.listen(1)
print("Server connected")

#Recieve camera data from robot
HEADERSIZE = 10
imageNum = 3394
while True:
    conn, addr = s.accept()
    print(f"Connection from {addr} has been established.")
    full_msg = b""
    new_msg = True
    while True:
        msg = conn.recv(1024)
        if new_msg:
            msglen = int(msg[:HEADERSIZE])
            new_msg = False
        full_msg += msg

        if len(full_msg) - HEADERSIZE == msglen:
            print("full message recieved")
            d = pickle.loads(full_msg[HEADERSIZE:])
            data = im.fromarray(d)
            data.save(f"image{imageNum}.png")
            imageNum += 1
            new_msg = True
            full_msg = b""