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

ans = "N"

while ((ans != "Y") & (ans != "y")):
    player.name = input("Enter player name: ")
    ans = input(player.name + " correct? (Y/N): ")
    print("")

menuDict = {"1", "2", "3", "4", "5", "6"}
menuStrDict = {1: "up", 2: "down", 3: "left", 4: "right", 5:"diagnol"}
print("Welcome to FNB-Clueless Game " + player.name + "...")

status = True

while status:
    print("Please select from the following menu:")
    print("1) Move Up")
    print("2) Move Down")
    print("3) Move Left")
    print("4) Move Right")
    print("5) Move Diagnol")
    print("6) Exit")
    print("")
    move = input("Enter Move: ")

    # checks if move is valid integer in range
    if move in menuDict:
        ans = input("Option " + move + " selected, correct? (Y/N): ")
        
        # confirms player move
        if ((ans == "Y") | (ans == "y")):
            if move == "6":
                msg = 'exit'
                print("Exiting...")
                message.SendServerMsg(msg)
                status = False

            else:
                msg = player.name + " moving " + menuStrDict[int(move)] + "..."
                print(player.name + " moving " + menuStrDict[int(move)] + "...")
                print("")
                
                conn = message.getConnectionInfo()
                ip, port = conn.getpeername()
                
                player.playerIp = ip
                player.location = str(menuStrDict[int(move)])

                wpd.setPlayerData(player)
                wph.data = wpd
                wph.setHeaderId()

                message.SendServerMsg(wph)
        else:
            print("Move not confirmed...")
            print("")
    else:
        print("Invalid move selected...")
        print("")
