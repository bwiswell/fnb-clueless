import os
import pickle
import Player as pl
import Wrapper as wrap
import Information as info
import Lobby
import ClueGUI
import asyncio

player = pl.Player()


class Client():
    def __init__(self):
        self.running = False
        self.info = info.Information()
        self.gui = None

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
            print("Received message: " + str(data_var))
            # take msg.id and do the task for the corrsponding wrapper
            if (data_var.id == 103):
                print(f"Client:msg ID: {data_var.data.playerNum}")
                # checking player position and if 0 starting game using button
                # Then start GUI after wrtiting to server
                if(data_var.data.playerNum == 0):
                    lobby.giveStartButton()
                    data_string = pickle.dumps(wrap.HeaderNew(wrap.MsgLobbyReady()))
                    writer.write(data_string)
                    # lobby.close()
                    # self.gui = ClueGUI.ClueGUI(data_var.data.indviPlayer,self.info.currentLocation)
                else:
                    pass
                # send player message not payer 1
                # will update all locations now generally happens at end of turn/ start of next players turn       
            elif( data_var.id == 501):
                self.info = data_var.data.info
                #impliment method here to take in self.info and return list of (name, location) tuples to feed below
                #gui.upddateGUI()

            elif(data_var.id == 100):
                lobby.close()
                self.info = data_var.data.gameInfo
                print("Client Name: " + str(data_var.data.indviPlayer.name))
                # send player start message?
                self.gui = ClueGUI.ClueGUI(data_var.data.indviPlayer,self.info.storeAllPlayers)
            else:
                pass
            
            #here we will impliment from the GUI player actions ie)move,suggest,accuse
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