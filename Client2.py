import Lobby
import ClueGUI
import Information
import Player

player = Player.Player()
player2 = Player.Player()
player3 = Player.Player()
player4 = Player.Player()

info = Information.Information()

# start the lobby
lobby = Lobby.Lobby()
# get name from lobby
player.name = lobby.getPlayerName()
player.location = "study"
player2.name = "Rob"
player2.location = "kitchen"
player3.name = "Ben"
player3.location = "lounge"
player4.name = "Frank"
player4.location = "conservatory"

lobby.giveStartButton()
lobby.close()
gui = ClueGUI.ClueGUI(player, [player, player2, player3, player4])

studyList = ["hw1", "hw3", "kitchen", "lounge", "conservatory"]
hall1List = ["study", "hall"]
hallList = ["hw1", "hw2", "hw4"]
hall2List = ["hall", "lounge"]
loungeList = ["hw2", "hw5", "study", "conservatory", "kitchen"]

hall3List = ["study", "library"]
hall4List = ["hall", "billiard room"]
hall5List = ["lounge", "dining room"]

libraryList = ["hw3", "hw6", "hw8"]
hall6List = ["library", "billiard room"]
billiardRoomList = ["hw4", "hw6", "hw7", "hw9"]
hall7List = ["billiard room", "dining room"]
diningRoom = ["hw5", "hw7", "hw10"]

hall8List = ["library", "conservatory"]
hall9List = ["billiard room", "ballroom"]
hall10List = ["dining room", "kitchen"]

conservatoryList = ["hw8", "hw11", "study", "lounge", "kitchen"]
hall11List = ["conservatory", "ballroom"]
ballroomList = ["hw9", "hw11", "hw12"]
hall12List = ["ballroom", "kitchen"]
kitchenList = ["hw10", "hw12", "study", "lounge", "conservatory"]

cornerRooms = ["study", "lounge", "conservatory", "kitchen"]

moveDict = {
            "hw1":hall1List, "hw2":hall2List, "hw3":hall3List, "hw4":hall4List, "hw5":hall5List, "hw6":hall6List,
            "hw7":hall7List, "hw8":hall8List, "hw9":hall9List, "hw10":hall10List, "hw11":hall11List, "hw12":hall12List,
            "study":studyList, "hall":hallList, "lounge":loungeList,
            "library":libraryList, "billiard room":billiardRoomList, "dining room":diningRoom,
            "conservatory":conservatoryList, "ballroom":ballroomList, "kitchen":kitchenList
           }
hasAccused = False
movedBySuggestion = False
NAME = 0
LOCATION = 1

def findPlayerIndex(name):
    for i in range(len(playerLocs)):
        if playerLocs[i][NAME] == name:
            return i

def determineValidMoves():
    if "hw" not in player.location:
        for loc in playerLocs:
            print(loc)
            if "hw" in loc[LOCATION]:
                if loc[LOCATION] in moveList:
                    moveList.remove(loc[LOCATION])
    print(moveList)

while True:
    #playerLocs = info.getCurrentLocations()
    playerLocs = [
                  (player.name, player.location),
                  (player2.name, player2.location),
                  (player3.name, player3.location),
                  (player4.name, player4.location)
                 ]
    gui.updateGUI(playerLocs)
    print(playerLocs)
    player.location = playerLocs[findPlayerIndex(player.name)][LOCATION]
    moveList = moveDict[player.location]
    actionList = ["move", "accuse", "suggest", "endturn"]
    print(moveList)
    determineValidMoves()
    print(moveList)

    action = gui.getPlayerAction(actionList)
    move = gui.getPlayerMove(moveList)
    print(action)
    print(move)
    player.location = move