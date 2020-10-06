# Save as client.py 
# Message Sender
import os
from socket import *
host = "73.243.41.224" # set to IP address of target computer
port = 87
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
while True:
    data = input("Enter message to send or type 'exit': ").encode()
    UDPSock.sendto(data, addr)
    print(data.decode())
    if data.decode() == "exit":
        print("Exiting server")
        break
UDPSock.close()
os._exit(0)