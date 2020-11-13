import os
import pickle
import Player as pl
import Wrapper as wrap
import Information as info
import Lobby
import ClueGUI
import asyncio

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

moveDict = {
            "hw1":hall1List, "hw2":hall2List, "hw3":hall3List, "hw4":hall4List, "hw5":hall5List, "hw6":hall6List,
            "hw7":hall7List, "hw8":hall8List, "hw9":hall9List, "hw10":hall10List, "hw11":hall11List, "hw12":hall12List,
            "study":studyList, "hall":hallList, "lounge":loungeList,
            "library":libraryList, "billiard room":billiardRoomList, "dining room":diningRoom,
            "conservatory":conservatoryList, "ballroom":ballroomList, "kitchen":kitchenList
           }
NAME = 0
LOCATION = 1

class Client():
    def __init__(self):
        self.player = pl.Player()
        self.running = False
        self.info = info.Information()
        self.gui = None
        self.moveList = None
        self.actionList = None
        self.hasAccused = False
        self.movedBySuggestion = False
        self.isTurn = False

    def findPlayerIndex(self, name):
        for i in range(len(self.info)):
            if self.info[i][NAME] == name:
                return i

    def determineValidMoves(self):
        if "hw" not in self.player.location:
            for loc in self.info:
                print(loc)
                if "hw" in loc[LOCATION]:
                    if loc[LOCATION] in self.moveList:
                        self.moveList.remove(loc[LOCATION])
        print(self.moveList)

    def updateGUI(self):
        # TODO: add the following line back in when I am ready to get server updates
        # playerLocs = info.getCurrentLocations()
        # TODO: remove this line when server update is used instead
        # playerLocs =
        # [
        #     (player.name, player.location),
        #     (player2.name, player2.location),
        #     (player3.name, player3.location),
        #     (player4.name, player4.location)
        # ]
        print(self.info)  # TODO: remove this print eventually
        self.gui.updateGUI(self.info)

    async def handle_server(self,reader,writer):
        # start the lobby
        lobby = Lobby.Lobby()
        # get name from lobby
        name = lobby.getPlayerName()

        self.player.name = name
        self.player.location = "study"
        # send msg across pipe to update server player
        msgWrap = wrap.MsgUpdatePlayer(self.player)
        helper = wrap.HeaderNew(msgWrap)
        data_string = pickle.dumps(helper)
        writer.write(data_string)

        buf = 2048

        while self.running:
            # async wait to read data from server and process them below
            # based on msg.id
            data = await reader.read(buf)
            data_var = pickle.loads(data)
            # playerUpdate = data_var
            # self.info = playerUpdate
            print("Received message: " + str(data_var))
            # take msg.id and do the task for the corrsponding wrapper
            if (data_var.id == 103):
                print(data_var.data.playerNum)
                # checking player position and if 0 starting game using button
                # Then start GUI after wrtiting to server
                if(data_var.data.playerNum == 0):
                    lobby.giveStartButton()
                    data_string = pickle.dumps(wrap.HeaderNew(wrap.MsgLobbyReady()))
                    writer.write(data_string)
                    lobby.close()
                    self.gui = ClueGUI.ClueGUI(self.player,[self.player])
                else:
                    pass
                   # send player message not payer 1
            # will update all locations now generally happens at end of turn/ start of next players turn
            elif( data_var.id == 501):
                self.info = data_var.data.info
                self.updateGUI()
                self.player.location = self.info[self.findPlayerIndex(self.player.name)][LOCATION]
                if self.isTurn is True:
                    self.moveList = moveDict[self.player.location]  # derermines potential move options
                    self.actionList = ["move", "accuse", "suggest"]  # all potential actions
                    print(self.moveList)  # TODO: remove this print eventually
                    self.determineValidMoves()
                    print(self.moveList)  # TODO: remove this print eventually
                    if self.hasAccused is True:
                        self.actionList.remove("accuse")
                        self.actionList.remove("suggest")

                        if len(self.moveList) == 0:
                            self.actionList.remove("move")
                            self.actionList.append("end turn")
                    else:
                        if self.movedBySuggestion is True:
                            self.movedBySuggestion = False
                            if len(self.moveList) == 0:
                                self.moveList.append(self.player.location)
                                self.actionList.append("end turn")
                        else:
                            if "hw" in self.player.location:
                                self.actionList.remove("accuse")
                                self.actionList.remove("suggest")
                            elif len(self.moveList) == 0:
                                self.actionList.remove("move")
                                self.actionList.remove("suggest")
                                self.actionList.append("end turn")
    
                    # action list loop until all valid actions exhausted or turn is ended
                    while len(self.actionList) > 0:
                        print(self.actionList)
                        action = self.gui.getPlayerAction(self.actionList)
        
                        # takes appropriate steps based on action
                        if action == "move":
                            self.actionList.remove("move")
                            self.player.location = self.gui.getPlayerMove(self.moveList)
                            self.updateGUI()
                            self.actionList.append("end turn")
            
                            if "hw" in self.player.location:
                                if "accuse" in self.actionList:
                                    self.actionList.remove("accuse")
                                if "suggest" in self.actionList:
                                    self.actionList.remove("suggest")
                            else:
                                if self.hasAccused is False:
                                    self.actionList.append("accuse")
                                    self.actionList.append("suggest")
        
                        elif action == "suggest":
                            self.actionList.remove("suggest")
                            print("Making suggestion...")
                            # TODO: handle suggestion
        
                        elif action == "accuse":
                            self.hasAccused = True
                            self.actionList.remove("accuse")
                            if "suggest" in self.actionList:
                                self.actionList.remove("suggest")
                            print("Making accusation...")
                            # TODO: handle accusation
        
                        else:
                            self.actionList.remove("end turn")
                            print("Turn ending...")
                            break
                else:
                    movedBySuggestion = True
            else:
                pass

            # player.name = "Rob"
            # player.location = "Right"

            # msgWrap = wrap.MsgPassPlayer(player)
            # helper = wrap.HeaderNew(msgWrap)
            # data_string = pickle.dumps(helper)
            # writer.write(data_string)

        # send move
        writer.close()
        await writer.wait_closed()
    # method to connect the client to the server.
    async def run(self,host,port):
        self.running = True
        reader, writer = await asyncio.open_connection(
            host,port
        )

        await self.handle_server(reader, writer)

client = Client()
asyncio.run(client.run("73.243.41.224", 87))
