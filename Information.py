import Player as pl

class Information:
    def __init__(self):
        # Intial data to be updated or pulled
        self.storeAllPlayers = []
        self.currentLocation = []
        self.startLocations = ["hw2", "hw11", "hw8", "hw5"]
        self.WEAPON_LIST = ["Candlestick", "Knife", "Ropes", "Revolver", "Lead", "Wrench"]
        self.ROOMNAME_LIST = ["Study", "Lounge", "Ballroom", "Library", "Billiard Room", "Hall", "Dining Room", "Conservatory", "Kitchen"]


    # when a move option occurs this will update the list of current player locations
    def updateCurrentLocation(self,incomingPlayer):
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

    # getter to get all player locations
    def getCurrentLocations(self):
        return self.currentLocation