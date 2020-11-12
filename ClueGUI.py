from ctypes import windll, c_int

import pygame

from Errors import NoPossibleActionError

from Constants import GUI_FONT_SIZES, GUI_FONT_THRESHOLDS
from Constants import PICK_ACTION_MESSAGE, ACTION_CONF, INVALID_ACTION, ACTION_MESSAGE
from Constants import PICK_MOVE_MESSAGE, MOVE_CONF, INVALID_MOVE, MOVE_MESSAGE
from Constants import PICK_SUGGESTION_MESSAGE

from Drawable import Drawable
from ThreadedScreen import ThreadedScreen
from ClueMap import ClueMap
from ControlPanel import ControlPanel
from Notepad import Notepad
import Card
from Dialogues import GUIMessage, ConfirmationDialogue, SuggestionDialogue

# Main GUI class. Provides several methods for client-GUI interaction:

# updateGUI(player_locations)           player_locations is a list of (name, location) tuples used to update the GUI.

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

class ClueGUI(Drawable):
    def __init__(self, player, all_players):
        self.screen = ThreadedScreen()

        # GUI element sizes and positions
        self.gui_size = self.screen.get_size()
        self.map_size = ((self.gui_size[1] // 7) * 9, self.gui_size[1])
        control_height = 2 * (self.gui_size[1] // 3)
        self.control_size = (self.gui_size[0] - self.map_size[0], control_height)
        self.control_pos = (self.map_size[0], 0)
        self.notepad_size = (self.gui_size[0] - self.map_size[0], self.gui_size[1] - control_height)
        self.notepad_pos = (self.map_size[0], self.gui_size[1] - self.notepad_size[1])

        Drawable.__init__(self, self.map_size, (0, 0))
        self.center = (self.gui_size[0] // 2, self.gui_size[1] // 2)

        # Initialize and font
        font_size = self.getFontSize()
        self.font = pygame.font.SysFont(None, font_size)

        # Clue Map
        self.clue_map = ClueMap(self.map_size)
        self.clue_map.initPlayerSprites(all_players)

        # Player information
        self.player = player
        self.player_sprite = self.clue_map.getPlayerSprite(self.player.character)

        # Cards
        self.card_deck = Card.initCards()

        # Control Panel
        player_cards = [self.card_deck.card_dict[card_name] for card_name in self.player.cards]
        self.control_panel = ControlPanel(self.control_size, self.control_pos, self.player.name, self.player_sprite, player_cards, self.font)
        self.control_panel.draw(self.screen)
        self.notepad = Notepad(self.notepad_size, self.notepad_pos, self.screen, self.font)

        # Initial GUI render
        self.updateGUI([(player.character, player.location) for player in all_players])

    # Get a font size appropriate to the screen size
    def getFontSize(self):
        gui_width = self.gui_size[0]
        for i in range(len(GUI_FONT_THRESHOLDS) - 1):
            if gui_width >= GUI_FONT_THRESHOLDS[i] and gui_width < GUI_FONT_THRESHOLDS[i+1]:
                return GUI_FONT_SIZES[i]
        return GUI_FONT_SIZES[len(GUI_FONT_SIZES) - 1]

    # Clear any messages or dialogues currently shown
    def clearDialogues(self):
        self.draw(self.screen)

    def updateGUI(self, player_locations):
        self.clue_map.update(player_locations)
        self.clue_map.draw(self)
        self.draw(self.screen)      

    def getPlayerAction(self, valid_actions):
        return self.getPlayerResponse(valid_actions, self.control_panel, PICK_ACTION_MESSAGE, ACTION_CONF, INVALID_ACTION, ACTION_MESSAGE)

    def getPlayerMove(self, valid_moves):
        return self.getPlayerResponse(valid_moves, self.clue_map, PICK_MOVE_MESSAGE, MOVE_CONF, INVALID_MOVE, MOVE_MESSAGE)

    # Helper function to get an action/move selection and display the appropriate confirmation dialogue
    def getPlayerResponse(self, valid_actions, click_area, pick_text, conf_text, invalid_text, success_text):
        self.notepad.block()
        self.clearDialogues()
        if len(valid_actions) == 0:
            raise NoPossibleActionError
        pygame.event.pump()
        done = False
        response = ""
        GUIMessage(self.font, pick_text, self.center).draw(self.screen)
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    response = click_area.getClicked(event.pos)
                    self.clearDialogues()
                    if response in valid_actions:
                        conf_text += response.name + "?"
                        conf_dialogue = ConfirmationDialogue(self.font, conf_text, self.center)
                        conf_dialogue.draw(self.screen)
                        done = conf_dialogue.getResponse()
                        self.clearDialogues()
                    else:
                        GUIMessage(self.font, invalid_text, self.center).draw(self.screen)
        success_text += response.name + "!"
        GUIMessage(self.font, success_text, self.center).draw(self.screen)
        self.notepad.unblock()
        return response

    # In progress - gets a player, location, and weapon card from a dialogue for a suggestion/accusation
    def getPlayerSuggestion(self):
        self.notepad.block()
        self.clearDialogues()
        pygame.event.pump()
        suggestion_dialogue = SuggestionDialogue(self.font, PICK_SUGGESTION_MESSAGE, self.center, self.gui_size[0], self.card_deck)
        suggestion_dialogue.draw(self.screen)
        response = suggestion_dialogue.getResponse(self.screen)
        self.notepad.unblock()
        self.clearDialogues()
        return response

    def quit(self):
        self.notepad.quit()
        self.screen.close()
        pygame.quit()