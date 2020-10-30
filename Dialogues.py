import pygame

# Colors used for displaying dialogues
BLACK = (0, 0, 0)
GRAY = (191, 191, 191)
WHITE = (255, 255, 255)

# The border radius to use around text items
BORDER_RADIUS = 1

# Simple class to render a text message on a white background with a black border
class Message(pygame.Surface):
    def __init__(self, font, text):
        text_object = font.render(text, True, BLACK)
        text_rect = text_object.get_rect()
        pygame.Surface.__init__(self, (text_rect.size[0] + BORDER_RADIUS * 8, text_rect.size[1] + BORDER_RADIUS * 8))
        text_surface = pygame.Surface((text_rect.size[0] + BORDER_RADIUS * 6, text_rect.size[1] + BORDER_RADIUS * 6))
        text_surface.fill(WHITE)
        text_surface.blit(text_object, (BORDER_RADIUS * 3, BORDER_RADIUS * 3))
        self.fill(BLACK)
        self.blit(text_surface, (BORDER_RADIUS, BORDER_RADIUS))

# Class to display a text input dialogue. The text field should contain the input prompt
# (i.e. "Enter a player name"). KEYDOWN events can be passed to handleKeyEvent,
# which updates the text in the input box and returns None if the input is not finished,
# or the value of the inputted text if the KEYDOWN event is the return key
class InputDialogue(pygame.Surface):
    def __init__(self, font, text):
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
        input_width = (3 * text_width) // 4
        input_x = (text_width - input_width) // 2
        y_margins = text_height // 3
        input_y = half_height - (text_height + y_margins)
        self.input_pos = (input_x, input_y)
        self.input_rect = pygame.Rect(input_x - BORDER_RADIUS, input_y - BORDER_RADIUS, input_width + 2 * BORDER_RADIUS, text_height + 2 * BORDER_RADIUS)
        text_surface = pygame.Surface(self.half_size)
        text_surface.fill(WHITE)
        text_surface.blit(text_object, (0, y_margins))
        self.blit(text_surface, (BORDER_RADIUS, BORDER_RADIUS))
        self.drawInput()

    def drawInput(self):
        input_surface = pygame.Surface(self.half_size)
        input_surface.fill(WHITE)
        input_object = self.font.render(self.input_text, True, BLACK)
        pygame.draw.rect(input_surface, GRAY, self.input_rect)
        pygame.draw.rect(input_surface, BLACK, self.input_rect, BORDER_RADIUS)
        input_surface.blit(input_object, self.input_pos)
        self.blit(input_surface, self.input_surface_pos)

    def handleKeyEvent(self, event):
        if event.key == pygame.K_RETURN:
            return self.input_text
        elif event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
        else:
            self.input_text += event.unicode
        self.drawInput()
        return None
        
# Class to display a confirm/cancel dialogue. The text field should contain the confirm/cancel prompt
# (i.e. "Are you sure you want to move to the Kitchen?"). MOUSEBUTTONDOWN events can be passed to getClicked,
# which returns True if the click position is within the "confirm" button, False if the click position is
# within the "cancel" button, and None if the click is anywhere else
class ConfirmationDialogue(pygame.Surface):
    def __init__(self, font, text):
        text_object = font.render(text, True, BLACK)
        text_rect = text_object.get_rect()
        dialogue_height = text_rect.size[1] * 3
        pygame.Surface.__init__(self, (text_rect.size[0] + BORDER_RADIUS * 2, dialogue_height + BORDER_RADIUS * 2))
        text_surface = pygame.Surface((text_rect.size[0], dialogue_height))
        text_surface.fill(WHITE)
        y_margins = text_rect.size[1] // 3
        text_surface.blit(text_object, (0, y_margins))
        confirm = font.render("Confirm", True, BLACK)
        confirm_width = confirm.get_rect().size[0]
        cancel = font.render("Cancel", True, BLACK)
        cancel_width = cancel.get_rect().size[0]
        option_x_margins = confirm_x = (text_rect.size[0] - (confirm_width + cancel_width)) // 3
        cancel_x = text_rect.size[0] - (option_x_margins + cancel_width)
        option_y = dialogue_height - (y_margins + text_rect.size[1])
        self.confirm_rect = pygame.Rect(confirm_x - BORDER_RADIUS, option_y - BORDER_RADIUS, confirm_width + 2 * BORDER_RADIUS, text_rect.size[1] + 2 * BORDER_RADIUS)
        self.cancel_rect = pygame.Rect(cancel_x - BORDER_RADIUS, option_y - BORDER_RADIUS, cancel_width + 2 * BORDER_RADIUS, text_rect.size[1] + 2 * BORDER_RADIUS)
        pygame.draw.rect(text_surface, GRAY, self.confirm_rect)
        pygame.draw.rect(text_surface, BLACK, self.confirm_rect, BORDER_RADIUS)
        text_surface.blit(confirm, (confirm_x, option_y))
        pygame.draw.rect(text_surface, GRAY, self.cancel_rect)
        pygame.draw.rect(text_surface, BLACK, self.cancel_rect, BORDER_RADIUS)
        text_surface.blit(cancel, (cancel_x, option_y))
        self.blit(text_surface, (BORDER_RADIUS, BORDER_RADIUS))
    
    def getClicked(self, click_pos, dialogue_pos):
        adj_x = click_pos[0] - dialogue_pos[0]
        adj_y = click_pos[1] - dialogue_pos[1]
        if self.confirm_rect.collidepoint((adj_x, adj_y)):
            return True
        elif self.cancel_rect.collidepoint((adj_x, adj_y)):
            return False
        else:
            return None