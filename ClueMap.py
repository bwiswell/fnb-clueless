import pygame
import os
import LocationSprite
from PlayerSprite import PlayerSprite

BACKGROUND_FILE_PATH = "\\assets\\background_asset.png"
OVERLAY_FILE_PATH = "\\assets\\overlay_asset.png"

# Game board GUI pane
class ClueMap(pygame.Surface):
    def __init__(self, size):
        pygame.Surface.__init__(self, size)
        self.size = size

        # Load the background image and set its position
        background_path = os.path.dirname(os.path.realpath(__file__)) + BACKGROUND_FILE_PATH
        background_asset = pygame.image.load(background_path)
        background_asset_position = pygame.Rect(0, 0, size[0], size[1])
        self.background = pygame.Surface(size).convert()
        self.background.blit(background_asset, (0, 0), background_asset_position)

        # Load the room and hallway images and set their positions
        self.locations = LocationSprite.loadLocationSprites()

        # Load the overlay image (walls, furniture) and set its position
        overlay_path = os.path.dirname(os.path.realpath(__file__)) + OVERLAY_FILE_PATH
        overlay_asset = pygame.image.load(overlay_path)
        overlay_asset_position = pygame.Rect(0, 0, size[0], size[1])
        self.overlay = pygame.Surface(size).convert()
        self.overlay.blit(overlay_asset, (0, 0), overlay_asset_position)
        self.overlay.set_colorkey((0, 0, 5))

        self.player_sprites = None

    # Assign player assets to each player
    def initPlayerSprites(self, ip_list):
        sprite_dict = {}
        for index,ip in enumerate(ip_list):
            sprite_dict[ip] = PlayerSprite(index)
        self.player_sprites = sprite_dict

    # Update the player assets to reflect current positions
    def updateLocations(self, player_locations):
        if self.player_sprites is None:
            self.initPlayerSprites([ip for ip,location in player_locations])
        for location in self.locations:
            location.clearPlayers()
        for ip,location in player_locations:
            self.locations[location].addPlayer(self.player_sprites[ip])

    # Render the game board from background to foreground
    def draw(self, player_locations, debug=False, font=None):
        self.blit(self.background, (0, 0))
        self.updateLocations(player_locations)
        for location in self.locations:
            location.draw(debug, font)
            self.blit(location, location.position)
        self.blit(self.overlay, (0, 0))

    # Check for a clicked room or hallway and return its name
    def getClicked(self, position):
        for location in self.locations:
            if location.rect.collidepoint(position):
                return location.name
        return None