import os

import pygame

# Colors
WHITE = (255, 255, 255)

# Assets filename
ASSET_FILE_PATH = "\\assets\\character_assets.png"

# Character asset info
NUM_CHARACTERS = 4
CHARACTER_SIZE = (64, 64)
character_assets = []

# Font info
FONT_SIZE = 18
font = None

def initCharacterAssets():
    global character_assets, font
    asset_path = os.path.dirname(os.path.realpath(__file__)) + ASSET_FILE_PATH
    character_sheet = pygame.image.load(asset_path)
    for i in range(NUM_CHARACTERS):
        character = pygame.Surface(CHARACTER_SIZE, pygame.SRCALPHA)
        character_asset_pos = (0, CHARACTER_SIZE[1] * i)
        character_asset_rect = pygame.Rect(character_asset_pos, CHARACTER_SIZE)
        character.blit(character_sheet, (0, 0), character_asset_rect)
        character_assets.append(character)
    font = pygame.font.SysFont(None, FONT_SIZE)

class PlayerSprite(pygame.Surface):
    def __init__(self, index, ip, name):
        pygame.Surface.__init__(self, CHARACTER_SIZE, pygame.SRCALPHA)
        self.convert()
        self.blit(character_assets[index], (0, 0))
        self.ip = ip
        self.name = name
        text_object = font.render(name, True, WHITE)
        text_x = 32 - text_object.get_size()[0] // 2
        self.blit(text_object, (text_x, 0))