# Save as server.py 
# Message Receiver
import os
import pickle
from socket import *
host = "192.168.0.177"
port = 87
buf = 1024
addr = (host, port)
UDPSock = socket(AF_INET,SOCK_STREAM)
#UDPSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 5)
UDPSock.bind((host,port))
UDPSock.listen(1)
conn, addr = UDPSock.accept()
print(f"Waiting to receive messages from {addr}...")
while True:
    data = conn.recv(buf)
    data_var = pickle.loads(data)
    
    #(data, addr) = UDPSock.recvfrom(buf)
    print("Received message: " + data_var)
    if data_var == "exit":
        print("Exiting server")
        break
conn.close()
os._exit(0)