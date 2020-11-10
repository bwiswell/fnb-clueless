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
        print("gmae started")
        if player.number == 0:
            msg = wrap.HeaderNew(wrap.MsgPassInformation(self.info))
            await player.sendServerMsg(msg)

    async def end_turn(self, player):
        player_count = len(self.players)
        self.active_player = (player.number + 1) % player_count

        next_player = self.players[self.active_player]
        msg = wrap.HeaderNew(wrap.MsgPassInformation(self.info))
        await next_player.sendServerMsg(msg)

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
            info1.storeAllPlayers.append(new_player)
            return new_player, self.game
        else:
            return None

    async def handle_client(self, reader, writer):
        buf = 2048
        player, game = self.register_player(writer)
        print("player num: " + str(player.number))
        
        msg = pickle.dumps(wrap.HeaderNew(wrap.MsgPassPlayerNum(player.number)))
        writer.write(msg)

        while self.running and player is not None:
            data = await reader.read(buf)
            msg = pickle.loads(data)
            print(msg.id)
            print("Received message: " + str(msg.data))

            if(msg.id == 1000):
                await game.start_game(player)
            elif(msg.id == 1234):
                print("Normal Message no object message")
            elif(msg.id == 102):
                playerData = msg.data.player
                await game.move(player, playerData)
            elif(msg.id == 104):
                print("here")
                print(msg.data.player.name)
                player.name = msg.data.player.name
                print(player.name)
            


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
