# Save as client.py 
# Message Sender
import os
import pickle
import socket

host = "73.243.41.224" # set to IP address of target computer
port = 87
addr = (host, port)
UDPSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
UDPSock.connect(addr)
while True:
    data = input("Enter message to send or type 'exit': ")
    data_string = pickle.dumps(data)
    UDPSock.send(data_string)
    print(data_string)
    if data == "exit":
        print("Exiting server")
        break
UDPSock.close()
os._exit(0)