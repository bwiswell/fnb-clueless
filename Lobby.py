from ctypes import windll, c_int

import pygame

from Constants import LOBBY_SIZE, BLACK, NAME_PROMPT, START_MESSAGE, START_BUTTON_TEXT

from Drawable import Drawable, Button
from ThreadedScreen import ThreadedScreen
from Dialogues import InputDialogue, GUIMessage

class Lobby(Drawable):
    def __init__(self):
        windll.shcore.SetProcessDpiAwareness(c_int(1))
        pygame.init()
        Drawable.__init__(self, LOBBY_SIZE, (0, 0))
        self.screen = ThreadedScreen(LOBBY_SIZE)
        self.fill(BLACK)
        self.font = pygame.font.SysFont(None, 24)
        self.draw(self.screen)

    def getPlayerName(self):
        input_dialogue = InputDialogue(self.font, NAME_PROMPT, self.center, 8)
        input_dialogue.draw(self.screen)
        name = input_dialogue.getResponse(self.screen)
        self.draw(self.screen)
        GUIMessage(self.font, START_MESSAGE, self.center).draw(self.screen)
        return name

    def giveStartButton(self):
        start = Button(self.font.render(START_BUTTON_TEXT, True, BLACK), self.center, size=(self.get_width() // 4, self.get_height() // 4))
        start.draw(self.screen)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and start.rect.collidepoint(event.pos):
                    return

    def close(self):
        self.screen.close()
        