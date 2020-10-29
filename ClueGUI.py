import pygame
from ClueMap import ClueMap

# Size of the GUI and elements within the GUI, to be replaced with rescaling logic
GUI_SIZE = (896, 896)
MAPVIEW_POS = (0, 0)
MAPVIEW_SIZE = (896, 896)

# Confirmation and message strings
MOVE_CONF = "Are you sure you want to move to the "
INVALID_MOVE = "That isn't a valid move!"
MOVE_MESSAGE = "You moved to the "

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Other
FONT_SIZE = 24

class ClueGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(GUI_SIZE)
        self.clue_map = ClueMap(MAPVIEW_SIZE)
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.confirm = self.font.render("Confirm", True, BLACK)
        self.cancel = self.font.render("Cancel", True, BLACK)
        self.text_height = self.confirm.get_rect().size[1]
        self.updateGUI()

    def updateGUI(self):
        self.screen.blit(self.clue_map.draw(), MAPVIEW_POS)
        pygame.display.update()

    def getPlayerMove(self, valid_moves):
        pygame.event.pump()
        moved = False
        location = ""
        while not moved:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    location = self.clue_map.getClicked(event.pos)
                    if location in valid_moves:
                        confirmation_text = MOVE_CONF + location + "?"
                        moved = self.showConfirmationDialogue(confirmation_text)
                    else:
                        self.showMessage(INVALID_MOVE)
        
        # For debugging
        print(location)

        moved_text = MOVE_MESSAGE + location + "!"
        self.showMessage(moved_text)
        return location

    def showMessage(self, message_text):
        left_x = MAPVIEW_POS[0]
        top_y = MAPVIEW_POS[1]
        width = MAPVIEW_SIZE[0]
        background_rect = pygame.Rect(left_x, top_y, width, self.text_height)
        pygame.draw.rect(self.screen, WHITE, background_rect)
        text_object = self.font.render(message_text, True, BLACK)
        text_rect = text_object.get_rect()
        text_width = text_rect.size[0]
        center_x = (left_x + width) // 2
        text_x = center_x - (text_width) // 2
        self.screen.blit(text_object, (text_x, top_y))
        pygame.display.update()

    def showConfirmationDialogue(self, confirmation_text):
        center_x = (MAPVIEW_POS[0] + MAPVIEW_SIZE[0]) // 2
        center_y = (MAPVIEW_POS[1] + MAPVIEW_SIZE[1]) // 2
        text_object = self.font.render(confirmation_text, True, BLACK)
        text_rect = text_object.get_rect()
        width = text_rect.size[0]
        height = self.text_height * 3
        left_x = center_x - width // 2
        top_y = center_y - height // 2
        background_rect = pygame.Rect(left_x, top_y, width, height)
        pygame.draw.rect(self.screen, WHITE, background_rect)
        self.screen.blit(text_object, (left_x, top_y))
        confirm_x = left_x
        confirm_y = top_y + self.text_height * 2
        confirm_width = self.confirm.get_rect().size[0]
        confirm_rect = pygame.Rect(confirm_x, confirm_y, confirm_width, self.text_height)
        pygame.draw.rect(self.screen, BLACK, confirm_rect, 2)
        self.screen.blit(self.confirm, (confirm_x, confirm_y))
        cancel_width = self.cancel.get_rect().size[0]
        cancel_x = (left_x + width) - cancel_width
        cancel_y = confirm_y
        cancel_rect = pygame.Rect(cancel_x, cancel_y, cancel_width, self.text_height)
        pygame.draw.rect(self.screen, BLACK, cancel_rect, 2)
        self.screen.blit(self.cancel, (cancel_x, cancel_y))
        pygame.display.update()
        pygame.event.pump()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if confirm_rect.collidepoint(event.pos):
                        return True
                    elif cancel_rect.collidepoint(event.pos):
                        self.updateGUI()
                        return False