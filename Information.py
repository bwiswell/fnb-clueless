import Player as pl

class Information:
    def __init__(self):
        self.storeAllPlayers = []
        self.currentLocation = []
        self.allLocations = []

    def updateCurrentLocation(self,incomingPlayer):
        player = pl.Player()
        player = incomingPlayer

        for index, pair in enumerate(self.currentLocation):
            if pair[0] == player.playerIP:
                print((pair[0],player.location))
                self.currentLocation[index] = (pair[0],player.location)
                print(currentLocation)
            else:
                self.currentLocation.append((player.playerIp,player.location))


    def getCurrentLocations(self):
        return self.currentLocation
