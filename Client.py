# Save as client.py 
# Message Sender
import os
import Message as msgClass
import Player as pl

player = pl.Player()
#message = msgClass.Message()
ans = "N"

while ans != "Y":
    player.name = input("Enter player name: ")
    ans = input(player.name + " correct? (Y/N): ")
    print("")

menuDict = {"1", "2", "3", "4", "5"}
menuStrDict = {1: "up", 2: "down", 3: "left", 4: "right"}
print("Welcome to FNB-Clueless Game " + player.name + "...")

while True:
    print("Please select from the following menu:")
    print("1) Move Up")
    print("2) Move Down")
    print("3) Move Left")
    print("4) Move Right")
    print("5) Exit")
    print("")
    move = input("Enter Move: ")

    # checks if move is valid integer in range
    if move in menuDict:
        ans = input("Option " + move + " selected, correct? (Y/N): ")
        
        # confirms player move
        if ans == "Y":
            if move == "5":
                print("Exiting...")
                os._exit(0)
            else:
                msg = player.name + "\t" + move
                print(player.name + " moving " + menuStrDict[int(move)] + "...")
                print("")
                # message.SendServerMsg(msg)
        else:
            print("Move not confirmed...")
            print("")
    else:
        print("Invalid move selected...")
        print("")
