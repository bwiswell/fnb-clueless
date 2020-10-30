# Save as server.py 
# Message Receiver
import os
import pickle
import Message as msg
import Player as pl
import Information as info
import Wrapper as wrap
from socket import *

info1 = info.Information()
wph = wrap.Header()


open = True

while open:

    host = "192.168.0.177"
    port = 87
    buf = 2048
    addr = (host, port)
    UDPSock = socket(AF_INET,SOCK_STREAM)
    UDPSock.bind((host,port))
    UDPSock.listen(1)
    conn, addr = UDPSock.accept()

    status = True
    data_var = ""
    print(f"Waiting to receive messages from {addr}...")
    while status:
        data = conn.recv(buf)
        data_var = pickle.loads(data)
        wph = data_var
   
        
        print("Received message: " + str(data_var))

        if(wph.HeaderId == 1234):
            print("Normal Message no object message")
        elif(wph.HeaderId == 8888):
            print(wph.data.playerData.location)
            print(wph.data.playerData.playerIp)
            info1.updateCurrentLocation(wph.data.playerData)
            locations = info1.getCurrentLocations()
            print(locations)


        if data_var == "exit":
            print("Exiting server...")
            status = False
    

#    message = msg.Message()
#    msg = "Does this work? Sending Server -> Client"
#    message.SendClientMsg(conn, addr, msg)

    conn.close()
