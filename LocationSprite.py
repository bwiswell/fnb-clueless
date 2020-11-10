import os
import json

import pygame

import GUIConstants

# Basic Exception to be raised when too many players are in one location
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
        size = (GUIConstants.ROOM_SIZE[0] + GUIConstants.ROOM_CAPTION_OFFSET[0], GUIConstants.ROOM_SIZE[1] + GUIConstants.ROOM_CAPTION_OFFSET[1] + caption.get_size()[1])
        LocationSprite.__init__(self, loc_id, name, image, position, size, collisionBox)
        self.caption = caption
        self.players = []

    # Empties the list of players currently in the room
    def clearPlayers(self):
        self.players = []

    # Adds a player to the room if there are less than 4 currently
    # in it
    def addPlayer(self, player):
        if len(self.players) >= 4:
            raise RoomOverflowError
        self.players.append(player)

    # Renders the players currently in the room
    def drawPlayers(self):
        for index, player in enumerate(self.players):
            self.blit(player, GUIConstants.ROOM_PLAYER_OFFSETS[index])

    # Draws the room, room caption, and any players in the room
    def draw(self):
        LocationSprite.draw(self)
        self.blit(self.caption, (160 + GUIConstants.ROOM_CAPTION_OFFSET[0], GUIConstants.ROOM_SIZE[1] + GUIConstants.ROOM_CAPTION_OFFSET[1]))
        self.drawPlayers()

# Subclass of LocationSprite for hallways
class HallwaySprite(LocationSprite):
    def __init__(self, loc_id, name, image, position, size, collisionBox, player_offset):
        LocationSprite.__init__(self, loc_id, name, image, position, size, collisionBox)
        self.player = None
        self.player_offset = player_offset

    # Removes any player currently in the hallway
    def clearPlayers(self):
        self.player = None

    # Adds a player to the hallway if there is not one already
    def addPlayer(self, player):
        if self.player is not None:
            raise RoomOverflowError
        self.player = player

    # Renders a player in the hallway
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
    location_data_path = os.path.dirname(os.path.realpath(__file__)) + GUIConstants.LOCATION_DATA_FILE_PATH
    with open(location_data_path) as data_file:
        location_data = json.load(data_file)
    asset_path = os.path.dirname(os.path.realpath(__file__)) + GUIConstants.LOCATION_ASSET_FILE_PATH
    asset_sheet = pygame.image.load(asset_path)
    location_sprites = {}

    for index,data_dict in enumerate(location_data):
        asset_pos = tuple(int(num) for num in data_dict["asset"].replace('(', '').replace(')', '').split(', '))
        position = tuple(int(num) for num in data_dict["position"].replace('(', '').replace(')', '').split(', '))
        if data_dict["type"] == "room":
            caption_text = font.render(data_dict["name"], True, GUIConstants.BLACK)
            text_height = caption_text.get_size()[1]
            caption = pygame.Surface((96, text_height + 2))
            caption.fill(GUIConstants.GRAY)
            pygame.draw.rect(caption, GUIConstants.BLACK, pygame.Rect(0, 0, 96, text_height + 2), 1)
            caption.blit(caption_text, (48 - caption_text.get_size()[0] // 2, 1))
            image = pygame.Surface(GUIConstants.ROOM_SIZE).convert()
            image.blit(asset_sheet, (0, 0), pygame.Rect(asset_pos, GUIConstants.ROOM_SIZE))
            collisionPos = (position[0] * scale, position[1] * scale)
            collisionSize = (GUIConstants.ROOM_SIZE[0] * scale, GUIConstants.ROOM_SIZE[1] * scale)
            collisionBox = pygame.Rect(collisionPos, collisionSize)
            location_sprites[data_dict["name"].lower()] = RoomSprite(index, data_dict["name"], image, position, collisionBox, caption)
        elif data_dict["type"] == "horizontal":
            image = pygame.Surface(GUIConstants.H_HALLWAY_SIZE).convert()
            image.blit(asset_sheet, (0, 0), pygame.Rect(asset_pos, GUIConstants.H_HALLWAY_SIZE))
            collisionPos = (position[0] * scale, position[1] * scale)
            collisionSize = (GUIConstants.H_HALLWAY_SIZE[0] * scale, GUIConstants.H_HALLWAY_SIZE[1] * scale)
            collisionBox = pygame.Rect(collisionPos, collisionSize)
            location_sprites[data_dict["name"].lower()] = HallwaySprite(index, data_dict["name"], image, position, GUIConstants.H_HALLWAY_SIZE, collisionBox, GUIConstants.H_HALLWAY_PLAYER_OFFSET)
        else:
            image = pygame.Surface(GUIConstants.V_HALLWAY_SIZE).convert()
            image.blit(asset_sheet, (0, 0), pygame.Rect(asset_pos, GUIConstants.V_HALLWAY_SIZE))
            collisionPos = (position[0] * scale, position[1] * scale)
            collisionSize = (GUIConstants.V_HALLWAY_SIZE[0] * scale, GUIConstants.V_HALLWAY_SIZE[1] * scale)
            collisionBox = pygame.Rect(collisionPos, collisionSize)
            location_sprites[data_dict["name"].lower()] = HallwaySprite(index, data_dict["name"], image, position, GUIConstants.V_HALLWAY_SIZE, collisionBox, GUIConstants.V_HALLWAY_PLAYER_OFFSET)

    return location_sprites