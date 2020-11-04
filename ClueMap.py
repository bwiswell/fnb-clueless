import os

import pygame

import LocationSprite
import PlayerSprite

BACKGROUND_FILE_PATH = "\\assets\\background_asset.png"
OVERLAY_FILE_PATH = "\\assets\\overlay_asset.png"

MAP_SIZE = (1152, 896)

# Game board GUI pane
class ClueMap(pygame.Surface):
    def __init__(self):
        pygame.Surface.__init__(self, MAP_SIZE)

        # Load the background image and set its position
        background_path = os.path.dirname(os.path.realpath(__file__)) + BACKGROUND_FILE_PATH
        background_asset = pygame.image.load(background_path)
        background_asset_position = pygame.Rect(0, 0, MAP_SIZE[0], MAP_SIZE[1])
        self.background = pygame.Surface(MAP_SIZE).convert()
        self.background.blit(background_asset, (0, 0), background_asset_position)

        # Load the room and hallway images and set their positions
        self.locations = LocationSprite.loadLocationSprites()

        # Load the overlay image (walls, furniture) and set its position
        overlay_path = os.path.dirname(os.path.realpath(__file__)) + OVERLAY_FILE_PATH
        overlay_asset = pygame.image.load(overlay_path)
        overlay_asset_position = pygame.Rect(0, 0, MAP_SIZE[0], MAP_SIZE[1])
        self.overlay = pygame.Surface(MAP_SIZE)
        self.overlay.blit(overlay_asset, (0, 0), overlay_asset_position)
        self.overlay.set_colorkey((0, 0, 5))

        self.players_by_ip = None
        self.players_by_name = None

    # Get a player sprite by their IP
    def getPlayerSpriteByIP(self, ip):
        return self.players_by_ip[ip]

    # Get a player sprite by their username
    def getPlayerSpriteByName(self, name):
        return self.players_by_name[name]

    # Assign player assets to each player
    def initPlayerSprites(self, players):
        PlayerSprite.initCharacterAssets()
        ip_dict = {}
        name_dict = {}
        for index,player in enumerate(players):
            player_sprite = PlayerSprite.PlayerSprite(index, player.ip, player.name)
            ip_dict[player.ip] = player_sprite
            name_dict[player.name] = player_sprite
        self.players_by_ip = ip_dict
        self.players_by_name = name_dict

    # Update the player assets to reflect current positions
    def updateLocations(self, player_locations):
        for location in self.locations:
            location.clearPlayers()
        for ip,location in player_locations:
            self.locations[location].addPlayer(self.players_by_ip[ip])

    # Render the game board from background to foreground
    def draw(self, player_locations):
        drawPlayers = player_locations is not None
        self.blit(self.background, (0, 0))
        if drawPlayers:
            self.updateLocations(player_locations)
        for location in self.locations:
            location.draw()
            self.blit(location, location.position)
        self.blit(self.overlay, (0, 0))


    # Check for a clicked room or hallway and return its name
    def getClicked(self, position):
        for location in self.locations:
            if location.rect.collidepoint(position):
                return location.name
        return None