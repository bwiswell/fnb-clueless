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
isTurn = True
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

def updateGUI():
    # TODO: add the following line back in when I am ready to get server updates
    #playerLocs = info.getCurrentLocations()
    # TODO: remove this line when server update is used instead
    playerLocs = [
                  (player.name, player.location),
                  (player2.name, player2.location),
                  (player3.name, player3.location),
                  (player4.name, player4.location)
                 ]
    print(playerLocs) # TODO: remove this print eventually
    gui.updateGUI(playerLocs)
    return playerLocs

while True:
    # TODO: wait for server update
    # server will need to tell client whether this is a suggestion/accusation or actual turn
    playerLocs = updateGUI()
    player.location = playerLocs[findPlayerIndex(player.name)][LOCATION]

    if isTurn is True:
        moveList = moveDict[player.location]  # derermines potential move options
        actionList = ["move", "accuse", "suggest"]  # all potential actions
        print(moveList)  # TODO: remove this print eventually
        determineValidMoves()
        print(moveList)  # TODO: remove this print eventually
        if hasAccused is True:
            actionList.remove("accuse")
            actionList.remove("suggest")
            if len(moveList) == 0:
                actionList.remove("move")
                actionList.append("end turn")
        else:
            if movedBySuggestion is True:
                movedBySuggestion = False
                if len(moveList) == 0:
                    moveList.append(player.location)
                    actionList.append("end turn")
            else:
                if "hw" in player.location:
                    actionList.remove("accuse")
                    actionList.remove("suggest")
                elif len(moveList) == 0:
                    actionList.remove("move")
                    actionList.remove("suggest")
                    actionList.append("end turn")

        # action list loop until all valid actions exhausted or turn is ended
        while len(actionList) > 0:
            print(actionList)
            action = gui.getPlayerAction(actionList)
            
            # takes appropriate steps based on action
            if action == "move":
                actionList.remove("move")
                player.location = gui.getPlayerMove(moveList)
                playerLocs = updateGUI()
                actionList.append("end turn")

                if "hw" in player.location:
                    if "accuse" in actionList:
                        actionList.remove("accuse")
                    if "suggest" in actionList:
                        actionList.remove("suggest")
                else:
                    if hasAccused is False:
                        actionList.append("accuse")
                        actionList.append("suggest")

            elif action == "suggest":
                actionList.remove("suggest")
                print("Making suggestion...")
                # TODO: handle suggestion

            elif action == "accuse":
                hasAccused = True
                actionList.remove("accuse")
                actionList.remove("suggest")
                print("Making accusation...")
                # TODO: handle accusation

            else:
                actionList.remove("end turn")
                print("Turn ending...")
                break
    else:
        movedBySuggestion = True
