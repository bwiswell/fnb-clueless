import os

import pygame

import GUIConstants

character_assets = []
font = None

# Loads all character assets from file and initializes the font
def initCharacterAssets():
    global character_assets, font
    asset_path = os.path.dirname(os.path.realpath(__file__)) + GUIConstants.CHARACTER_ASSET_FILE_PATH
    character_sheet = pygame.image.load(asset_path)
    for i in range(GUIConstants.NUM_CHARACTERS):
        character = pygame.Surface(GUIConstants.CHARACTER_ASSET_SIZE, pygame.SRCALPHA)
        character_asset_pos = (0, GUIConstants.CHARACTER_ASSET_SIZE[1] * i)
        character_asset_rect = pygame.Rect(character_asset_pos, GUIConstants.CHARACTER_ASSET_SIZE)
        character.blit(character_sheet, (0, 0), character_asset_rect)
        character_assets.append(character)
    font = pygame.font.SysFont(None, GUIConstants.CHARACTER_NAME_FONT_SIZE)

# Basic player Sprite class consisting of a player image and username caption
class PlayerSprite(pygame.Surface):
    def __init__(self, index, name):
        pygame.Surface.__init__(self, GUIConstants.CHARACTER_ASSET_SIZE, pygame.SRCALPHA)
        self.convert()
        self.name = name

        self.image = pygame.Surface(GUIConstants.CHARACTER_ASSET_SIZE, pygame.SRCALPHA)
        self.image.blit(character_assets[index], (0, -6))
        
        self.blit(character_assets[index], (0, 0))
        text_object = font.render(name, True, GUIConstants.WHITE)
        text_x = self.get_width() // 2 - text_object.get_width() // 2
        self.blit(text_object, (text_x, 0))
