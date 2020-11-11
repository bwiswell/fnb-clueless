import pygame

import GUIConstants

from Lobby import Lobby
from ClueGUI import ClueGUI

lobby = Lobby()

name = lobby.getPlayerName()

class Player:
    def __init__(self, name, location, cards):
        self.name = name
        self.location = location
        self.cards = cards

class Card(pygame.Surface):
    def __init__(self, text_obj):
        pygame.Surface.__init__(self, (150, 200))
        self.fill(GUIConstants.WHITE)
        self.blit(text_obj, (self.get_width() // 2 - text_obj.get_width(), self.get_height() // 2 - text_obj.get_height() // 2))

font = pygame.font.SysFont(None, 24)
cards = []
for i in range(3):
    text_obj = font.render(str(i), True, GUIConstants.BLACK)
    cards.append(Card(text_obj))

player = Player(name, "library", cards)

lobby.giveStartButton()

gui = ClueGUI(player, [player])

gui.getPlayerAction(["move"])