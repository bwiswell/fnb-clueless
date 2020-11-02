import pygame
from ClueMap import ClueMap
from ControlPanel import ControlPanel
from Dialogues import Message, InputDialogue, ConfirmationDialogue

# Size of the GUI and elements within the GUI, to be replaced with rescaling logic
GUI_SIZE = (1280, 896)
MAPVIEW_POS = (0, 0)
MAPVIEW_SIZE = (896, 896)
CONTROL_POS = (896, 0)
CONTROL_SIZE = (384, 896)

# Confirmation and message strings
NAME_PROMPT = "Please enter a character name."
TURN_MESSAGE = "It's your turn - make a move!"
ACTION_CONF = "Are you sure you want to "
MOVE_CONF = "Are you sure you want to move to the "
INVALID_ACTION = "Pick a valid action to perform!"
INVALID_MOVE = "That isn't a valid move!"
ACTION_MESSAGE = "You have chosen to "
MOVE_MESSAGE = "You moved to the "

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# The font size to use for dialogues and messages
FONT_SIZE = 24

# Main GUI class. Provides several methods for client-GUI interaction:

# updateGUI():                          updates the GUI based on server updates. Will be expanded
#                                       as the server update system is implemented

# getPlayerName():                      displays a text input dialogue and returns a string containing
#                                       a player name
#
# Possible return values:               an alphanumeric string between 1 and 15 characters (NOT YET FULLY IMPLEMENTED)

# getPlayerAction():                    waits for the player to select an action option button and returns
#                                       a string indicating the selected action
#
# Possible return values:               move, suggest, accuse, endturn

# getPlayerMove(valid_moves):           valid_moves is a list of location IDs that constitue the valid
#                                       moves for the current player. Returns a location ID (after 2
#                                       factor confirmation) that represents the desired move

class ClueGUI(pygame.Surface):
    def __init__(self):
        pygame.init()
        pygame.Surface.__init__(self, GUI_SIZE)
        self.screen = pygame.display.set_mode(GUI_SIZE)
        self.center = (GUI_SIZE[0] // 2, GUI_SIZE[1] // 2)
        self.clue_map = ClueMap(MAPVIEW_SIZE)
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.control_panel = ControlPanel(CONTROL_SIZE, CONTROL_POS, self.font)

    # Clear any messages or dialogues currently shown
    def clearDialogues(self):
        self.screen.blit(self, (0, 0))
        pygame.display.update()

    def updateGUI(self, player_locations):
        self.clue_map.draw(player_locations, True, self.font)
        self.blit(self.clue_map, MAPVIEW_POS)
        self.control_panel.draw()
        self.blit(self.control_panel, CONTROL_POS)
        self.screen.blit(self, (0, 0))
        pygame.display.update()

    def getPlayerName(self):
        input_dialogue = InputDialogue(self.font, NAME_PROMPT, self.center)
        input_dialogue.draw(self.screen)
        name = input_dialogue.getResponse(self.screen)
        self.clearDialogues()
        return name

    def getPlayerAction(self, valid_actions):
        pygame.event.pump()
        action_selected = False
        action = ""
        while not action_selected:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    action = self.control_panel.getClicked(event.pos)
                    if action in valid_actions:
                        self.clearDialogues()
                        conf_text = ACTION_CONF + action + "?"
                        conf_dialogue = ConfirmationDialogue(self.font, conf_text, self.center)
                        conf_dialogue.draw(self.screen)
                        action_selected = conf_dialogue.getResponse()
                        self.clearDialogues()
                    else:
                        Message(self.font, INVALID_ACTION, self.center).draw(self.screen)
        action_text = MOVE_MESSAGE + action + "!"
        Message(self.font, action_text, self.center).draw(self.screen)
        return action

    def getPlayerMove(self, valid_moves):
        pygame.event.pump()
        moved = False
        location = ""
        while not moved:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    location = self.clue_map.getClicked(event.pos)
                    if location in valid_moves:
                        self.clearDialogues()
                        conf_text = MOVE_CONF + location + "?"
                        conf_dialogue = ConfirmationDialogue(self.font, conf_text, self.center)
                        conf_dialogue.draw(self.screen)
                        moved = conf_dialogue.getResponse()
                        self.clearDialogues()
                    else:
                        Message(self.font, INVALID_MOVE, self.center).draw(self.screen)
        moved_text = MOVE_MESSAGE + location + "!"
        Message(self.font, moved_text, self.center).draw(self.screen)
        return location