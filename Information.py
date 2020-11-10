import Player as pl

class Information:
    def __init__(self):
        self.storeAllPlayers = []
        self.currentLocation = []
        self.startLocations = ["hw2", "hw11", "hw8", "hw5"]

    def updateCurrentLocation(self,incomingPlayer):
        player = pl.Player()
        player = incomingPlayer
        if(self.currentLocation.__len__() != 0):
            for index, pair in enumerate(self.currentLocation):
                if pair[0] == player.name:
                    print((pair[0],player.location))
                    self.currentLocation[index] = (pair[0],player.location)
                    print(currentLocation)
                else:
                    self.currentLocation.append((player.name,player.location))
                    print(self.currentLocation.__len__())
        else:
            self.currentLocation.append((player.name,player.location))
            print(self.currentLocation.__len__())


    def getCurrentLocations(self):
        return self.currentLocation
