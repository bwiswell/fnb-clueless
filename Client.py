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
from Constants import RED, GREEN

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
            print("Received message from server: " + str(data_var.id))
            if (data_var.id == 103):
                # Player number received from server
                print(f"Client Player Number: {data_var.data.playerNum}")
                self.myNumber = data_var.data.playerNum
                if(data_var.data.playerNum == 0):
                    # Player 1, give start button (now called getStart())
                    lobby.getStart("FNBC")
                    data_string = pickle.dumps(wrap.HeaderNew(wrap.MsgLobbyReady()))
                    writer.write(data_string)
                else:
                    # Not player 1, wait for game to start
                    lobby.showWaitingMessage()   

            # General location update message (new locations in storeAllPlayers)   
            elif( data_var.id == 501):
                self.info = data_var.data.info
                self.gui.updateGUI(self.info.storeAllPlayers)

            # Game start message
            elif(data_var.id == 100):
                lobby.close()
                self.info = data_var.data.gameInfo
                self.gui = ClueGUI.ClueGUI(data_var.data.indviPlayer,self.info.storeAllPlayers)

            # Turn start message for this client's player
            elif(data_var.id == 105):
                self.gui.postMessage("Your turn has begun!", GREEN)
                self.suggested = False
                self.validMoves = AdjList.determineValidMoves(self.info.storeAllPlayers[self.myNumber], self.info.storeAllPlayers)

                if (self.lost and len(self.validMoves) == 0):
                    self.actionList = [Actions.ENDTURN]
                elif (self.lost):
                    self.actionList = [Actions.MOVE]
                elif (len(self.validMoves) == 0 and ClueEnums.isRoom(self.info.storeAllPlayers[self.myNumber].location)):
                    self.actionList = [Actions.ACCUSE, Actions.SUGGEST, Actions.ENDTURN]
                elif (len(self.validMoves) == 0):
                    self.actionList = [Actions.ACCUSE, Actions.ENDTURN]
                elif (ClueEnums.isRoom(self.info.storeAllPlayers[self.myNumber].location)):
                    self.actionList = [Actions.MOVE, Actions.ACCUSE, Actions.SUGGEST]
                else:
                    self.actionList = [Actions.MOVE, Actions.ACCUSE]

                action = self.gui.getPlayerAction(self.actionList)
                self.actionList.remove(action)
                msg = self.handleAction(action)
                writer.write(msg)
                
            # Turn continue message for this client's player
            elif(data_var.id == 106):
                if (ClueEnums.isRoom(self.info.storeAllPlayers[self.myNumber].location)):
                    # According to the project description, one suggestion per turn
                    if (Actions.SUGGEST not in self.actionList and not self.lost and not self.suggested):
                        self.actionList.append(Actions.SUGGEST)
                    elif (Actions.SUGGEST in self.actionList and self.lost):
                        self.actionList.remove(Actions.SUGGEST)
                else:
                    if Actions.SUGGEST in self.actionList:
                        self.actionList.remove(Actions.SUGGEST)

                if (len(self.actionList) == 0 or Actions.MOVE not in self.actionList):
                    self.actionList.append(Actions.ENDTURN)

                action = self.gui.getPlayerAction(self.actionList)
                self.actionList.remove(action)
                msg = self.handleAction(action)
                writer.write(msg)

            # Suggestion response message (somebody, maybe this client, made a suggestion
            # and now the server is broadcasting to all clients what the suggestion was and
            # if it was correct)
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
                # If this client made the suggestion, then this player gets to see which card
                # and which player disproved it (if any)
                if data_var.data.disprov_card is not None and data_var.data.playerNum == self.myNumber:
                    disproven_text = data_var.data.disprov_player.name + " disproved your suggestion with the "
                    disproven_text += data_var.data.disprov_card.text + " card."
                    self.gui.postMessage(disproven_text)

            # Game lost message (somebody, maybe this client, made an incorrect accusation
            # and now the server is broadcasting to all clients what the accusation was
            # and that it was incorrect)
            elif(data_var.id == 6666):
                accusation_text = data_var.data.name + " accused "
                accusation_text += data_var.data.accusation["player"].text
                accusation_text += " in the " + data_var.data.accusation["location"].text
                accusation_text += " with the " + data_var.data.accusation["weapon"].text + "!"
                self.gui.postMessage(accusation_text)
                lost_text = data_var.data.name + " lost the game!"
                self.gui.postMessage(lost_text)
                # If this client made the accusation, then set the lost flag to True
                if data_var.data.playerNum == self.myNumber:
                    self.lost = True

            # Game won message (somebody, maybe this client, made a correct accusation and
            # now the server is broadcasting to all clients what the accusation was and
            # that it was correct and ended the game
            elif(data_var.id == 7777):
                won_message = data_var.data.name + " won!"
                self.gui.postMessage(won_message)
                accusation_text = "It was " + data_var.data.accusation["player"].text
                accusation_text += " in the " + data_var.data.accusation["location"].text
                accusation_text += " with the " + data_var.data.accusation["weapon"].text + "!"
                self.gui.postMessage(accusation_text)

                # Give players time to see the won message and then quit the game
                time.sleep(3)
                self.gui.quit()
                self.running = False

            else:
                pass

        # Close server connection
        writer.close()
        await writer.wait_closed()
    
    # Handle any player action and return the response message to be sent back to the
    # server
    def handleAction(self, action):
        # Handle a move action
        if action == Actions.MOVE:
            player = self.info.storeAllPlayers[self.myNumber]
            move = self.gui.getPlayerMove(self.validMoves)
            player.location = move
            data_string = pickle.dumps(wrap.HeaderNew(wrap.MsgMovePlayer(player)))
            return data_string
        # Handle a suggest action
        elif action == Actions.SUGGEST:
            self.suggested = True
            location = self.info.storeAllPlayers[self.myNumber].location
            suggestion = self.gui.getPlayerSuggestion(location)
            data_string = pickle.dumps(wrap.HeaderNew(wrap.MsgSuggest(suggestion)))
            return data_string
        # Handle an accuse action
        elif action == Actions.ACCUSE:
            location = self.info.storeAllPlayers[self.myNumber].location
            accusation = self.gui.getPlayerAccusation()
            data_string = pickle.dumps(wrap.HeaderNew(wrap.MsgAccuse(accusation)))
            return data_string
        # Handle an end turn action
        else:
            self.gui.postMessage("Your turn has ended.", RED)
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
asyncio.run(client.run("71.204.206.17", 25565))