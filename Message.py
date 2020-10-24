import os
import pickle
import socket
import Player as pl

class Message:
    def __init__(self):
        #trial
        host = "73.243.41.224" # set to IP address of target computer
        port = 87
        self.addr = (host, port)

    
    def SendServerMsg(self,msg):
        UDPSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        UDPSock.connect(self.addr)
        while True:
            #data = input("Enter message to send or type 'exit': ")
            data_string = pickle.dumps(msg)
            UDPSock.send(data_string)
            print(data_string)
            if data_string == "exit":
                print("Exiting server")
                break
        UDPSock.close()
        os._exit(0)
    
    #def SendClientMsg(self):
        # This will most likely be used to send GUI updates to client from
        # server. 

    #def RcvPlayerMsg(self):
        # This may not be needed as the Server should always be listening

    #def RcvServerMsg(self):
        # Might be needed for the client to get messages from the server

    #def holdGUIUpdate():
        # This will be used to hold the updated GUI state
        # if and once its updated from the server to client
