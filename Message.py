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
        self.UDPSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.UDPSock.connect(self.addr)


    def SendServerMsg(self,msg):

        status = True
        while status:
            data_string = pickle.dumps(msg)

            if msg == "exit":
                print("Exiting server in snd msg")
                status = False
            else:
                self.UDPSock.send(data_string)
                print(msg)
                status = False


    def SendPlayerInformation(self,player):
        print("sending")
    
    def SendClientMsg(self, conn, addr, msg):
        # This will most likely be used to send GUI updates to client from
        # server.
        data_string = pickle.dumps(msg)
        conn.send(data_string)
        
    def getConnectionInfo(self):
        return self.UDPSock

    #def RcvPlayerMsg(self):
        # This may not be needed as the Server should always be listening

    #def RcvServerMsg(self):
        # Might be needed for the client to get messages from the server

    #def holdGUIUpdate():
        # This will be used to hold the updated GUI state
        # if and once its updated from the server to client