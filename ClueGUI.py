import pygame
from ClueMap import ClueMap
import Dialogues

# Size of the GUI and elements within the GUI, to be replaced with rescaling logic
GUI_SIZE = (896, 896)
MAPVIEW_POS = (0, 0)
MAPVIEW_SIZE = (896, 896)

# Confirmation and message strings
TURN_MESSAGE = "It's your turn - make a move!"
MOVE_CONF = "Are you sure you want to move to the "
INVALID_MOVE = "That isn't a valid move!"
MOVE_MESSAGE = "You moved to the "

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# The font size to use for dialogues and messages
FONT_SIZE = 24

# Main GUI class. Provides several methods for client-GUI interaction:
#
# updateGUI():                          updates the GUI based on server updates. Will be expanded
#                                       as the server update system is implemented
#
# getPlayerName():                      displays a text input dialogue and returns a string containing
#                                       a player name
#
# getPlayerMove(valid_moves):           valid_moves is a list of location IDs that constitue the valid
#                                       moves for the current player. Returns a location ID (after 2
#                                       factor confirmation) that represents the desired move
#
# showMessage(message_text):            message_text is a string that will be displayed in a message
#                                       dialogue at the top of the GUI
#
# showConfirmationDialogue(conf_text):  conf_text is a string that will be displayed as the prompt in a
#                                       confirm/cancel dialogue. Returns True if the confirm option is
#                                       selected or False if the cancel option is selected.
class ClueGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(GUI_SIZE)
        self.center_x = GUI_SIZE[0] // 2
        self.center_y = GUI_SIZE[1] // 2
        self.clue_map = ClueMap(MAPVIEW_SIZE)
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.updateGUI()

    def updateGUI(self):
        self.screen.blit(self.clue_map.draw(), MAPVIEW_POS)
        pygame.display.update()

    def getPlayerName(self):
        input_dialogue = Dialogues.InputDialogue(self.font, "Please enter your name")
        input_size = input_dialogue.get_size()
        input_x = self.center_x - (input_size[0] // 2)
        input_y = self.center_y - (input_size[1] // 2)
        input_pos = (input_x, input_y)
        self.screen.blit(input_dialogue, input_pos)
        pygame.display.update()
        pygame.event.pump()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    name = input_dialogue.handleKeyEvent(event)
                    self.screen.blit(input_dialogue, input_pos)
                    pygame.display.update()
                    if name is not None:
                        self.updateGUI()
                        return name

    def getPlayerMove(self, valid_moves):
        self.showMessage(TURN_MESSAGE)
        pygame.event.pump()
        moved = False
        location = ""
        while not moved:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.updateGUI()
                    location = self.clue_map.getClicked(event.pos)
                    if location in valid_moves:
                        conf_text = MOVE_CONF + location + "?"
                        moved = self.showConfirmationDialogue(conf_text)
                    else:
                        self.showMessage(INVALID_MOVE)
        moved_text = MOVE_MESSAGE + location + "!"
        self.showMessage(moved_text)
        return location

    def showMessage(self, message_text):
        message = Dialogues.Message(self.font, message_text)
        message_size = message.get_size()
        message_x = self.center_x - (message_size[0] // 2)
        message_pos = (message_x, 0)
        self.screen.blit(message, message_pos)
        pygame.display.update()

    def showConfirmationDialogue(self, conf_text):
        conf_dialogue = Dialogues.ConfirmationDialogue(self.font, conf_text)
        conf_size = conf_dialogue.get_size()
        conf_x = self.center_x - (conf_size[0] // 2)
        conf_y = self.center_y - (conf_size[1] // 2)
        conf_pos = (conf_x, conf_y)
        self.screen.blit(conf_dialogue, conf_pos)
        pygame.display.update()
        pygame.event.pump()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    selection = conf_dialogue.getClicked(event.pos, conf_pos)
                    if selection is not None:
                        self.updateGUI()
                        return selection