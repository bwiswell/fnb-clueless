import os
import pickle
import Player as pl
import Wrapper as wrap
import Information as info
import Lobby
import ClueGUI
import asyncio
import ClueEnums
from ClueEnums import Actions
import AdjList
import time

player = pl.Player()


class Client():
    def __init__(self):
        self.running = False
        self.info = info.Information()
        self.gui = None
        self.validMoves = []
        self.actionList = []
        self.lost = False
        self.myNumber = None
        self.suggested = False

    async def handle_server(self,reader,writer):
        # start the lobby
        lobby = Lobby.Lobby()
        # get name from lobby
        name = lobby.getPlayerName()

        player.name = name
        player.location = "ballroom"
        # send msg across pipe to update server player
        msgWrap = wrap.MsgUpdatePlayer(player)
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
            print("Received message from server: " + str(data_var.id))
            # take msg.id and do the task for the corrsponding wrapper
            if (data_var.id == 103):
                print(f"Client Player Number: {data_var.data.playerNum}")
                self.myNumber = data_var.data.playerNum
                # checking player position and if 0 starting game using button
                # Then start GUI after wrtiting to server
                if(data_var.data.playerNum == 0):
                    lobby.getStart("FNBC")
                    data_string = pickle.dumps(wrap.HeaderNew(wrap.MsgLobbyReady()))
                    writer.write(data_string)
                else:
                    lobby.showWaitingMessage()
                # send player message not payer 1
                # will update all locations now generally happens at end of turn/ start of next players turn       
            elif( data_var.id == 501):
                self.info = data_var.data.info
                self.gui.updateGUI(self.info.storeAllPlayers)

            elif(data_var.id == 100):
                lobby.close()
                self.info = data_var.data.gameInfo
                self.gui = ClueGUI.ClueGUI(data_var.data.indviPlayer,self.info.storeAllPlayers)
            elif(data_var.id == 105):
                self.gui.postMessage("Your turn has begun!")
                self.suggested = False
                self.validMoves = AdjList.determineValidMoves(self.info.storeAllPlayers[self.myNumber], self.info.storeAllPlayers)

                if (self.lost and len(self.validMoves) == 0):
                    self.actionList = [Actions.ENDTURN]
                elif (self.lost):
                    self.actionList = [Actions.MOVE]
                elif (len(self.validMoves) == 0 and ClueEnums.isRoom(self.info.storeAllPlayers[self.myNumber].location)):
                    self.actionList = [Actions.ACCUSE, Actions.SUGGEST, Actions.ENDTURN]
                elif (len(self.validMoves) == 0):
                    self.actionList = [Actions.ENDTURN]
                elif (ClueEnums.isRoom(self.info.storeAllPlayers[self.myNumber].location)):
                    self.actionList = [Actions.MOVE, Actions.ACCUSE, Actions.SUGGEST]
                else:
                    self.actionList = [Actions.MOVE]

                action = self.gui.getPlayerAction(self.actionList)
                self.actionList.remove(action)
                msg = self.handleAction(action)
                writer.write(msg)
                
            elif(data_var.id == 106):
                if (ClueEnums.isRoom(self.info.storeAllPlayers[self.myNumber].location)):
                    # According to the project description, one suggestion per turn
                    if (Actions.SUGGEST not in self.actionList and not self.lost and not self.suggested):
                        self.actionList.append(Actions.SUGGEST)
                    if (Actions.ACCUSE not in self.actionList and not self.lost):
                        self.actionList.append(Actions.ACCUSE)
                else:
                    if Actions.SUGGEST in self.actionList:
                        self.actionList.remove(Actions.SUGGEST)
                    if Actions.ACCUSE in self.actionList:
                        self.actionList.remove(Actions.ACCUSE)

                if (len(self.actionList) == 0 or Actions.MOVE not in self.actionList):

                    self.actionList.append(Actions.ENDTURN)

                action = self.gui.getPlayerAction(self.actionList)
                self.actionList.remove(action)
                msg = self.handleAction(action)
                writer.write(msg)

            elif(data_var.id == 201):
                suggestion_text = data_var.data.name + " suggested that it was "
                suggestion_text += data_var.data.suggestion["player"].text
                suggestion_text += " in the " + data_var.data.suggestion["location"].text
                suggestion_text += " with the " + data_var.data.suggestion["weapon"].text + "!"
                self.gui.postMessage(suggestion_text)
                disproven_text = data_var.data.name + " was "
                if data_var.data.disprov_card is None:
                    disproven_text += "not "
                disproven_text += "disproven."
                self.gui.postMessage(disproven_text)
                if data_var.data.disprov_card is not None and data_var.data.playerNum == self.myNumber:
                    disproven_text = data_var.data.disprov_player.name + " disproved your suggestion with the "
                    disproven_text += data_var.data.disprov_card.text + " card."
                    self.gui.postMessage(disproven_text)

            elif(data_var.id == 6666):
                # Somebody lost the game
                accusation_text = data_var.data.name + " accused "
                accusation_text += data_var.data.accusation["player"].text
                accusation_text += " in the " + data_var.data.accusation["location"].text
                accusation_text += " with the " + data_var.data.accusation["weapon"].text + "!"
                self.gui.postMessage(accusation_text)
                lost_text = data_var.data.name + " lost the game!"
                self.gui.postMessage(lost_text)
                if data_var.data.playerNum == self.myNumber:
                    self.lost = True

            elif(data_var.id == 7777):
                # Somebody won the game
                won_message = data_var.data.name + " won!"
                self.gui.postMessage(won_message)
                accusation_text = "It was " + data_var.data.accusation["player"].text
                accusation_text += " in the " + data_var.data.accusation["location"].text
                accusation_text += " with the " + data_var.data.accusation["weapon"].text + "!"
                self.gui.postMessage(accusation_text)
                time.sleep(3)
                self.gui.quit()
                self.running = False

            else:
                pass

        # send move
        writer.close()
        await writer.wait_closed()
    
    def handleAction(self, action):
        if action == Actions.MOVE:
            player = self.info.storeAllPlayers[self.myNumber]
            move = self.gui.getPlayerMove(self.validMoves)
            player.location = move
            data_string = pickle.dumps(wrap.HeaderNew(wrap.MsgMovePlayer(player)))
            return data_string
        elif action == Actions.SUGGEST:
            self.suggested = True
            location = self.info.storeAllPlayers[self.myNumber].location
            suggestion = self.gui.getPlayerSuggestion(location)
            data_string = pickle.dumps(wrap.HeaderNew(wrap.MsgSuggest(suggestion)))
            return data_string
        elif action == Actions.ACCUSE:
            location = self.info.storeAllPlayers[self.myNumber].location
            accusation = self.gui.getPlayerAccusation(location)
            data_string = pickle.dumps(wrap.HeaderNew(wrap.MsgAccuse(accusation)))
            return data_string
        else:
            data_string = pickle.dumps(wrap.HeaderNew(wrap.MsgEndTurn()))
            return data_string

        
    # method to connect the client to the server.
    async def run(self,host,port):
        self.running = True
        reader, writer = await asyncio.open_connection(
            host,port
        )

        await self.handle_server(reader, writer)


client = Client()
asyncio.run(client.run("73.243.41.224", 87))