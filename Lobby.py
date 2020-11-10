from ctypes import windll, c_int

import pygame

import GUIConstants

from ThreadedScreen import ThreadedScreen
from Dialogues import InputDialogue, GUIMessage, Button

class Lobby(pygame.Surface):
    def __init__(self):
        windll.shcore.SetProcessDpiAwareness(c_int(1))
        pygame.init()
        self.screen = ThreadedScreen((800, 600))
        pygame.Surface.__init__(self, self.screen.get_size())
        self.position = (0, 0)
        self.fill(GUIConstants.BLACK)
        self.center = (self.get_width() // 2, self.get_height() // 2)
        self.font = pygame.font.SysFont(None, 24)
        self.screen.draw(self)

    def getPlayerName(self):
        input_dialogue = InputDialogue(self.font, GUIConstants.NAME_PROMPT, self.center, 8)
        self.screen.draw(input_dialogue)
        name = input_dialogue.getResponse(self.screen)
        self.screen.draw(self)
        self.screen.draw(GUIMessage(self.font, GUIConstants.START_MESSAGE, self.center))
        return name

    def giveStartButton(self):
        start = Button(self.font, "Start Game", self.center, True, (self.get_width() // 4, self.get_height() // 4))
        self.screen.draw(start)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and start.rect.collidepoint(event.pos):
                    return

    def close(self):
        self.screen.close()
        