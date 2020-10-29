# Save as server.py 
# Message Receiver
import os
import pickle
import Message as msg
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

status = True

print(f"Waiting to receive messages from {addr}...")
while status:
    data = conn.recv(buf)
    data_var = pickle.loads(data)
    
    print("Received message: " + data_var)
    if data_var == "exit":
        print("Exiting server")
        status = False
        
print("here1")
message = msg.Message()
msg = "Does this work? Sending Server -> Client"
message.SendClientMsg(conn, addr, msg)


conn.close()
os._exit(0)