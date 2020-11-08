from ctypes import windll, c_int

import pygame

import GUIConstants

from ThreadedScreen import ThreadedScreen
from ClueMap import ClueMap
from ControlPanel import ControlPanel
from Notepad import Notepad
from Dialogues import Message, InputDialogue, ConfirmationDialogue, SuggestionDialogue

# Main GUI class. Provides several methods for client-GUI interaction:

# updateGUI(player_locations)           player_locations is a list of (ip, location) tuples used to update the GUI.

# getPlayerName()                       displays a text input dialogue and returns a string containing
#                                       a player name
#
# Possible return values:               an alphanumeric string between 1 and 8 characters

# initPlayers(players)                  players is a list containing of player objects used to initialize the player
#                                       sprites and associate them with player ip addresses. Must be invoked before
#                                       any call to updateGUI() from the client

# getPlayerAction(valid_actions)        valid_actions is a list of actions that are available for the current
#                                       player. Returns a string (after 2 factor confirmation) that represents 
#                                       the desired action
#
# Possible return values:               move, suggest, accuse, endturn

# getPlayerMove(valid_moves)            valid_moves is a list of location IDs that constitue the valid
#                                       moves for the current player. locations IDs should be entirely lowercase.
#                                       Returns a lowercase location ID (after 2 factor confirmation) that represents 
#                                       the desired move

# quit()                                must be called to safely exit keylistener and mouselistener threads
#                                       as well as pygame

class NoPossibleActionError(Exception):
    def __init__(self):
        print("No possible actions were provided!")

class ClueGUI(pygame.Surface):
    def __init__(self):
        windll.shcore.SetProcessDpiAwareness(c_int(1))
        pygame.init()
        self.screen = ThreadedScreen()
        self.position = (0, 0)

        # GUI element sizes and positions
        self.gui_size = self.screen.get_size()
        self.center = (self.gui_size[0] // 2, self.gui_size[1] // 2)
        self.map_size = ((self.gui_size[1] // 7) * 9, self.gui_size[1])
        control_height = 2 * (self.gui_size[1] // 3)
        self.control_size = (self.gui_size[0] - self.map_size[0], control_height)
        self.control_pos = (self.map_size[0], 0)
        self.notepad_size = (self.gui_size[0] - self.map_size[0], self.gui_size[1] - control_height)
        self.notepad_pos = (self.map_size[0], self.gui_size[1] - self.notepad_size[1])

        # Initialize internal screen and font
        pygame.Surface.__init__(self, self.gui_size, pygame.SRCALPHA)
        font_size = self.getFontSize()
        self.font = pygame.font.SysFont(None, font_size)

        # GUI elements
        self.clue_map = ClueMap(self.map_size)
        self.control_panel = None
        self.notepad = Notepad(self.notepad_size, self.notepad_pos, self.screen, self.font)

        # Player information
        self.player_name = ""
        self.player = None
        self.player_sprite = None

        # Initial GUI render
        self.updateGUI(None)

    # Get a font size appropriate to the screen size
    def getFontSize(self):
        gui_width = self.gui_size[0]
        for i in range(len(GUIConstants.GUI_FONT_THRESHOLDS) - 1):
            if gui_width >= GUIConstants.GUI_FONT_THRESHOLDS[i] and gui_width < GUIConstants.GUI_FONT_THRESHOLDS[i+1]:
                return GUIConstants.GUI_FONT_SIZES[i]
        return GUIConstants.GUI_FONT_SIZES[len(GUIConstants.GUI_FONT_SIZES) - 1]

    # Clear any messages or dialogues currently shown
    def clearDialogues(self):
        self.screen.draw(self)

    def updateGUI(self, player_locations):
        if player_locations is not None:
            player_locations = [(ip,loc.lower()) for (ip,loc) in player_locations]
        self.clue_map.draw(player_locations)
        self.blit(pygame.transform.smoothscale(self.clue_map, self.map_size), (0, 0))
        self.screen.draw(self)

    def getPlayerName(self):
        self.notepad.block()
        input_dialogue = InputDialogue(self.font, GUIConstants.NAME_PROMPT, self.center, 8)
        input_dialogue.draw(self.screen)
        name = input_dialogue.getResponse(self.screen)
        self.clearDialogues()
        self.notepad.unblock()
        self.player_name = name
        self.screen.draw(Message(self.font, GUIConstants.START_MESSAGE, self.center))
        return name

    def initPlayers(self, players):
        self.clue_map.initPlayerSprites(players)
        for player in players:
            if player.name == self.player_name:
                self.player = player
        self.player_sprite = self.clue_map.getPlayerSpriteByName(self.player_name)
        self.control_panel = ControlPanel(self.control_size, self.control_pos, self.player_sprite, self.player.cards, self.font)
        self.blit(self.control_panel, self.control_pos)
        self.updateGUI(None)

    def getPlayerAction(self, valid_actions):
        return self.getPlayerResponse(valid_actions, self.control_panel, GUIConstants.PICK_ACTION_MESSAGE, GUIConstants.ACTION_CONF, GUIConstants.INVALID_ACTION, GUIConstants.ACTION_MESSAGE)

    def getPlayerMove(self, valid_moves):
        return self.getPlayerResponse(valid_moves, self.clue_map, GUIConstants.PICK_MOVE_MESSAGE, GUIConstants.MOVE_CONF, GUIConstants.INVALID_MOVE, GUIConstants.MOVE_MESSAGE)

    # Helper function to get an action/move selection and display the appropriate confirmation dialogue
    def getPlayerResponse(self, valid_actions, click_area, pick_text, conf_text, invalid_text, success_text):
        self.notepad.block()
        self.clearDialogues()
        if len(valid_actions) == 0:
            raise NoPossibleActionError
        valid_actions = [action.lower() for action in valid_actions]
        pygame.event.pump()
        done = False
        response = ""
        self.screen.draw(Message(self.font, pick_text, self.center))
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    response = click_area.getClicked(event.pos)
                    self.clearDialogues()
                    if response in valid_actions:
                        conf_text += response + "?"
                        conf_dialogue = ConfirmationDialogue(self.font, conf_text, self.center)
                        self.screen.draw(conf_dialogue)
                        done = conf_dialogue.getResponse()
                        self.clearDialogues()
                    else:
                        self.screen.draw(Message(self.font, invalid_text, self.center))
        success_text += response + "!"
        self.screen.draw(Message(self.font, success_text, self.center))
        self.notepad.unblock()
        return response

    # In progress - gets a player, location, and weapon card from a dialogue for a suggestion/accusation
    def getPlayerSuggestion(self, card_deck):
        self.clearDialogues()
        pygame.event.pump()
        suggestion_dialogue = SuggestionDialogue(self.font, GUIConstants.PICK_SUGGESTION_MESSAGE, self.center, self.gui_size[0], card_deck)
        self.screen.draw(suggestion_dialogue)
        return suggestion_dialogue.getResponse(self.screen)

    def quit(self):
        self.notepad.quit()
        pygame.quit()