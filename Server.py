import os
import pickle
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
    # method called in order to begin the player 
    # turn sequence and starting the game    
    async def start_game(self, player):
        print("gmae started")
        # for player in self.players:
        #     #send out msg to all players that game is starting and allow player 1 to move
        #     pass
        if player.number == 0:
            msg = wrap.HeaderNew(wrap.MsgPassInformation(self.info))
            await player.sendServerMsg(msg)
    # Ends current players turn and sends server updated info class
    async def end_turn(self, player):
        player_count = len(self.players)
        self.active_player = (player.number + 1) % player_count

        next_player = self.players[self.active_player]
        msg = wrap.HeaderNew(wrap.MsgPassInformation(self.info))
        await next_player.sendServerMsg(msg)
    # method to updated player location for GUI to eventually see and use to
    # move the char then ends the turn
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
        self.counter = 0
        self.game = Game()
    
    # this method will create a new player based on connection 
    # anytime someone connects it will create their thread and 
    # set the char with all initial info

    def register_player(self, writer):
        
        player_count = self.counter
        print("THe player count is: " + str(player_count))
        if player_count < self.max_players:
            new_player = Player(number=player_count, writer=writer, 
                        location=info1.startLocations.pop(0))
            self.game.players.append(new_player)
            info1.storeAllPlayers.append(new_player)
            self.counter += 1
            return new_player, self.game
        else:
            return None

    async def handle_client(self, reader, writer):
        buf = 2048
        player, game = self.register_player(writer)
        print("player num: " + str(player.number))
        
        # send player its turn number after intialization.
        msg = pickle.dumps(wrap.HeaderNew(wrap.MsgPassPlayerNum(player.number)))
        writer.write(msg)

        # waits to read/ get data from client will then sort the msg wrapper
        # based on msg.id and determine what tasks need to be done
        while self.running and player is not None:
            data = await reader.read(buf)
            msg = pickle.loads(data)
            print("here " + str(msg.id))
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

    # starts server and listens for connection
    async def run(self, host, port):
        self.running = True
        server = await asyncio.start_server(
            self.handle_client, host, port
        )

        async with server:
            await server.serve_forever()

server = Server()
asyncio.run(server.run("0.0.0.0", 87))
