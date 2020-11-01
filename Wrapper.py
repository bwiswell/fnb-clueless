import Player as pl

class Wrapper:
    def __init__(self):
        print("hello")


class Header:
    def __init__(self):
        self.HeaderId = 1234
        self.data = Data()
        self.DataSize = self.data.__sizeof__()


    def setHeaderId(self):

        if isinstance(self.data.dataObject, pl.Player):
            self.HeaderId = 8888
        else:
            self.HeaderId = 12345
    

        
        
class Data:
    def __init__(self):
        p1 = pl.Player()
        self.playerData = p1
        self.dataType = Data
        self.dataObject = p1

    def setPlayerData(self,data):
        
        p1 = pl.Player()
        p1 = data
        self.playerData = p1
        self.dataObject = p1
        self.dataType = pl.Player

    def printData(self):
        print(self.playerData)
