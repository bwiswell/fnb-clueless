import os

import pygame

import GUIConstants

import LocationSprite
import PlayerSprite

# Game board GUI pane
class ClueMap(pygame.Surface):
    def __init__(self, scaled_map_size):
        pygame.Surface.__init__(self, GUIConstants.MAP_SIZE)

        # Scaling information
        scale_x = scaled_map_size[0] / GUIConstants.MAP_SIZE[0]
        scale_y = scaled_map_size[1] / GUIConstants.MAP_SIZE[1]
        scale = (scale_x + scale_y) / 2

        # Load the background image and set its position
        background_path = os.path.dirname(os.path.realpath(__file__)) + GUIConstants.BACKGROUND_ASSET_FILE_PATH
        background_asset = pygame.image.load(background_path)
        background_asset_position = pygame.Rect(0, 0, GUIConstants.MAP_SIZE[0], GUIConstants.MAP_SIZE[1])
        self.background = pygame.Surface(GUIConstants.MAP_SIZE).convert()
        self.background.blit(background_asset, (0, 0), background_asset_position)

        # Load the room and hallway images and set their positions
        self.locations = LocationSprite.loadLocationSprites(scale)

        # Load the overlay image (walls, furniture) and set its position
        overlay_path = os.path.dirname(os.path.realpath(__file__)) + GUIConstants.OVERLAY_ASSET_FILE_PATH
        overlay_asset = pygame.image.load(overlay_path)
        overlay_asset_position = pygame.Rect(0, 0, GUIConstants.MAP_SIZE[0], GUIConstants.MAP_SIZE[1])
        self.overlay = pygame.Surface(GUIConstants.MAP_SIZE)
        self.overlay.blit(overlay_asset, (0, 0), overlay_asset_position)
        self.overlay.set_colorkey((0, 0, 5))

        self.player_sprites = {}

    # Get a player sprite by their username
    def getPlayerSprite(self, name):
        return self.player_sprites[name]

    # Assign player assets to each player
    def initPlayerSprites(self, players):
        PlayerSprite.initCharacterAssets()
        for index,player in enumerate(players):
            player_sprite = PlayerSprite.PlayerSprite(index, player.name)
            self.player_sprites[player.name] = player_sprite

    # Update the player assets to reflect current positions
    def updateLocations(self, player_locations):
        for location in self.locations.values():
            location.clearPlayers()
        for name,location in player_locations:
            self.locations[location].addPlayer(self.player_sprites[name])

    # Render the game board from background to foreground
    def draw(self, player_locations):
        drawPlayers = player_locations is not None
        self.blit(self.background, (0, 0))
        if drawPlayers:
            self.updateLocations(player_locations)
        for location in self.locations.values():
            location.draw()
            self.blit(location, location.position)
        self.blit(self.overlay, (0, 0))

    # Check for a clicked room or hallway and return its name
    def getClicked(self, position):
        for location in self.locations.values():
            if location.rect.collidepoint(position):
                return location.name.lower()
        return None