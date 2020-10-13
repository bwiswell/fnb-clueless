# Save as server.py 
# Message Receiver
import os
import pickle
import Player as pl
from socket import *


host = "192.168.0.177"
port = 87
buf = 2048
addr = (host, port)
UDPSock = socket(AF_INET,SOCK_STREAM)
UDPSock.bind((host,port))
UDPSock.listen(1)
conn, addr = UDPSock.accept()

player1 = pl.Player()

print(f"Waiting to receive messages from {addr}...")
while True:
    data = conn.recv(buf)
    data_var = pickle.loads(data)
    player1 = data_var
    
    #(data, addr) = UDPSock.recvfrom(buf)
    print("Received message: " + player1.name)
    if data_var == "exit":
        print("Exiting server")
        break
conn.close()
os._exit(0)