import Player as pl

class Information:
    def __init__(self):
        self.storeAllPlayers = []
        self.currentLocation = []
        self.allLocations = []
        print("here123")


    def updateCurrentLocation(self,incomingPlayer):
        print("here124")

        player = pl.Player()
        player = incomingPlayer
        if(self.currentLocation.__len__() != 0):
            for index, pair in enumerate(self.currentLocation):
                if pair[0] == player.playerIP:
                    print((pair[0],player.location))
                    self.currentLocation[index] = (pair[0],player.location)
                    print(currentLocation)
                else:
                    self.currentLocation.append((player.playerIp,player.location))
                    print("here123")
                    print(self.currentLocation.__len__())
        else:
            self.currentLocation.append((player.playerIp,player.location))
            print("here125")
            print(self.currentLocation.__len__())



    def getCurrentLocations(self):
        return self.currentLocation
