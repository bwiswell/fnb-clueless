# Save as server.py 
# Message Receiver
import os
import pickle
import Message as msg
from Player import Player
import Information as info
import Wrapper as wrap
from socket import *
import asyncio


info1 = info.Information()

class Game():
    def __init__(self):
        self.info = info.Information()
        self.active_player = 0
        self.players = []
        
    async def start_game(self, player):
        if player.number == 0:
            await player.sendshit(self.info)

    async def end_turn(self, player):
        player_count = len(self.players)
        self.active_player = (player.number + 1) % player_count

        next_player = self.players[self.active_player]
        await next_player.sendshit(self.info)

    async def move(self, player, data):
        if player.number == self.active_player:
            print(data.location)
            print(data.name)
            self.info.updateCurrentLocation(data)
            locations = self.info.getCurrentLocations()
            msg = wrap.MsgUpdateGame(self.info)
            print(locations)
            
            await self.end_turn(player)

class Server():

    def __init__(self):
        
        self.running = False
        self.players = []
        self.max_players = 4
        self.game = Game()

    def register_player(self, writer):
        player_count = len(self.players)
        if player_count < self.max_players:
            new_player = Player(number=player_count, writer=writer)
            self.game.players.append(new_player)
            return new_player, self.game
        else:
            return None

    async def handle_client(self, reader, writer):
        buf = 2048
        player, game = self.register_player(writer)

        while self.running and player is not None:
            data = await reader.read(buf)
            data_var = pickle.loads(data)
            msgid = wrap.HeaderNew(data_var).id
            print(msgid)
            print("Received message: " + str(data_var))

            if(msgid == 1000):
                await game.start_game(player)
            elif(msgid == 1234):
                print("Normal Message no object message")
            elif(msgid == 102):
                playerData = data_var.player
                await game.move(player, playerData)

            if msg == "exit":
                print("Exiting server...")
                self.running = False

        writer.close()
        await writer.wait_closed()

    async def run(self, host, port):
        self.running = True
        server = await asyncio.start_server(
            self.handle_client, host, port
        )

        async with server:
            await server.serve_forever()

server = Server()
asyncio.run(server.run("0.0.0.0", 87))


# open = True

# while open:

#     host = "192.168.0.177"
#     port = 87
#     buf = 2048
#     addr = (host, port)
#     UDPSock = socket(AF_INET,SOCK_STREAM)
#     UDPSock.bind((host,port))
#     UDPSock.listen(1)
#     conn, addr = UDPSock.accept()

#     status = True
#     data_var = ""
#     print(f"Waiting to receive messages from {addr}...")
#     while status:
#         data = conn.recv(buf)
#         data_var = pickle.loads(data)
#         wph = data_var
   
        
#         print("Received message: " + str(data_var))

#         if(wph.HeaderId == 1234):
#             print("Normal Message no object message")
#         elif(wph.HeaderId == 8888):
#             print(wph.data.playerData.location)
#             print(wph.data.playerData.playerIp)
#             info1.updateCurrentLocation(wph.data.playerData)
#             locations = info1.getCurrentLocations()
#             print(locations)


#         if data_var == "exit":
#             print("Exiting server...")
#             status = False
    

#    message = msg.Message()
#    msg = "Does this work? Sending Server -> Client"
#    message.SendClientMsg(conn, addr, msg)

    # conn.close()

