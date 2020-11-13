import os
import pickle
from Player import Player
import Information as info
import Wrapper as wrap
from socket import *
import asyncio
from ClueEnums import Characters, Rooms, Weapons
import random


info1 = info.Information()

class PlayerClient:
    def __init__(self, number, writer):
        self.number = number
        self.writer = writer
        self.name = ''
        self.character = None

    # method to send server any msg type usinga wrapper
    async def sendMsg(self,msg):
        data_string = pickle.dumps(msg)
        self.writer.write(data_string)
        await self.writer.drain()

class Game():
    def __init__(self):
        self.info = info.Information()
        self.active_player = 0
        self.clients = []
        self.case_file, self.cards = self.initCaseFile()

    def initCaseFile(self):
        character_cards = [c for c in Characters]
        print("Num Char Cards: " + str(len(character_cards)))
        weapon_cards = [w for w in Weapons]
        print("Num Weapon Cards: " + str(len(weapon_cards)))
        room_cards = [r for r in Rooms]
        print("Num Room Cards: " + str(len(room_cards)))
        case_character = random.choice(character_cards)
        character_cards.remove(case_character)
        case_weapon = random.choice(weapon_cards)
        weapon_cards.remove(case_weapon)
        case_room = random.choice(room_cards)
        room_cards.remove(case_room)
        case_file = {"player" : case_character, "weapon" : case_weapon, "location" : case_room}
        character_cards.append(weapon_cards)
        character_cards.append(room_cards)
        return case_file, character_cards

    # method called in order to begin the player 
    # turn sequence and starting the game    
    async def start_game(self, client):
        print("game started")
        writes = []
        for client in self.clients:      
            msg = wrap.HeaderNew(wrap.MsgGameStart(client.character,info1))
            writes.append(client.sendMsg(msg))
            #send out msg to all players that game is starting and allow player 1 to move

        await asyncio.gather(*writes)

        if client.number == 0:
            msg = wrap.HeaderNew(wrap.MsgPassInformation(self.info))
            await client.sendMsg(msg)

    # Ends current players turn and sends server updated info class
    async def end_turn(self, client):
        player_count = len(self.clients)
        self.active_player = (client.number + 1) % player_count

        next_player = self.clients[self.active_player]
        msg = wrap.HeaderNew(wrap.MsgPassInformation(self.info))
        await next_player.sendMsg(msg)
    # method to updated player location for GUI to eventually see and use to
    # move the char then ends the turn
    async def move(self, client, data):
        if client.number == self.active_player:
            print("server: " +str(data.location))
            print("server: " + str(data.name))
            self.info.updateCurrentLocation(data)
            locations = self.info.getCurrentLocations()
            msg = wrap.MsgUpdateGame(self.info)
            print("server:" + str(locations))
            
            await self.end_turn(client)

    def assign_cards(self):
        cards = []
        for i in range(3):
            rand_card = random.choice(self.cards)
            self.cards.remove(rand_card)
            cards.append(rand_card)
        return cards

class Server():

    def __init__(self):
        
        self.running = False
        self.max_players = 4
        self.counter = 0
        self.game = Game()
    
    # this method will create a new player based on connection 
    # anytime someone connects it will create their thread and 
    # set the char with all initial info
    def register_player(self, writer, name):
        player_count = self.counter
        print("Server:The player count is: " + str(player_count))
        if player_count < self.max_players:
            client = PlayerClient(number=player_count, writer=writer)
            self.game.clients.append(client)
            character = Player(name=name, number=client.number, location=info1.startLocations.pop(0), 
                            character=Characters(client.number), cards=self.game.assign_cards())
            info1.storeAllPlayers.append(character)
            client.character = character
            self.counter += 1
            return client, self.game
        else:
            return None

    async def handle_client(self, reader, writer):
        buf = 2048
        data = await reader.read(buf)
        msg = pickle.loads(data)
        print("Server:player name: " + str(msg.data.player.name))
        client, game = self.register_player(writer, msg.data.player.name)
        print("Server:player num: " + str(client.number))
        
        # send player its turn number after intialization.
        msg = wrap.HeaderNew(wrap.MsgPassPlayerNum(client.number,client.character))
        await client.sendMsg(msg)

        # waits to read/ get data from client will then sort the msg wrapper
        # based on msg.id and determine what tasks need to be done
        while self.running and client is not None:
            data = await reader.read(buf)
            msg = pickle.loads(data)
            print("Server recieved " + str(msg.id))
            print("Received message: " + str(msg.data))

            if(msg.id == 1000):
                await game.start_game(client)
            elif(msg.id == 1234):
                print("Normal Message no object message")
            elif(msg.id == 102):
                playerData = msg.data.player
                await game.move(client, playerData)
            elif(msg.id == 104):
                print("here")
                print("server: " + str(msg.data.player.name))
                client.name = msg.data.player.name
                print(client.name)
            
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
