import pygame
from Dialogues import Button

ACTION_OPTIONS = ["Move", "Suggest", "Accuse", "End Turn"]

WHITE = (255, 255, 255)

class ControlPanel(pygame.Surface):
    def __init__(self, size, position, font):
        pygame.Surface.__init__(self, size)
        self.position = position
        self.font = font
        self.button_size = (size[0], size[1] // 10)
        self.buttons = self.initButtons()

    def initButtons(self):
        buttons = []
        x = self.button_size[0] // 2
        y = self.button_size[1] // 2
        for action in ACTION_OPTIONS:
            return_value = action.lower().replace(" ", "")
            buttons.append(Button(self.font, action, (x, y), return_value, self.button_size))
            y += self.button_size[1]
        return buttons

    def draw(self):
        self.fill(WHITE)
        for button in self.buttons:
            self.blit(button, button.position)

    def getClicked(self, position):
        adj_pos = (position[0] - self.position[0], position[1] - self.position[1])
        for button in self.buttons:
            if button.rect.collidepoint(adj_pos):
                return button.return_value
        return None