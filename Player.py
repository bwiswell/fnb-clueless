import pickle

class Player:
    def __init__(self, number=None, writer=None, location=None, character=None):
        self.name = ""
        self.location = location
        self.character = character
        self.cards = ""
        self.turnOrder = 0
        self.playerIP = ""
        self.number = number
        self.writer = writer

    # method to send server any msg type usinga wrapper
    async def sendServerMsg(self,msg):
        data_string = pickle.dumps(msg)
        self.writer.write(data_string)
        await self.writer.drain()
    