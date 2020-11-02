import os
import json

import pygame

# Asset sizes
ROOM_SIZE = (192, 192)
H_HALLWAY_SIZE = (128, 64)
V_HALLWAY_SIZE = (64, 128)

# Player positions within locations
ROOM_PLAYER_OFFSETS = [(64, 64), (96, 64), (64, 96), (96, 96)]
H_HALLWAY_PLAYER_OFFSET = (48, 16)
V_HALLWAY_PLAYER_OFFSET = (16, 48)

# Colors
RED = (255, 0, 0)

# Assets filename
DATA_FILE_PATH = "\\assets\\location_assets_data.json"
ASSET_FILE_PATH = "\\assets\\location_assets.png"

# Basic Exception to be raised when too many players
# are in one location
class RoomOverflowError(Exception):
    def __init__(self):
        print("Too many players in a room!")

# Base class for all locations
class LocationSprite(pygame.Surface):
    def __init__(self, loc_id, name, image, position, size):
        pygame.Surface.__init__(self, size)
        self.loc_id = loc_id
        self.name = name
        self.image = image
        self.position = position

    def clearPlayers(self):
        raise NotImplementedError

    def addPlayer(self, player):
        raise NotImplementedError

    def drawPlayers(self):
        raise NotImplementedError
 
    def drawText(self, font):
        text_object = font.render(self.name, True, RED)
        text_x = self.get_size()[0] // 2 - text_object.get_size()[0] // 2
        text_y = self.get_size()[1] // 2 - text_object.get_size()[1] // 2
        self.blit(text_object, (text_x, text_y))

    def draw(self, debug=False, font=None):
        self.blit(self.image, (0, 0))
        if debug:
            self.drawText(font)

# Subclass of LocationSprite for rooms
class RoomSprite(LocationSprite):
    def __init__(self, loc_id, name, image, position):
        LocationSprite.__init__(self, loc_id, name, image, position, ROOM_SIZE)
        self.players = []

    def clearPlayers(self):
        self.players = []

    def addPlayer(self, player):
        if len(self.players) >= 4:
            raise RoomOverflowError
        self.players.append(player)

    def drawPlayers(self):
        for index, player in enumerate(self.players):
            self.blit(player, ROOM_PLAYER_OFFSETS[index])

    def draw(self, debug=False, font=None):
        LocationSprite.draw(self, debug, font)
        self.drawPlayers()

# Subclass of LocationSprite for hallways
class HallwaySprite(LocationSprite):
    def __init__(self, loc_id, name, image, position, size, player_offset):
        LocationSprite.__init__(self, loc_id, name, image, position, size)
        self.player = None
        self.player_offset = player_offset

    def clearPlayers(self):
        self.player = None

    def addPlayer(self, player):
        if self.player is not None:
            raise RoomOverflowError
        self.player = player

    def drawPlayers(self):
        if self.player is not None:
            self.blit(self.player, self.player_offset)

    def draw(self, debug=False, font=None):
        LocationSprite.draw(self, debug, font)
        self.drawPlayers()

def loadLocationSprites():
    location_data_path = os.path.dirname(os.path.realpath(__file__)) + DATA_FILE_PATH
    with open(location_data_path) as data_file:
        location_data = json.load(data_file)
    asset_path = os.path.dirname(os.path.realpath(__file__)) + ASSET_FILE_PATH
    asset_sheet = pygame.image.load(asset_path).convert()
    location_sprites = []

    for index,data_dict in enumerate(location_data):
        asset_pos = tuple(int(num) for num in data_dict["asset"].replace('(', '').replace(')', '').split(', '))
        position = tuple(int(num) for num in data_dict["position"].replace('(', '').replace(')', '').split(', '))
        if data_dict["type"] == "room":
            image = pygame.Surface(ROOM_SIZE).convert()
            image.blit(asset_sheet, (0, 0), pygame.Rect(asset_pos, ROOM_SIZE))
            location_sprites.append(RoomSprite(index, data_dict["name"], image, position))
        elif data_dict["type"] == "horizontal":
            image = pygame.Surface(H_HALLWAY_SIZE).convert()
            image.blit(asset_sheet, (0, 0), pygame.Rect(asset_pos, H_HALLWAY_SIZE))
            location_sprites.append(HallwaySprite(index, data_dict["name"], image, position, H_HALLWAY_SIZE, H_HALLWAY_PLAYER_OFFSET))
        else:
            image = pygame.Surface(V_HALLWAY_SIZE).convert()
            image.blit(asset_sheet, (0, 0), pygame.Rect(asset_pos, V_HALLWAY_SIZE))
            location_sprites.append(HallwaySprite(index, data_dict["name"], image, position, V_HALLWAY_SIZE, V_HALLWAY_PLAYER_OFFSET))

    return location_sprites