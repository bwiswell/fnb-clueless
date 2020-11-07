import re

import pygame

# Colors used for displaying dialogues
BLACK = (0, 0, 0)
GRAY = (191, 191, 191)
WHITE = (255, 255, 255)

# The border radius to use around text items
BORDER_RADIUS = 1

# Simple class to render a text message on a white background with a black border
class Message(pygame.Surface):
    def __init__(self, font, text, center):
        text_object = font.render(text, True, BLACK)
        text_rect = text_object.get_rect()
        pygame.Surface.__init__(self, (text_rect.size[0] + BORDER_RADIUS * 8, text_rect.size[1] + BORDER_RADIUS * 8))
        text_surface = pygame.Surface((text_rect.size[0] + BORDER_RADIUS * 6, text_rect.size[1] + BORDER_RADIUS * 6))
        text_surface.fill(WHITE)
        text_surface.blit(text_object, (BORDER_RADIUS * 3, BORDER_RADIUS * 3))
        self.fill(BLACK)
        self.blit(text_surface, (BORDER_RADIUS, BORDER_RADIUS))
        self.position = (center[0] - (self.get_size()[0] // 2), 0)

    def draw(self, screen):
        screen.blit(self, self.position)
        pygame.display.update()

# Class to display a text input dialogue. The text field should contain the input prompt
# (i.e. "Enter a player name"). KEYDOWN events can be passed to handleKeyEvent,
# which updates the text in the input box and returns None if the input is not finished,
# or the value of the inputted text if the KEYDOWN event is the return key
class InputDialogue(pygame.Surface):
    def __init__(self, font, text, center, max_characters):
        self.font = font
        self.input_text = ""
        text_object = font.render(text, True, BLACK)
        text_rect = text_object.get_rect()
        text_width = text_rect.size[0]
        text_height = text_rect.size[1]
        dialogue_height = text_height * 3
        pygame.Surface.__init__(self, (text_width + BORDER_RADIUS * 2, dialogue_height + BORDER_RADIUS * 2))
        self.fill(BLACK)
        half_height = dialogue_height // 2
        self.half_size = (text_width, half_height)
        self.input_surface_pos = (BORDER_RADIUS, BORDER_RADIUS + half_height)
        input_width = text_width // 2
        input_x = (text_width - input_width) // 2
        y_margins = text_height // 3
        self.input_y = half_height - (text_height + y_margins)
        self.input_rect = pygame.Rect(input_x - BORDER_RADIUS, self.input_y - BORDER_RADIUS, input_width + 2 * BORDER_RADIUS, text_height + 2 * BORDER_RADIUS)
        text_surface = pygame.Surface(self.half_size)
        text_surface.fill(WHITE)
        text_surface.blit(text_object, (0, y_margins))
        self.blit(text_surface, (BORDER_RADIUS, BORDER_RADIUS))
        self.position = (center[0] - self.get_size()[0] // 2, center[1] - self.get_size()[1] // 2)
        self.max_characters = max_characters

    def drawInput(self):
        input_surface = pygame.Surface(self.half_size)
        input_surface.fill(WHITE)
        input_object = self.font.render(self.input_text, True, BLACK)
        pygame.draw.rect(input_surface, GRAY, self.input_rect)
        pygame.draw.rect(input_surface, BLACK, self.input_rect, BORDER_RADIUS)
        input_x = self.input_rect.x + (self.input_rect.size[0] // 2 - input_object.get_size()[0] // 2)
        input_surface.blit(input_object, (input_x, self.input_y))
        self.blit(input_surface, self.input_surface_pos)

    def draw(self, screen):
        self.drawInput()
        screen.blit(self, self.position)
        pygame.display.update()

    def getResponse(self, screen):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if len(self.input_text) > 0:
                            return self.input_text
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        alphanumeric = re.findall("[0-9A-Za-z]", event.unicode)
                        if len(alphanumeric) != 0 and len(self.input_text) < self.max_characters:
                            self.input_text += event.unicode
                    self.draw(screen)
        
# Class to display a confirm/cancel dialogue. The text field should contain the confirm/cancel prompt
# (i.e. "Are you sure you want to move to the Kitchen?"). MOUSEBUTTONDOWN events can be passed to getClicked,
# which returns True if the click position is within the "confirm" button, False if the click position is
# within the "cancel" button, and None if the click is anywhere else
class ConfirmationDialogue(pygame.Surface):
    def __init__(self, font, text, center):
        text_object = font.render(text, True, BLACK)
        text_rect = text_object.get_rect()
        dialogue_height = text_rect.size[1] * 3
        pygame.Surface.__init__(self, (text_rect.size[0] + BORDER_RADIUS * 2, dialogue_height + BORDER_RADIUS * 2))
        text_surface = pygame.Surface((text_rect.size[0], dialogue_height))
        text_surface.fill(WHITE)
        x_margins = text_rect.size[0] // 3
        y_margins = dialogue_height // 4
        text_surface.blit(text_object, (0, y_margins - text_rect.size[1] // 2))
        self.confirm = Button(font, "Confirm", (x_margins, y_margins * 3), True)
        text_surface.blit(self.confirm, self.confirm.position)
        self.cancel = Button(font, "Cancel", (x_margins * 2, y_margins * 3), False)
        text_surface.blit(self.cancel, self.cancel.position)
        self.blit(text_surface, (BORDER_RADIUS, BORDER_RADIUS))
        self.position = (center[0] - (self.get_size()[0] // 2), center[1] - (self.get_size()[1] // 2))

    def draw(self, screen):
        screen.blit(self, self.position)
        pygame.display.update()
    
    def getResponse(self):
        pygame.event.pump()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    adj_pos = (event.pos[0] - self.position[0], event.pos[1] - self.position[1])
                    if self.confirm.rect.collidepoint(adj_pos):
                        return self.confirm.return_value
                    elif self.cancel.rect.collidepoint(adj_pos):
                        return self.cancel.return_value

class Button(pygame.Surface):
    def __init__(self, font, text, center, return_value, size=None):
        self.return_value = return_value
        text_object = font.render(text, True, BLACK)
        text_size = text_object.get_rect().size
        self.size = size
        if size is None:
            self.size = (text_size[0] + BORDER_RADIUS * 2, text_size[1] + BORDER_RADIUS * 2)
        pygame.Surface.__init__(self, self.size)
        self.fill(GRAY)
        pygame.draw.rect(self, BLACK, self.get_rect(), BORDER_RADIUS)
        self.blit(text_object, (self.size[0] // 2 - text_size[0] // 2, self.size[1] // 2 - text_size[1] // 2))
        self.position = (center[0] - (self.get_size()[0] // 2), center[1] - (self.get_size()[1] // 2))
        self.rect = pygame.Rect(self.position, self.size)

class Slot(pygame.Surface):
    def __init__(self, width, position, category, cards):
        height = 5 * (width // 3)
        self.size = (width, height)
        pygame.Surface.__init__(self, self.size)
        self.position = position
        self.rect = pygame.Rect(position, self.size)
        self.category = category
        self.cards = cards
        self.num_cards = len(self.cards)
        self.current_index = 0
        self.current_card = self.cards[self.current_index]

        card_width = 4 * (width // 5)
        card_height = 4 * (card_width // 3)
        self.card_size = (card_width, card_height)
        
        half_x_margin = (width - card_width) // 2
        half_y_margin = (height - card_height) // 2
        self.card_pos = (half_x_margin, half_y_margin)

        up_points = [(half_x_margin, half_y_margin), (width - half_x_margin, half_y_margin), (width // 2, 0)]
        down_points = [(half_x_margin, height - half_y_margin), (width - half_x_margin, height - half_y_margin), (width // 2, height)]
        self.up = pygame.Rect(half_x_margin, 0, card_width, half_y_margin)
        self.down = pygame.Rect(half_x_margin, height - half_y_margin, card_width, half_y_margin)

        self.fill(WHITE)
        pygame.draw.polygon(self, BLACK, up_points)
        pygame.draw.polygon(self, BLACK, down_points)
        self.drawCard()

    def drawCard(self):
        self.blit(pygame.transform.smoothscale(self.current_card, self.card_size), self.card_pos)

    def handleClick(self, click_pos):
        adj_pos = (click_pos[0] - self.position[0], click_pos[1] - self.position[1])
        if self.up.collidepoint(adj_pos):
            self.current_index -= 1
            self.current_card = self.cards[self.current_index % self.num_cards]
            self.drawCard()
        elif self.down.collidepoint(adj_pos):
            self.current_index += 1
            self.current_card = self.cards[self.current_index % self.num_cards]
            self.drawCard()

class SuggestionDialogue(pygame.Surface):
    def __init__(self, font, text, center, screen_width, card_deck):
        text_object = font.render(text, True, BLACK)
        text_size = text_object.get_size()
        dialogue_width = screen_width // 3
        slot_width = dialogue_width // 3
        slot_y_offset = text_size[1] * 2
        text_pos = (dialogue_width // 2 - text_size[0] // 2, slot_y_offset // 2 - text_size[1] // 2)
        player_slot = Slot(slot_width, (0, slot_y_offset), "player", card_deck.player_cards)
        weapon_slot = Slot(slot_width, (slot_width * 2, slot_y_offset), "weapon", card_deck.weapon_cards)
        location_slot = Slot(slot_width, (slot_width, slot_y_offset), "location", card_deck.location_cards)
        self.slots = [player_slot, location_slot, weapon_slot]
        slot_height = player_slot.size[1]
        dialogue_height = slot_height + slot_y_offset * 2
        self.size = (dialogue_width, dialogue_height)
        pygame.Surface.__init__(self, self.size)

        self.confirm = Button(font, "Confirm", (slot_width, dialogue_height - slot_y_offset // 2), True)
        self.cancel = Button(font, "Cancel", (slot_width * 2, dialogue_height - slot_y_offset // 2), False)

        self.fill(WHITE)
        self.blit(text_object, text_pos)
        for slot in self.slots:
            self.blit(slot, slot.position)
        self.blit(self.confirm, self.confirm.position)
        self.blit(self.cancel, self.cancel.position)
        self.position = (center[0] - (self.size[0] // 2), center[1] - (self.size[1] // 2))

    def draw(self, screen):
        screen.blit(self, self.position)
        pygame.display.update()

    def getSelection(self):
        selection = {}
        for slot in self.slots:
            selection[slot.category] = slot.current_card.id
        return selection

    def getResponse(self, screen):
        pygame.event.pump()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    adj_pos = (event.pos[0] - self.position[0], event.pos[1] - self.position[1])
                    if self.confirm.rect.collidepoint(adj_pos):
                        return self.getSelection()
                    elif self.cancel.rect.collidepoint(adj_pos):
                        return self.cancel.return_value
                    else:
                        for slot in self.slots:
                            if slot.rect.collidepoint(adj_pos):
                                slot.handleClick(adj_pos)
                                self.blit(slot, slot.position)
                                self.draw(screen)