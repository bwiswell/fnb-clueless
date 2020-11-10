import pickle

class Player:
    def __init__(self, number=None, writer=None):
        name = ""
        location = "test"
        cards = ""
        turnOrder = 0
        playerIP = ""
        self.number = number
        self.writer = writer

    async def sendshit(self,msg):
        data_string = pickle.dumps(msg)

        self.writer.write(data_string)
        await self.writer.drain()
    
    def sendServerMsg(self):
        # Here we will impliment the player Directions and how to move
        # From here a message will be sent using the messaging service
        # Messaging service will send messages to the Server side based
        # based on player choices
        
        print("messages Sent")