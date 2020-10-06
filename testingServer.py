# Save as server.py 
# Message Receiver
import os
from socket import *
host = "192.168.0.177"
port = 1803
buf = 1024
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)
print("Waiting to receive messages...")
while True:
    (data, addr) = UDPSock.recvfrom(buf)
    print("Received message: " + data.decode())
    if data.decode() == "exit":
        print("Exiting server")
        break
UDPSock.close()
os._exit(0)
