import os
import pickle
import socket
import Player as pl

class Message:
    def __init__(self):
        #trial
        host = "73.243.41.224" # set to IP address of target computer
        port = 87
        addr = (host, self.port)
        UDPSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        UDPSock.connect(addr)
    
    def SendServerMsg(self,msg):
        while True:
            #data = input("Enter message to send or type 'exit': ")
            data_string = pickle.dumps(msg)
            self.UDPSock.send(data_string)
            print(data_string)
            if data_string == "exit":
                print("Exiting server")
                break
        self.UDPSock.close()
        os._exit(0)
    
    def SendClientMsg(self):

    def RcvPlayerMsg(self):

    def RcvServerMsg(self):

    #def holdGUIUpdate():
        # This will be used to hold the updated GUI state
        # if and once its updated from the server to client
