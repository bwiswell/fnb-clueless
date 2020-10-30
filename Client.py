# Save as client.py 
# Message Sender
import os
import pickle
import Message as msgClass
import Player as pl
import Wrapper as wrap

player = pl.Player()
message = msgClass.Message()
wph = wrap.Header()
wpd = wrap.Data()

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
