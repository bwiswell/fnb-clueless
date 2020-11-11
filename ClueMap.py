import os

import pygame

from Constants import BACKGROUND_ASSET_FILE_PATH, OVERLAY_ASSET_FILE_PATH, MAP_SIZE

from Drawable import Drawable

import LocationSprite
import PlayerSprite

# Game board GUI pane
class ClueMap(Drawable):
    def __init__(self, scaled_map_size):
        Drawable.__init__(self, scaled_map_size, (0, 0))
        self.clue_map = pygame.Surface(MAP_SIZE)

        # Scaling information
        scale_x = scaled_map_size[0] / MAP_SIZE[0]
        scale_y = scaled_map_size[1] / MAP_SIZE[1]
        scale = (scale_x + scale_y) / 2

        # Load the background image and set its position
        background_path = os.path.dirname(os.path.realpath(__file__)) + BACKGROUND_ASSET_FILE_PATH
        background_asset = pygame.image.load(background_path)
        background_asset_position = pygame.Rect(self.position, MAP_SIZE)
        self.background = pygame.Surface(MAP_SIZE).convert()
        self.background.blit(background_asset, (0, 0), background_asset_position)

        # Load the room and hallway images and set their positions
        self.locations = LocationSprite.initLocationSprites(scale)

        # Load the overlay image (walls, furniture) and set its position
        overlay_path = os.path.dirname(os.path.realpath(__file__)) + OVERLAY_ASSET_FILE_PATH
        overlay_asset = pygame.image.load(overlay_path)
        overlay_asset_position = pygame.Rect(self.position, MAP_SIZE)
        self.overlay = pygame.Surface(MAP_SIZE)
        self.overlay.blit(overlay_asset, (0, 0), overlay_asset_position)
        self.overlay.set_colorkey((0, 0, 5))

        self.player_sprites = {}

    # Assign player assets to each player
    def initPlayerSprites(self, players):
        self.player_sprites = PlayerSprite.initPlayerSprites(players)

    # Get a player sprite from a Characters enum member
    def getPlayerSprite(self, character):
        return self.player_sprites[character]

    # Update the player assets to reflect current positions
    def updateLocations(self, player_locations):
        for location in self.locations.values():
            location.clearPlayers()
        for name,location in player_locations:
            self.locations[location].addPlayer(self.player_sprites[name])

    def update(self, player_locations):
        self.clue_map.blit(self.background, (0, 0))
        if player_locations is not None:
            self.updateLocations(player_locations)
        for location in self.locations.values():
            location.update()
            location.draw(self.clue_map)
        self.clue_map.blit(self.overlay, (0, 0))
        self.blit(pygame.transform.smoothscale(self.clue_map, self.size), (0, 0))

    # Check for a clicked room or hallway and return its name
    def getClicked(self, click_pos):
        adj_pos = (click_pos[0] - self.position[0], click_pos[1] - self.position[1])
        for loc_id,location in self.locations.items():
            if location.collision_box.collidepoint(adj_pos):
                return loc_id
        return None