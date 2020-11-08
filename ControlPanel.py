import math

import pygame

import GUIConstants

from Dialogues import Button

class ControlPanel(pygame.Surface):
    def __init__(self, size, position, player_sprite, font):
        pygame.Surface.__init__(self, size)
        self.size = size
        self.position = position
        self.font = font
        self.player_sprite = player_sprite

        player_image = player_sprite.image
        player_name = self.font.render(player_sprite.name, True, GUIConstants.BLACK)

        player_image_size = player_image.get_size()
        player_image_width = (size[0] - GUIConstants.BORDER_RADIUS * 3) // 2
        player_data_width = size[0] // 2
        player_image_height = math.floor((player_image_size[1] / player_image_size[0]) * player_image_width)
        self.player_data_height = player_image_height + GUIConstants.BORDER_RADIUS * 2
        scaled_player_image_size = (player_image_width // 2, player_image_height // 2)

        left_player_data = pygame.Rect(0, 0, player_data_width, self.player_data_height)
        right_player_data = pygame.Rect(player_data_width, 0, player_data_width, self.player_data_height)

        player_image_pos = (left_player_data.centerx - scaled_player_image_size[0] // 2, left_player_data.centery - scaled_player_image_size[1] // 2)

        player_name_center = right_player_data.center
        player_name_size = player_name.get_size()
        player_name_pos = (player_name_center[0] - player_name_size[0] // 2, player_name_center[1] - player_name_size[1] // 2)

        self.button_size = (size[0], size[1] // 10)
        self.buttons = self.initButtons()

        self.fill(GUIConstants.WHITE)
        self.blit(pygame.transform.smoothscale(player_image, scaled_player_image_size), player_image_pos)
        self.blit(player_name, player_name_pos)
        pygame.draw.rect(self, GUIConstants.BLACK, left_player_data, BORDER)
        pygame.draw.rect(self, GUIConstants.BLACK, right_player_data, BORDER)
        for button in self.buttons:
            self.blit(button, button.position)

    def initButtons(self):
        buttons = []
        x = self.button_size[0] // 2
        y = self.player_data_height + self.button_size[1] // 2
        for action_text,action_id in zip(GUIConstants.ACTION_OPTION_TEXT,GUIConstants.ACTION_OPTIONS):
            buttons.append(Button(self.font, action_text, (x, y), action_id, self.button_size))
            y += self.button_size[1]
        return buttons        

    def getClicked(self, position):
        adj_pos = (position[0] - self.position[0], position[1] - self.position[1])
        for button in self.buttons:
            if button.rect.collidepoint(adj_pos):
                return button.return_value
        return None