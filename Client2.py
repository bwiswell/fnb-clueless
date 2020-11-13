import Lobby
import ClueGUI
import Information
import Player

import ClueEnums
from ClueEnums import Locations, Rooms, Actions, Characters, Weapons

player = Player.Player()
player2 = Player.Player()
player3 = Player.Player()
player4 = Player.Player()

info = Information.Information()

# start the lobby
lobby = Lobby.Lobby()
# get name from lobby
player.name = lobby.getPlayerName()
player.location = Locations.STUDY
player.character = Characters.MSSCARLET
player.cards = [Rooms.KITCHEN, Characters.PROFPLUM, Weapons.CANDLESTICK]
player2.name = "Rob"
player2.location = Locations.KITCHEN
player2.character = Characters.REVGREEN
player3.name = "Ben"
player3.location = Locations.LOUNGE
player3.character = Characters.MRSPEACOCK
player4.name = "Frank"
player4.location = Locations.CONSERVATORY
player4.character = Characters.CNLMUSTARD

lobby.getStart("FNBC")
lobby.close()
gui = ClueGUI.ClueGUI(player, [player, player2, player3, player4])
           
hasAccused = False
movedBySuggestion = False
isTurn = True
CHARACTER = 0
LOCATION = 1

def findPlayerIndex(character):
    for i in range(len(playerLocs)):
        if playerLocs[i][CHARACTER] == character:
            return i

def determineValidMoves():
    if ClueEnums.isRoom(player.location):
        for p,loc in playerLocs:
            print(loc)
            if not ClueEnums.isRoom(loc):
                if loc in moveList:
                    moveList.remove(loc)
    print(moveList)

def updateGUI():
    # TODO: add the following line back in when I am ready to get server updates
    #playerLocs = info.getCurrentLocations()
    # TODO: remove this line when server update is used instead
    playerLocs = [
                  (player.character, player.location),
                  (player2.character, player2.location),
                  (player3.character, player3.location),
                  (player4.character, player4.location)
                 ]
    print(playerLocs) # TODO: remove this print eventually
    gui.updateGUI(playerLocs)
    return playerLocs

while True:
    # TODO: wait for server update
    # server will need to tell client whether this is a suggestion/accusation or actual turn
    playerLocs = updateGUI()
    player.location = playerLocs[findPlayerIndex(player.character)][LOCATION]

    if isTurn is True:
        moveList = MOVEDICT[player.location]  # derermines potential move options
        actionList = [Actions.MOVE, Actions.ACCUSE, Actions.SUGGEST]  # all potential actions
        print(moveList)  # TODO: remove this print eventually
        determineValidMoves()
        print(moveList)  # TODO: remove this print eventually
        if hasAccused is True:
            actionList.remove(Actions.ACCUSE)
            actionList.remove(Actions.SUGGEST)
            if len(moveList) == 0:
                actionList.remove(Actions.MOVE)
                actionList.append(Actions.ENDTURN)
        else:
            if movedBySuggestion is True:
                movedBySuggestion = False
                if len(moveList) == 0:
                    moveList.append(player.location)
                    actionList.append(Actions.ENDTURN)
            else:
                if not ClueEnums.isRoom(player.location):
                    actionList.remove(Actions.ACCUSE)
                    actionList.remove(Actions.SUGGEST)
                elif len(moveList) == 0:
                    actionList.remove(Actions.MOVE)
                    actionList.remove(Actions.SUGGEST)
                    actionList.append(Actions.ENDTURN)

        # action list loop until all valid actions exhausted or turn is ended
        while len(actionList) > 0:
            print(actionList)
            action = gui.getPlayerAction(actionList)
            
            # takes appropriate steps based on action
            if action == Actions.MOVE:
                actionList.remove(Actions.MOVE)
                player.location = gui.getPlayerMove(moveList)
                playerLocs = updateGUI()
                actionList.append(Actions.ENDTURN)

                if not ClueEnums.isRoom(player.location):
                    if Actions.ACCUSE in actionList:
                        actionList.remove(Actions.ACCUSE)
                    if Actions.SUGGEST in actionList:
                        actionList.remove(Actions.SUGGEST)
                else:
                    if hasAccused is False:
                        actionList.append(Actions.ACCUSE)
                        actionList.append(Actions.SUGGEST)

            elif action == Actions.SUGGEST:
                actionList.remove(Actions.SUGGEST)
                print("Making suggestion...")
                suggestion = gui.getPlayerSuggestion()
                # TODO: handle suggestion

            elif action == Actions.ACCUSE:
                hasAccused = True
                actionList.remove(Actions.ACCUSE)
                if Actions.SUGGEST in actionList:
                    actionList.remove(Actions.SUGGEST)
                print("Making accusation...")
                accusation = gui.getPlayerAccusation()
                # TODO: handle accusation

            else:
                actionList.remove(Actions.ENDTURN)
                print("Turn ending...")
                break
    else:
        movedBySuggestion = True