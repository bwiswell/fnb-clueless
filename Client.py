# Save as client.py 
# Message Sender
import os
import pickle
import Message as msgClass
import Player as pl
import Wrapper as wrap
import Information as info
import Lobby
import ClueGUI
import asyncio

player = pl.Player()
message = msgClass.Message()




class Client():
    def __init__(self):
        self.running = False
        self.info = info.Information()
        self.gui = None

    async def handle_server(self,reader,writer):
        lobby = Lobby.Lobby()
        name = lobby.getPlayerName()

        player.name = name
        player.location = "ballroom"

        msgWrap = wrap.MsgUpdatePlayer(player)
        helper = wrap.HeaderNew(msgWrap)
        data_string = pickle.dumps(helper)
        writer.write(data_string)

        buf = 2048
        # send game start


        while self.running:

            data = await reader.read(buf)
            data_var = pickle.loads(data)
            playerUpdate = data_var
            self.info = playerUpdate
            print("Received message: " + str(data_var))

            if (data_var.id == 103):
                print(data_var.data.playerNum)
                if(data_var.data.playerNum == 0):
                    lobby.giveStartButton()
                    data_string = pickle.dumps(wrap.HeaderNew(wrap.MsgLobbyReady()))
                    writer.write(data_string)
                    lobby.close()
                    self.gui = ClueGUI.ClueGUI(player,[player])

                else:
                    pass
                    # send player message not payer 1
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

    async def run(self,host,port):
        self.running = True
        reader, writer = await asyncio.open_connection(
            host,port
        )

        await self.handle_server(reader, writer)


client = Client()
asyncio.run(client.run("73.243.41.224", 87))
