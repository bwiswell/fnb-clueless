from ctypes import windll, c_int

import pygame

from Errors import NoPossibleActionError

from Constants import GUI_FONT_SIZES, GUI_FONT_THRESHOLDS
from Constants import GAME_START_MESSAGE
from Constants import PICK_ACTION_MESSAGE, ACTION_CONF, INVALID_ACTION, ACTION_MESSAGE
from Constants import PICK_MOVE_MESSAGE, MOVE_CONF, INVALID_MOVE, MOVE_MESSAGE
from Constants import PICK_SUGGESTION_MESSAGE, PICK_ACCUSATION_MESSAGE

from Drawable import Drawable
from ThreadedScreen import ThreadedScreen
from ClueMap import ClueMap
from ControlPanel import ControlPanel
from InformationCenter import InformationCenter
import Card
from Dialogues import ConfirmationDialogue, SuggestionDialogue

# Main GUI class. Provides several methods for client-GUI interaction:

# updateGUI(player_locations)           player_locations is a list of (name, location) tuples used to update the GUI.

# postMessage(text)                     text is a message to display in the message log on the GUI

# getPlayerAction(valid_actions)        valid_actions is a list of actions that are available for the current
#                                       player. Returns a string (after 2 factor confirmation) that represents 
#                                       the desired action
#
# Possible return values:               move, suggest, accuse, endturn

# getPlayerMove(valid_moves)            valid_moves is a list of location IDs that constitue the valid
#                                       moves for the current player. locations IDs should be entirely lowercase.
#                                       Returns a lowercase location ID (after 2 factor confirmation) that represents 
#                                       the desired move

# getPlayerSuggestion()                 gets a suggestion from the player

# getPlayerAccusation()                 gets an accusation from the player. essentially an alias for getPlayerSuggestion

# quit()                                must be called to safely exit keylistener and mouselistener threads
#                                       as well as pygame

class ClueGUI(Drawable):
    def __init__(self, player, all_players):
        self.screen = ThreadedScreen()

        # GUI element sizes and positions
        self.gui_size = self.screen.get_size()
        self.center = (self.gui_size[0] // 2, self.gui_size[1] // 2)
        self.map_size = ((self.gui_size[1] // 7) * 9, self.gui_size[1])
        control_height = self.gui_size[1] // 2
        self.control_size = (self.gui_size[0] - self.map_size[0], control_height)
        self.control_pos = (self.map_size[0], 0)
        self.information_center_size = (self.gui_size[0] - self.map_size[0], self.gui_size[1] - control_height)
        self.information_center_pos = (self.map_size[0], self.gui_size[1] - self.information_center_size[1])

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
        self.control_panel = ControlPanel(self.control_size, self.control_pos, self.player, self.player_sprite, player_cards, self.font)
        self.control_panel.draw(self.screen)
        self.information_center = InformationCenter(self.information_center_size, self.information_center_pos, self.font, self.screen)

        # Initial GUI render
        self.updateGUI([(player.character, player.location) for player in all_players])
        self.postMessage(GAME_START_MESSAGE)

    # Get a font size appropriate to the screen size
    def getFontSize(self):
        gui_width = self.gui_size[0]
        for i in range(len(GUI_FONT_THRESHOLDS) - 1):
            if gui_width >= GUI_FONT_THRESHOLDS[i] and gui_width < GUI_FONT_THRESHOLDS[i+1]:
                return GUI_FONT_SIZES[i]
        return GUI_FONT_SIZES[len(GUI_FONT_SIZES) - 1]

    # Clear any dialogues or highlights currently shown
    def clear(self):
        self.draw(self.screen)
        self.control_panel.draw(self.screen)

    def updateGUI(self, player_locations):
        self.clue_map.update(player_locations)
        self.clue_map.draw(self)
        self.draw(self.screen)

    def postMessage(self, text):
        self.information_center.postMessage(text)

    def getPlayerAction(self, valid_actions):
        return self.getPlayerResponse(valid_actions, self.control_panel, PICK_ACTION_MESSAGE, ACTION_CONF, INVALID_ACTION, ACTION_MESSAGE)

    def getPlayerMove(self, valid_moves):
        return self.getPlayerResponse(valid_moves, self.clue_map, PICK_MOVE_MESSAGE, MOVE_CONF, INVALID_MOVE, MOVE_MESSAGE)

    # Helper function to get an action/move selection and display the appropriate confirmation dialogue
    def getPlayerResponse(self, valid_actions, click_area, pick_text, conf_text, invalid_text, success_text):
        if len(valid_actions) == 0:
            raise NoPossibleActionError
        self.postMessage(pick_text)
        click_area.disallow(valid_actions, self.screen)
        done = False
        response = ""
        while not done:
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                    response = click_area.getClicked(event.pos)
                    if response in valid_actions:
                        click_area.select(response, self.screen)
                        conf_text += response.text + "?"
                        conf_dialogue = ConfirmationDialogue(self.font, conf_text, self.center)
                        conf_dialogue.draw(self.screen)
                        done = conf_dialogue.getResponse()
                        self.clear()
                        if not done:
                            click_area.disallow(valid_actions, self.screen)
                    else:
                        self.postMessage(invalid_text)
        success_text += response.text + "!"
        self.postMessage(success_text)
        return response

    # In progress - gets a player, location, and weapon card from a dialogue for a suggestion/accusation
    def getPlayerSuggestion(self):
        self.getSuggestionOrAccusation(PICK_SUGGESTION_MESSAGE)

    def getPlayerAccusation(self):
        self.getSuggestionOrAccusation(PICK_ACCUSATION_MESSAGE)

    def getSuggestionOrAccusation(self, text):
        pygame.event.pump()
        suggestion_dialogue = SuggestionDialogue(self.font, text, self.center, self.gui_size[0], self.card_deck)
        suggestion_dialogue.draw(self.screen)
        response = suggestion_dialogue.getResponse(self.screen)
        self.clear()
        return response


    def quit(self):
        self.information_center.quit()
        self.screen.close()
        pygame.quit()