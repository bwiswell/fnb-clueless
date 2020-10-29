class Player:
    def __init__(self):
        name = ""
        #location = Room Class
        weapon = ""
        turnOrder = 0
    
    def sendServerMsg(self):
        # Here we will impliment the player Directions and how to move
        # From here a message will be sent using the messaging service
        # Messaging service will send messages to the Server side based
        # based on player choices
        
        print("messages Sent")