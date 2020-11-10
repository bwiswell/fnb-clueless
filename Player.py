import pickle

class Player:
    def __init__(self, number=None, writer=None):
        self.name = ""
        self.location = "test"
        self.cards = ""
        self.turnOrder = 0
        self.playerIP = ""
        self.number = number
        self.writer = writer

    async def sendServerMsg(self,msg):
        data_string = pickle.dumps(msg)
        self.writer.write(data_string)
        await self.writer.drain()
    