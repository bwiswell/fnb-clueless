import pygame

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
TEAL = (0, 255, 255)

PLAYER_COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE, TEAL]

class PlayerSprite(pygame.Surface):
    def __init__(self, index):
        pygame.Surface.__init__(self, (32, 32), pygame.SRCALPHA)
        pygame.draw.circle(self, PLAYER_COLORS[index], (16, 16), 16)