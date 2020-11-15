import os

import pygame

from Constants import BLACK, WHITE, GRAY, BLUE, GUI_FONT_PATH, LOBBY_SIZE, NAME_PROMPT, ROOM_CODE_PROMPT, START_WAIT_MESSAGE

from ClueEnums import LobbyButtons

from Drawable import Drawable, Button
from ThreadedScreen import ThreadedScreen
from Dialogues import InputDialogue

class Lobby(Drawable):
    def __init__(self):
        Drawable.__init__(self, LOBBY_SIZE, (0, 0))
        self.screen = ThreadedScreen(LOBBY_SIZE)
        pygame.display.set_caption("Clueless Lobby")
        icon = pygame.Surface((32, 32))
        icon.fill(WHITE)
        pygame.display.set_icon(icon)
        font_path = os.path.dirname(os.path.realpath(__file__)) + GUI_FONT_PATH
        self.font = pygame.font.Font(font_path, 24)
        button_offset = LOBBY_SIZE[1] // 8
        self.button_size = (LOBBY_SIZE[0] // 4, LOBBY_SIZE[1] // 6)
        self.top_pos = (self.center[0], self.center[1] - button_offset)
        self.bottom_pos = (self.center[0], self.center[1] + button_offset)
        
        background = pygame.Surface(LOBBY_SIZE)
        background.fill(BLACK)
        background_font = pygame.font.SysFont(None, 36)

        clueless_obj = background_font.render("CLUELESS: ", True, BLUE)
        digital_obj = background_font.render("THE DIGITAL BOARD GAME", True, WHITE)
        caption = pygame.Surface((clueless_obj.get_width() + digital_obj.get_width(), background_font.get_height()))
        caption.fill(BLACK)
        caption.blit(clueless_obj, (0, 0))
        caption.blit(digital_obj, (clueless_obj.get_width(), 0))

        offset = caption.get_height() * 3
        for i in range(10):
            background.blit(caption, (offset * i - offset * 14, offset * i))
            background.blit(caption, (offset * i - offset * 7, offset * i))
            background.blit(caption, (offset * i, offset * i))
            background.blit(caption, (offset * i + offset * 7, offset * i))

        self.blit(background, (0, 0))
        self.draw(self.screen)

    def getPlayerName(self):
        input_dialogue = InputDialogue(self.font, NAME_PROMPT, self.center, 8)
        input_dialogue.draw(self.screen)
        name = input_dialogue.getResponse(self.screen)
        self.draw(self.screen)
        return name

    def getLobbyType(self):
        new_button = Button(self.font.render("New Game", True, BLACK), self.top_pos, size=self.button_size)
        new_button.draw(self.screen)
        join_button = Button(self.font.render("Join Game", True, BLACK), self.bottom_pos, size=self.button_size)
        join_button.draw(self.screen)
        while True:
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if new_button.rect.collidepoint(event.pos):
                        self.draw(self.screen)
                        return LobbyButtons.NEW
                    elif join_button.rect.collidepoint(event.pos):
                        self.draw(self.screen)
                        return LobbyButtons.JOIN

    def getStart(self, room_code):
        room_code_title_obj = self.font.render("Room Code:", True, BLACK)
        room_code_obj = self.font.render(room_code, True, BLACK)
        room_code_text_size = (max(room_code_title_obj.get_width(), room_code_obj.get_width()), self.font.get_height() * 2)
        room_code_text = pygame.Surface(room_code_text_size)
        room_code_text.fill(GRAY)
        room_code_text.blit(room_code_title_obj, (room_code_text_size[0] // 2 - room_code_title_obj.get_width() // 2, 0))
        room_code_text.blit(room_code_obj, (room_code_text_size[0] // 2 - room_code_obj.get_width() // 2, self.font.get_height()))
        room_code_button = Button(room_code_text, self.top_pos, size=self.button_size)
        room_code_button.draw(self.screen)
        start_button = Button(self.font.render("Start Game", True, BLACK), self.bottom_pos, size=self.button_size)
        start_button.draw(self.screen)
        while True:
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and start_button.rect.collidepoint(event.pos):
                    return True

    def getRoomCode(self):
        input_dialogue = InputDialogue(self.font, ROOM_CODE_PROMPT, self.center, 4)
        input_dialogue.draw(self.screen)
        code = input_dialogue.getResponse(self.screen)
        self.draw(self.screen)
        return code

    def showWaitingMessage(self):
        Button(self.font.render(START_WAIT_MESSAGE, True, BLACK), self.center, size=(self.size[0] // 2, self.button_size[1])).draw(self.screen)

    def close(self):
        self.screen.close()