import re

import pygame

from Constants import WHITE, GRAY, BLACK, BORDER_RADIUS

from Drawable import CenteredDrawable, Button

# Simple class to render a text message on a white background with a black border
class GUIMessage(CenteredDrawable):
    def __init__(self, font, text, center):
        text_object = font.render(text, True, BLACK)
        CenteredDrawable.__init__(self, (text_object.get_width() + BORDER_RADIUS * 8, text_object.get_height() + BORDER_RADIUS * 8), center)
        pygame.draw.rect(self, BLACK, self.get_rect(), BORDER_RADIUS)
        self.blit(text_object, (BORDER_RADIUS * 4, BORDER_RADIUS * 4))
        self.position = (self.position[0], 0)

class Dialogue(CenteredDrawable):
    def __init__(self, size, center):
        CenteredDrawable.__init__(self, size, center)

    def getResponse(self):
        raise NotImplementedError

# Class to display a text input dialogue. The text field should contain the input prompt
# (i.e. "Enter a player name"). KEYDOWN events can be passed to handleKeyEvent,
# which updates the text in the input box and returns None if the input is not finished,
# or the value of the inputted text if the KEYDOWN event is the return key
class InputDialogue(Dialogue):
    def __init__(self, font, text, center, max_characters):
        self.font = font
        self.input_text = ""
        text_object = font.render(text, True, BLACK)
        text_rect = text_object.get_rect()
        text_width = text_rect.size[0]
        text_height = text_rect.size[1]
        dialogue_height = text_height * 3
        Dialogue.__init__(self, (text_width + BORDER_RADIUS * 2, dialogue_height + BORDER_RADIUS * 2), center)
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
        self.max_characters = max_characters
        input_surface = pygame.Surface(self.half_size)
        input_surface.fill(WHITE)
        pygame.draw.rect(input_surface, GRAY, self.input_rect)
        pygame.draw.rect(input_surface, BLACK, self.input_rect, BORDER_RADIUS)
        self.blit(input_surface, self.input_surface_pos)

    # Render the text currently entered by the player
    def drawInput(self):
        input_surface = pygame.Surface(self.half_size)
        input_surface.fill(WHITE)
        input_object = self.font.render(self.input_text, True, BLACK)
        pygame.draw.rect(input_surface, GRAY, self.input_rect)
        pygame.draw.rect(input_surface, BLACK, self.input_rect, BORDER_RADIUS)
        input_x = self.input_rect.x + (self.input_rect.size[0] // 2 - input_object.get_size()[0] // 2)
        input_surface.blit(input_object, (input_x, self.input_y))
        self.blit(input_surface, self.input_surface_pos)

    # Detect key presses to edit the input text and return the
    # final text input
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
                    self.drawInput()
                    self.draw(screen)
        
# Class to display a confirm/cancel dialogue. The text field should contain the confirm/cancel prompt
# (i.e. "Are you sure you want to move to the Kitchen?"). MOUSEBUTTONDOWN events can be passed to getClicked,
# which returns True if the click position is within the "confirm" button, False if the click position is
# within the "cancel" button, and None if the click is anywhere else
class ConfirmationDialogue(Dialogue):
    def __init__(self, font, text, center):
        text_object = font.render(text, True, BLACK)
        text_rect = text_object.get_rect()
        dialogue_height = text_rect.size[1] * 3
        Dialogue.__init__(self, (text_rect.size[0] + BORDER_RADIUS * 2, dialogue_height + BORDER_RADIUS * 2), center)
        text_surface = pygame.Surface((text_rect.size[0], dialogue_height))
        text_surface.fill(WHITE)
        x_margins = text_rect.size[0] // 3
        y_margins = dialogue_height // 4
        text_surface.blit(text_object, (0, y_margins - text_rect.size[1] // 2))
        self.confirm = Button(font.render("Confirm", True, BLACK), (x_margins, y_margins * 3), True)
        text_surface.blit(self.confirm, self.confirm.position)
        self.cancel = Button(font.render("Cancel", True, BLACK), (x_margins * 2, y_margins * 3), False)
        text_surface.blit(self.cancel, self.cancel.position)
        self.blit(text_surface, (BORDER_RADIUS, BORDER_RADIUS))
    
    # Detect clicks until the player selects "confirm" or "cancel"
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

# Simple class that takes a list of cards, displays one, and has up and down arrows
# the player can interact with to scroll through the cards in the list
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

    # Draw the currently selected card
    def drawCard(self):
        self.blit(pygame.transform.smoothscale(self.current_card, self.card_size), self.card_pos)

    # Detect clicks to the up and down buttons
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

# Class to display a dialogue in which the player can select a player, location,
# and weapon card comprising a suggestion/accusation. Allows the player to scroll
# through each category of card until "confirm" or "cancel" is selected. On "confirm",
# the name of each selected card is returned. Otherwise, False is returned.
class SuggestionDialogue(Dialogue):
    def __init__(self, font, text, center, screen_width, card_deck):
        text_object = font.render(text, True, BLACK)
        dialogue_width = screen_width // 3
        slot_width = dialogue_width // 3
        slot_y_offset = text_object.get_height() * 2
        text_pos = (dialogue_width // 2 - text_object.get_width() // 2, slot_y_offset // 2 - text_object.get_height() // 2)
        player_slot = Slot(slot_width, (0, slot_y_offset), "player", card_deck.player_cards)
        weapon_slot = Slot(slot_width, (slot_width * 2, slot_y_offset), "weapon", card_deck.weapon_cards)
        location_slot = Slot(slot_width, (slot_width, slot_y_offset), "location", card_deck.location_cards)
        self.slots = [player_slot, location_slot, weapon_slot]
        slot_height = player_slot.size[1]
        dialogue_height = slot_height + slot_y_offset * 2
        Dialogue.__init__(self, (dialogue_width, dialogue_height), center)

        self.fill(WHITE)
        self.blit(text_object, text_pos)
        for slot in self.slots:
            self.blit(slot, slot.position)
        self.confirm = Button(font, "Confirm", (slot_width, dialogue_height - slot_y_offset // 2), True)
        self.blit(self.confirm, self.confirm.position)
        self.cancel = Button(font, "Cancel", (slot_width * 2, dialogue_height - slot_y_offset // 2), False)
        self.blit(self.cancel, self.cancel.position)

    # Encapsulates the currently selected cards into a dict whose keys are the
    # names of the card categories ("player", "location", "weapon")
    def getSelection(self):
        selection = {}
        for slot in self.slots:
            selection[slot.category] = slot.current_card.id
        return selection

    # Detect clicks until the player selects "confirm" or "cancel"
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