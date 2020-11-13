import math

import pygame

from Constants import WHITE, MID_GRAY, BLACK, RED, BORDER_RADIUS, ACTION_OPTION_TEXT

from ClueEnums import Actions

from Drawable import Selectable, GrayOut, Button

class ControlPanel(Selectable):
    def __init__(self, size, position, player, player_sprite, cards, font):
        Selectable.__init__(self, size, position)
        self.fill(MID_GRAY)

        # Player data (image and name) sizes and positions
        player_image = player_sprite.image
        player_name = font.render(player.name, True, BLACK)
        player_character = font.render(player.character.text, True, BLACK)
        player_info = pygame.Surface((max(player_name.get_width(), player_character.get_width()), player_name.get_height() + player_character.get_height()), pygame.SRCALPHA)
        player_info.blit(player_name, (player_info.get_width() // 2 - player_name.get_width() // 2, 0))
        player_info.blit(player_character, (player_info.get_width() // 2 - player_character.get_width() // 2, player_name.get_height()))

        image_width = size[0] // 4
        data_width = image_width * 2
        data_height = (player_image.get_height() // player_image.get_width()) * image_width

        left_data = pygame.Rect(0, 0, data_width, data_height)
        right_data = pygame.Rect(data_width, 0, data_width, data_height)

        player_image_pos = (left_data.centerx - image_width // 2, left_data.centery - data_height // 2)
        player_info_pos = (right_data.centerx - player_info.get_width() // 2, right_data.centery - player_info.get_height() // 2)

        # Render player data
        pygame.draw.rect(self, BLACK, left_data, BORDER_RADIUS)
        pygame.draw.rect(self, BLACK, right_data, BORDER_RADIUS)
        self.blit(pygame.transform.smoothscale(player_image, (image_width, data_height)), player_image_pos)
        self.blit(player_info, player_info_pos)

        # Player cards sizes and positions
        card_width = (size[0] - BORDER_RADIUS * 4) // 3
        card_height = 4 * (card_width // 3)
        card_slot_width = card_width + BORDER_RADIUS * 2
        card_slot_height = card_height + BORDER_RADIUS * 2

        card_slot_y = data_height
        left_slot = pygame.Rect(0, card_slot_y, card_slot_width, card_slot_height)
        center_slot = pygame.Rect(card_slot_width, card_slot_y, card_slot_width, card_slot_height)
        right_slot = pygame.Rect(card_slot_width * 2, card_slot_y, card_slot_width, card_slot_height)

        card_y = card_slot_y + BORDER_RADIUS
        left_card_pos = (left_slot.x + BORDER_RADIUS, card_y)
        center_card_pos = (center_slot.x + BORDER_RADIUS, card_y)
        right_card_pos = (right_slot.x + BORDER_RADIUS, card_y)

        # Render player cards
        pygame.draw.rect(self, BLACK, left_slot, BORDER_RADIUS)
        pygame.draw.rect(self, BLACK, center_slot, BORDER_RADIUS)
        pygame.draw.rect(self, BLACK, right_slot, BORDER_RADIUS)
        self.blit(pygame.transform.smoothscale(cards[0], (card_width, card_height)), left_card_pos)
        self.blit(pygame.transform.smoothscale(cards[1], (card_width, card_height)), center_card_pos)
        self.blit(pygame.transform.smoothscale(cards[2], (card_width, card_height)), right_card_pos)

        # Button sizes and positions
        button_y = card_slot_y + card_slot_height
        button_height = (size[1] - button_y) // 4
        self.buttons = []
        self.initButtons((size[0], button_height), button_y, font)

        # Render buttons
        for button in self.buttons:
            self.blit(button, button.position)

    # Helper method to initialize the action buttons
    def initButtons(self, size, start_y, font):
        x = size[0] // 2
        y = start_y + size[1] // 2
        for index,action_text in enumerate(ACTION_OPTION_TEXT):
            text_obj = font.render(action_text, True, BLACK)
            self.buttons.append(Button(text_obj, (x, y), Actions(index), size))
            y += size[1]

    def highlight(self, valid_actions, screen):
        for button in self.buttons:
            if button.return_value not in valid_actions:
                button_true_pos = (self.position[0] + button.position[0], self.position[1] + button.position[1])
                GrayOut(button.size, button_true_pos).draw(screen)

    def select(self, action, screen):
        for button in self.buttons:
            if button.return_value == action:
                button_true_pos = (self.position[0] + button.position[0], self.position[1] + button.position[1])
                button_rect = pygame.Rect(button_true_pos, button.size)
                screen.drawRect(button_rect, BLACK, BORDER_RADIUS * 4)

    # Click detection methods for the action buttons
    def getClicked(self, click_pos):
        adj_pos = (click_pos[0] - self.position[0], click_pos[1] - self.position[1])
        for button in self.buttons:
            if button.rect.collidepoint(adj_pos):
                return button.return_value
        return Noneon.return_value not in valid_actions:
                button_true_pos = (self.position[0] + button.position[0], self.position[1] + button.position[1])
                GrayOut(button.size, button_true_pos).draw(screen)

    def select(self, action, screen):
        for button in self.buttons:
            if button.return_value == action:
                button_true_pos = (self.position[0] + button.position[0], self.position[1] + button.position[1])
                button_rect = pygame.Rect(button_true_pos, button.size)
                screen.drawRect(button_rect, BLACK, BORDER_RADIUS * 4)

    # Click detection methods for the action buttons
    def getClicked(self, click_pos):
        adj_pos = (click_pos[0] - self.position[0], click_pos[1] - self.position[1])
        for button in self.buttons:
            if button.rect.collidepoint(adj_pos):
                return button.return_value
        return None