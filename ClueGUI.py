import pygame

import GUIConstants

from ThreadedScreen import ThreadedScreen
from ClueMap import ClueMap
from ControlPanel import ControlPanel
from Notepad import Notepad
from Dialogues import GUIMessage, InputDialogue, ConfirmationDialogue, SuggestionDialogue, DismissableTextDialogue

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

# showSuggestionResponse(disproven=False, disproving_player=None, disproving_card=None)
#                                       disproven is a boolean that indicates if the player's suggestion was disproven
#                                       by another player's card. disproving_player is the player who had the disproving
#                                       card if there was one. disproving_card is the id of the disproving card if there
#                                       was one

# notifySuggestion(suggesting_player, suggestion, disproven=False)
#                                       suggesting_player is the player who made the suggestion. suggestion is the dict
#                                       containing that player's suggestion. disproven indicates if the suggestion was
#                                       disproven by another player's card

# showAccusationResponse(correct=False) correct is a boolean indicates if the player's accusation was correct

# notifyAccusation(accusing_player, accusation, correct=False)
#                                       accusing_player is the player who made the accusation. accusation is the dict
#                                       containing that player's accusation. correct indicates if the accusation was
#                                       correct

# quit()                                must be called to safely exit keylistener and mouselistener threads
#                                       as well as pygame

class NoPossibleActionError(Exception):
    def __init__(self):
        print("No possible actions were provided!")

class ClueGUI(pygame.Surface):
    def __init__(self, player, all_players):
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

        # Clue Map
        self.clue_map = ClueMap(self.map_size)
        self.clue_map.initPlayerSprites(all_players)

        # Player information
        self.player = player
        self.player_sprite = self.clue_map.getPlayerSprite(self.player.name)

        # Control Panel
        self.control_panel = ControlPanel(self.control_size, self.control_pos, self.player_sprite, self.player.cards, self.font)
        self.blit(self.control_panel, self.control_pos)
        self.notepad = Notepad(self.notepad_size, self.notepad_pos, self.screen, self.font)

        # Initial GUI render
        self.updateGUI([(player.name, player.location) for player in all_players])

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
        self.clue_map.draw(player_locations)
        self.blit(pygame.transform.smoothscale(self.clue_map, self.map_size), (0, 0))
        self.screen.draw(self)        

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
        self.screen.draw(GUIMessage(self.font, pick_text, self.center))
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
                        self.screen.draw(GUIMessage(self.font, invalid_text, self.center))
        success_text += response + "!"
        self.screen.draw(GUIMessage(self.font, success_text, self.center))
        self.notepad.unblock()
        return response

    # In progress - gets a player, location, and weapon card from a dialogue for a suggestion/accusation
    def getPlayerSuggestion(self):
        """
        self.notepad.block()
        self.clearDialogues()
        pygame.event.pump()
        suggestion_dialogue = SuggestionDialogue(self.font, GUIConstants.PICK_SUGGESTION_MESSAGE, self.center, self.gui_size[0], card_deck)
        self.screen.draw(suggestion_dialogue)
        response = suggestion_dialogue.getResponse(self.screen)
        self.notepad.unblock()
        self.clearDialogues()
        return response
        """

    def showSuggestionResponse(self, disproven=False, disproving_player=None, disproving_card=None):
        text = GUIConstants.SUGGESTION_NOT_DISPROVEN
        if disproven:
            text = GUIConstants.SUGGESTION_DISPROVEN_PRE + disproving_player.name + GUIConstants.SUGGESTION_DISPROVEN_POST + disproving_card + "card!"
        self.showDismissableDialogue(text)

    def notifySuggestion(self, suggesting_player, suggestion, disproven=False):
        text = suggesting_player.name + GUIConstants.SUGGESTION_NOTIFICATION_PRE + suggestion["player"]
        text += GUIConstants.SUGGESTION_NOTIFICATION_MID + suggestion["location"]
        text += GUIConstants.SUGGESTION_NOTIFICATION_POST + suggestion["weapon"]
        if disproven:
            text += GUIConstants.SUGGESTION_NOTIFICATION_DISPROVEN
        else:
            text += GUIConstants.SUGGESTION_NOTIFICATION_NOT_DISPROVEN
        self.showDismissableDialogue(text)

    def showAccusationResponse(self, correct=False):
        text = GUIConstants.ACCUSATION_RESPONSE
        if correct:
            text += "correct!"
        else:
            text += "incorrect!"
        self.showDismissableDialogue(text)

    def notifyAccusation(self, accusing_player, accusation, correct=False):
        text = accusing_player.name + GUIConstants.ACCUSATION_NOTIFICATION_PRE + accusation["player"]
        text += GUIConstants.SUGGESTION_NOTIFICATION_MID + accusation["location"]
        text += GUIConstants.SUGGESTION_NOTIFICATION_POST + accusation["weapon"]
        if correct:
            text += GUIConstants.ACCUSATION_CORRECT
        else:
            text += GUIConstants.ACCUSATION_INCORRECT
        self.showDismissableDialogue(text)

    # Helper function to show a dismissable dialogue
    def showDismissableDialogue(self, text):
        self.notepad.block()
        dismissable_dialogue = DismissableTextDialogue(self.font, text, self.center)
        self.screen.draw(dismissable_dialogue)
        dismissable_dialogue.getResponse()
        self.clearDialogues()
        self.notepad.unblock()

    def quit(self):
        self.notepad.quit()
        pygame.quit()