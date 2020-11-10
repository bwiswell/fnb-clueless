# Save as client.py 
# Message Sender
import os
import pickle
import Message as msgClass
import Player as pl
import Wrapper as wrap
import Information as info
import asyncio

player = pl.Player()
message = msgClass.Message()



class Client():
    def __init__(self):
        self.running = False
        self.info = info.Information()

    async def handle_server(self,reader,writer):
        buf = 2048
        # send game start
        data_string = pickle.dumps(wrap.MsgLobbyReady())
        writer.write(data_string)
        while self.running:

            data = await reader.read(buf)
            data_var = pickle.loads(data)
            playerUpdate = data_var
            self.info = playerUpdate
            print("Received message: " + str(data_var))

            player.name = "Rob"
            player.location = "Right"

            data_string = pickle.dumps(wrap.MsgPassPlayer(player))
            writer.write(data_string)

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

print("here")


#SendPlayerInformation(player)

print(ip)

#data = conn.recv(2048)

   
# repeat as long as message 
# string are not empty 
#while data:
#    data_var = pickle.loads(data)
#    print("Received message: " + data_var)
#    data = conn.recv(2048)
