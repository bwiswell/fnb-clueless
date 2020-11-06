import os
import json

import pygame

# Asset sizes
ROOM_SIZE = (256, 192)
H_HALLWAY_SIZE = (160, 64)
V_HALLWAY_SIZE = (64, 128)

# Caption position offset
CAPTION_OFFSET = (7, 14)

# Player positions within locations
ROOM_PLAYER_OFFSETS = [(64, 32), (128, 32), (64, 96), (128, 96)]
H_HALLWAY_PLAYER_OFFSET = (48, 0)
V_HALLWAY_PLAYER_OFFSET = (0, 32)

# Colors
GRAY = (191, 191, 191)
BLACK = (0, 0, 0)

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
    def __init__(self, loc_id, name, image, position, size, collisionBox):
        pygame.Surface.__init__(self, size, pygame.SRCALPHA)
        self.convert()
        self.loc_id = loc_id
        self.name = name
        self.image = image
        self.position = position
        self.rect = collisionBox

    def clearPlayers(self):
        raise NotImplementedError

    def addPlayer(self, player):
        raise NotImplementedError

    def drawPlayers(self):
        raise NotImplementedError

    def draw(self):
        self.blit(self.image, (0, 0))

# Subclass of LocationSprite for rooms
class RoomSprite(LocationSprite):
    def __init__(self, loc_id, name, image, position, collisionBox, caption):
        size = (ROOM_SIZE[0] + CAPTION_OFFSET[0], ROOM_SIZE[1] + CAPTION_OFFSET[1] + caption.get_size()[1])
        LocationSprite.__init__(self, loc_id, name, image, position, size, collisionBox)
        self.caption = caption
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

    # Draws the room, room caption, and any players in the room
    def draw(self):
        LocationSprite.draw(self)
        self.blit(self.caption, (160 + CAPTION_OFFSET[0], ROOM_SIZE[1] + CAPTION_OFFSET[1]))
        self.drawPlayers()

# Subclass of LocationSprite for hallways
class HallwaySprite(LocationSprite):
    def __init__(self, loc_id, name, image, position, size, collisionBox, player_offset):
        LocationSprite.__init__(self, loc_id, name, image, position, size, collisionBox)
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

    # Draws the hallway and and any players in the hallway
    def draw(self):
        LocationSprite.draw(self)
        self.drawPlayers()

# Loads all location sprites and returns them as an (id, locationSprite) dictionary
def loadLocationSprites(scale):
    font = pygame.font.SysFont(None, 16)
    location_data_path = os.path.dirname(os.path.realpath(__file__)) + DATA_FILE_PATH
    with open(location_data_path) as data_file:
        location_data = json.load(data_file)
    asset_path = os.path.dirname(os.path.realpath(__file__)) + ASSET_FILE_PATH
    asset_sheet = pygame.image.load(asset_path)
    location_sprites = {}

    for index,data_dict in enumerate(location_data):
        asset_pos = tuple(int(num) for num in data_dict["asset"].replace('(', '').replace(')', '').split(', '))
        position = tuple(int(num) for num in data_dict["position"].replace('(', '').replace(')', '').split(', '))
        if data_dict["type"] == "room":
            caption_text = font.render(data_dict["name"], True, BLACK)
            text_height = caption_text.get_size()[1]
            caption = pygame.Surface((96, text_height + 2))
            caption.fill(GRAY)
            pygame.draw.rect(caption, BLACK, pygame.Rect(0, 0, 96, text_height + 2), 1)
            caption.blit(caption_text, (48 - caption_text.get_size()[0] // 2, 1))
            image = pygame.Surface(ROOM_SIZE).convert()
            image.blit(asset_sheet, (0, 0), pygame.Rect(asset_pos, ROOM_SIZE))
            collisionPos = (position[0] * scale, position[1] * scale)
            collisionSize = (ROOM_SIZE[0] * scale, ROOM_SIZE[1] * scale)
            collisionBox = pygame.Rect(collisionPos, collisionSize)
            location_sprites[data_dict["name"].lower()] = RoomSprite(index, data_dict["name"], image, position, collisionBox, caption)
        elif data_dict["type"] == "horizontal":
            image = pygame.Surface(H_HALLWAY_SIZE).convert()
            image.blit(asset_sheet, (0, 0), pygame.Rect(asset_pos, H_HALLWAY_SIZE))
            collisionPos = (position[0] * scale, position[1] * scale)
            collisionSize = (H_HALLWAY_SIZE[0] * scale, H_HALLWAY_SIZE[1] * scale)
            collisionBox = pygame.Rect(collisionPos, collisionSize)
            location_sprites[data_dict["name"].lower()] = HallwaySprite(index, data_dict["name"], image, position, H_HALLWAY_SIZE, collisionBox, H_HALLWAY_PLAYER_OFFSET)
        else:
            image = pygame.Surface(V_HALLWAY_SIZE).convert()
            image.blit(asset_sheet, (0, 0), pygame.Rect(asset_pos, V_HALLWAY_SIZE))
            collisionPos = (position[0] * scale, position[1] * scale)
            collisionSize = (V_HALLWAY_SIZE[0] * scale, V_HALLWAY_SIZE[1] * scale)
            collisionBox = pygame.Rect(collisionPos, collisionSize)
            location_sprites[data_dict["name"].lower()] = HallwaySprite(index, data_dict["name"], image, position, V_HALLWAY_SIZE, collisionBox, V_HALLWAY_PLAYER_OFFSET)

    return location_sprites