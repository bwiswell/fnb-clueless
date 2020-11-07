import pygame
from ClueMap import ClueMap
from ControlPanel import ControlPanel
from Dialogues import Message, InputDialogue, ConfirmationDialogue, SuggestionDialogue

# Confirmation and message strings
NAME_PROMPT = "Please enter a character name between 1 and 8 characters."
START_MESSAGE = "Waiting for the game to start..."
PICK_ACTION_MESSAGE = "It's your turn - select an action!"
PICK_MOVE_MESSAGE = "You have chosen to move - select a valid location!"
ACTION_CONF = "Are you sure you want to "
MOVE_CONF = "Are you sure you want to move to the "
INVALID_ACTION = "Pick a valid action to perform!"
INVALID_MOVE = "Pick a valid move to make!"
ACTION_MESSAGE = "You have chosen to "
MOVE_MESSAGE = "You moved to the "
PICK_SUGGESTION_MESSAGE = "Pick a player card, weapon card, and location card to make a suggestion!"

# The font size to use for dialogues and messages
FONT_SIZE = 24

# Main GUI class. Provides several methods for client-GUI interaction:

# updateGUI(player_locations):          player_locations is a list of (ip, location) tuples used to update the GUI.

# getPlayerName():                      displays a text input dialogue and returns a string containing
#                                       a player name
#
# Possible return values:               an alphanumeric string between 1 and 8 characters

# initPlayers(players)                  players is a list containing of player objects used to initialize the player
#                                       sprites and associate them with player ip addresses. Must be invoked before
#                                       any call to updateGUI() from the client

# getPlayerAction(valid_actions):       valid_actions is a list of actions that are available for the current
#                                       player. Returns a string (after 2 factor confirmation) that represents 
#                                       the desired action
#
# Possible return values:               move, suggest, accuse, endturn

# getPlayerMove(valid_moves):           valid_moves is a list of location IDs that constitue the valid
#                                       moves for the current player. locations IDs should be entirely lowercase.
#                                       Returns a lowercase location ID (after 2 factor confirmation) that represents 
#                                       the desired move

class NoPossibleActionError(Exception):
    def __init__(self):
        print("No possible actions were provided!")

class NoPossibleMoveError(Exception):
    def __init__(self):
        print("No possible moves were provided!")

class ClueGUI(pygame.Surface):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        self.gui_size = self.screen.get_size()
        self.map_size = ((self.gui_size[1] // 7) * 9, self.gui_size[1])
        self.control_size = (self.gui_size[0] - self.map_size[0], self.gui_size[1])
        self.control_pos = (self.map_size[0], 0)
        pygame.Surface.__init__(self, self.gui_size)
        self.center = (self.gui_size[0] // 2, self.gui_size[1] // 2)
        self.clue_map = ClueMap(self.map_size)
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.control_panel = None
        self.player_name = ""
        self.player_sprite = None
        self.updateGUI(None)

    # Clear any messages or dialogues currently shown
    def clearDialogues(self):
        self.screen.blit(self, (0, 0))
        pygame.display.update()

    def updateGUI(self, player_locations):
        if player_locations is not None:
            player_locations = [(ip,loc.lower()) for (ip,loc) in player_locations]
        self.clue_map.draw(player_locations)
        self.blit(pygame.transform.smoothscale(self.clue_map, self.map_size), (0, 0))
        self.screen.blit(self, (0, 0))
        pygame.display.update()

    def getPlayerName(self):
        input_dialogue = InputDialogue(self.font, NAME_PROMPT, self.center, 8)
        input_dialogue.draw(self.screen)
        name = input_dialogue.getResponse(self.screen)
        self.clearDialogues()
        self.player_name = name
        Message(self.font, START_MESSAGE, self.center).draw(self.screen)
        return name

    def initPlayers(self, players):
        self.clue_map.initPlayerSprites(players)
        self.player_sprite = self.clue_map.getPlayerSpriteByName(self.player_name)
        self.control_panel = ControlPanel(self.control_size, self.control_pos, self.player_sprite)
        self.blit(self.control_panel, self.control_pos)
        self.updateGUI(None)

    def getPlayerAction(self, valid_actions):
        self.clearDialogues()
        if len(valid_actions) == 0:
            raise NoPossibleActionError
        valid_actions = [action.lower() for action in valid_actions]
        pygame.event.pump()
        action_selected = False
        action = ""
        Message(self.font, PICK_ACTION_MESSAGE, self.center).draw(self.screen)
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
                        self.clearDialogues()
                        Message(self.font, INVALID_ACTION, self.center).draw(self.screen)
        action_text = ACTION_MESSAGE + action + "!"
        Message(self.font, action_text, self.center).draw(self.screen)
        return action

    def getPlayerMove(self, valid_moves):
        self.clearDialogues()
        if len(valid_moves) == 0:
            raise NoPossibleMoveError
        valid_moves = [move.lower() for move in valid_moves]
        pygame.event.pump()
        moved = False
        location = ""
        Message(self.font, PICK_MOVE_MESSAGE, self.center).draw(self.screen)
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
                        self.clearDialogues()
                        Message(self.font, INVALID_MOVE, self.center).draw(self.screen)
        moved_text = MOVE_MESSAGE + location + "!"
        Message(self.font, moved_text, self.center).draw(self.screen)
        return location

    def getPlayerSuggestion(self, card_deck):
        self.clearDialogues()
        pygame.event.pump()
        suggestion_dialogue = SuggestionDialogue(self.font, PICK_SUGGESTION_MESSAGE, self.center, self.gui_size[0], card_deck)
        suggestion_dialogue.draw(self.screen)
        return suggestion_dialogue.getResponse(self.screen)