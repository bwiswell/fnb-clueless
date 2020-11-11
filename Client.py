# Save as client.py 
# Message Sender
import os
import pickle
import pygame
from ClueGUI import ClueGUI
#import Message as msgClass
import Player
import Wrapper as wrap

gui = ClueGUI()
player = Player()
#message = msgClass.Message()
#wph = wrap.Header()
#wpd = wrap.Data()

studyList = ["HW0", "HW6", "Kitchen", "Lounge", "Conservatory"]
hall0List = ["Study", "Hall"]
hallList = ["HW0", "HW1", "HW8"]
hall1List = ["Hall", "Lounge"]
loungeList = ["HW1", "HW10", "Study", "Conservatory", "Kitchen"]

hall6List = ["Study", "Library"]
hall8List = ["Hall", "Billiard Room"]
hall10List = ["Lounge", "Dining Room"]

libraryList = ["HW2", "HW6", "HW7"]
hall2List = ["Library", "Billiard Room"]
billiardRoomList = ["HW2", "HW3", "HW8", "HW9"]
hall3List = ["Billiard Room", "Dining Room"]
diningRoom = ["HW3", "HW10", "HW11"]

hall7List = ["Library", "Conservatory"]
hall9List = ["Billiard Room", "Ballroom"]
hall11List = ["Dining Room", "Kitchen"]

conservatoryList = ["HW4", "HW7", "Study", "Lounge", "Kitchen"]
hall4List = ["Conservatory", "Ballroom"]
ballroomList = ["HW4", "HW5", "HW9"]
hall5List = ["Ballroom", "Kitchen"]
kitchenList = ["HW5", "HW11", "Study", "Lounge", "Conservatory"]

cornerRooms = ["Study", "Lounge", "Conservatory", "Kitchen"]

moveDict = {
            "HW0":hall0List, "HW1":hall1List, "HW2":hall2List, "HW3":hall3List, "HW4":hall4List, "HW5":hall5List,
            "HW6":hall6List, "HW7":hall7List, "HW8":hall8List, "HW9":hall9List, "HW10":hall10List, "HW11":hall11List,
            "Study":studyList, "Hall":hallList, "Lounge":loungeList,
            "Library":libraryList, "Billiard Room":billiardRoomList, "Dining Room":diningRoom,
            "Conservatory":conservatoryList, "Ballroom":ballroomList, "Kitchen":kitchenList
           }

actionList = ["accuse", "suggest", "endturn"]
locList = ["Hall", "Library"]
playerLocs = [("Rob", "Hall"), ("Ben", "HW1"), ("Frank", "Study"), ("Sahil", "Hall")]
gui.updateGUI()
hasAccused = False
movedBySuggestion = False
NAME = 0
LOCATION = 1

def findPlayerIndex(name):
    for i in playerLocs.__len__():
        if playerLocs[i][NAME] == name:
            return i

def determineValidMoves():
    if "HW" not in player.location:

        for loc in playerLocs:
            print(loc)

            if "HW" in loc[LOCATION]:
                if loc[LOCATION] in moveList:
                    moveList.remove(loc[LOCATION])
    print(moveList)

while True:
    # wait for server update along with updated player locations
    # use information class here to get playerLocs list of tuples
    gui.updateGUI()
    print(playerLocs)
    # determine list of valid player moves
    player.location = playerLocs[findPlayerIndex(player.name)][LOCATION]
    moveList = moveDict[player.location]
    actionList = ["move", "accuse", "suggest", "endturn"]
    print(moveList)
    determineValidMoves(playerLocs)
    print(moveList)

    if moveList.__len__() == 0:
        actionList.remove("move")

        if movedBySuggestion is True:
            if player.location not in cornerRooms:
                actionList.remove("accuse")
                actionList.remove("suggest")
            

    if hasAccused is True:
        actionList.remove("accuse")
        actionList.remove("suggest")

    action = gui.getPlayerAction(actionList)

    if action == "endturn":
        raise SystemExit

    elif action == "accuse":
        hasAccused = True
        name = "Rob" # TODO: will need to get from GUI
        playerToMove = Player()
        playerToMove.location = player.location
        # wpd.setPlayerData(player)
        # wph.data = wpd
        # wph.setHeaderId()
        # message.SendServerMsg(wph)
        
        # wpd.setPlayerData(playerToMove)
        # wph.data = wpd
        # wph.setHeaderId()
        # message.SendServerMsg(wph)
        # TODO: send message to server with this information
        # TODO: wait for server update on whether accusation was correct
        

    elif action == "suggest":
        name = "Rob" # TODO: will need to get from GUI
        playerToMove = Player()
        playerToMove.location = player.location
        # wpd.setPlayerData(player)
        # wph.data = wpd
        # wph.setHeaderId()
        # message.SendServerMsg(wph)

        # wpd.setPlayerData(playerToMove)
        # wph.data = wpd
        # wph.setHeaderId()
        # message.SendServerMsg(wph)

    move = gui.getPlayerMove(moveList)
    print(action)
    print(move)
    player.location = move







    # conn = message.getConnectionInfo()
    # ip, port = conn.getpeername()
    #
    # player.playerIp = ip
    #


    #if suggestion made check
    #package message and send update to server

    # for event in pygame.event.get():
    #     if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_ESCAPE:
    #             raise SystemExit

# while ((ans != "Y") & (ans != "y")):
#     player.name = input("Enter player name: ")
#     ans = input(player.name + " correct? (Y/N): ")
#     print("")
#
# menuDict = {"1", "2", "3", "4", "5", "6"}
# menuStrDict = {1: "up", 2: "down", 3: "left", 4: "right", 5:"diagnol"}
# print("Welcome to FNB-Clueless Game " + player.name + "...")
#
# status = True
#
# while status:
#     print("Please select from the following menu:")
#     print("1) Move Up")
#     print("2) Move Down")
#     print("3) Move Left")
#     print("4) Move Right")
#     print("5) Move Diagnol")
#     print("6) Exit")
#     print("")
#     move = input("Enter Move: ")
#
#     # checks if move is valid integer in range
#     if move in menuDict:
#         ans = input("Option " + move + " selected, correct? (Y/N): ")
#
#         # confirms player move
#         if ((ans == "Y") | (ans == "y")):
#             if move == "6":
#                 msg = 'exit'
#                 print("Exiting...")
#                 message.SendServerMsg(msg)
#                 status = False
#
#             else:
#                 msg = player.name + " moving " + menuStrDict[int(move)] + "..."
#                 print(player.name + " moving " + menuStrDict[int(move)] + "...")
#                 print("")
#                 conn = message.getConnectionInfo()
#                 ip, port = conn.getpeername()
#                 player.playerIp = ip
#                 player.location = str(menuStrDict[int(move)])
#
#                 wpd.setPlayerData(player)
#                 wph.data = wpd
#                 wph.setHeaderId()
#
#                 message.SendServerMsg(wph)
#         else:
#             print("Move not confirmed...")
#             print("")
#     else:
#         print("Invalid move selected...")
#         print("")
#
# print("here")
#
#
# #SendPlayerInformation(player)
#
# print(ip)
#
# #data = conn.recv(2048)
#
#
# # repeat as long as message
# # string are not empty
# #while data:
# #    data_var = pickle.loads(data)
# #    print("Received message: " + data_var)
# #    data = conn.recv(2048)
