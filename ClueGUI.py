from ctypes import windll, c_int
import time
from queue import Queue

import pygame

from Errors import NoPossibleActionError

from Constants import WHITE, BLACK, GUI_FONT_SIZES, GUI_FONT_THRESHOLDS
from Constants import GAME_START_MESSAGE
from Constants import PICK_ACTION_MESSAGE, ACTION_CONF, ACTION_MESSAGE
from Constants import PICK_MOVE_MESSAGE, MOVE_CONF, MOVE_MESSAGE
from Constants import PICK_SUGGESTION_MESSAGE, PICK_ACCUSATION_MESSAGE

from Drawable import Drawable
from ThreadedScreen import ThreadedScreen
from ClueMap import ClueMap
from ControlPanel import ControlPanel
from InformationCenter import InformationCenter
from Client import Client
import Card
from Dialogues import ConfirmationDialogue, SuggestionDialogue
from ClientRequest import ClientRequests
from Lobby import Lobby

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

class ClueGUI():
    def __init__(self):
        windll.shcore.SetProcessDpiAwareness(c_int(1))
        pygame.init()
        self.screen = None

        # Lobby
        self.lobby = None

        # GUI element sizes and positions
        self.gui_size = None
        self.center = None
        self.map_size = None
        self.control_size = None
        self.control_pos = None
        self.information_center_size = None
        self.information_center_pos = None

        self.surface = None

        # Font
        self.font = None

        # Clue Map
        self.clue_map = None

        # Player information
        self.player = None
        self.player_sprite = None

        # Cards
        self.card_deck = None

        # Control Panel
        self.control_panel = None
        
        # Information Center
        self.information_center = None

        # Game control
        self.running = True

        # Client requests
        self.request_queue = Queue()

        # Client
        self.client = Client(self.request_queue)
        self.client.start()

        self.run()

    # Get a font size appropriate to the screen size
    def getFontSize(self):
        gui_width = self.gui_size[0]
        for i in range(len(GUI_FONT_THRESHOLDS) - 1):
            if gui_width >= GUI_FONT_THRESHOLDS[i] and gui_width < GUI_FONT_THRESHOLDS[i+1]:
                return GUI_FONT_SIZES[i]
        return GUI_FONT_SIZES[len(GUI_FONT_SIZES) - 1]

    def initSizes(self):
        self.gui_size = self.screen.get_size()
        self.center = (self.gui_size[0] // 2, self.gui_size[1] // 2)
        self.map_size = ((self.gui_size[1] // 7) * 9, self.gui_size[1])
        control_height = self.gui_size[1] // 2
        self.control_size = (self.gui_size[0] - self.map_size[0], control_height)
        self.control_pos = (self.map_size[0], 0)
        self.information_center_size = (self.gui_size[0] - self.map_size[0], self.gui_size[1] - control_height)
        self.information_center_pos = (self.map_size[0], self.gui_size[1] - self.information_center_size[1])

    def initGUI(self, player, player_list):
        self.screen = ThreadedScreen()
        self.initSizes()
        self.surface = Drawable(self.map_size, (0, 0))
        self.font = pygame.font.SysFont(None, self.getFontSize())
        self.clue_map = ClueMap(self.map_size)
        self.clue_map.initPlayerSprites(player_list)
        self.player = player
        self.player_sprite = self.clue_map.getPlayerSprite(self.player.character)
        self.card_deck = Card.initCards(len(player_list))
        player_cards = [self.card_deck.card_dict[card_name] for card_name in self.player.cards]
        self.control_panel = ControlPanel(self.control_size, self.control_pos, self.player, self.player_sprite, player_cards, self.font)
        self.control_panel.draw(self.screen)
        self.information_center = InformationCenter(self.information_center_size, self.information_center_pos, self.font, self.screen)
        self.updateGUI(player_list)
        self.postMessage(GAME_START_MESSAGE)

    # Clear any dialogues or highlights currently shown
    def clear(self):
        self.surface.draw(self.screen)
        self.control_panel.draw(self.screen)

    def updateGUI(self, players):
        self.clue_map.update(players)
        self.clue_map.draw(self.surface)
        self.surface.draw(self.screen)

    def postMessage(self, text, color=BLACK):
        self.information_center.postMessage(text, color)

    def getPlayerAction(self, valid_actions):
        return self.getPlayerResponse(valid_actions, self.control_panel, PICK_ACTION_MESSAGE, ACTION_CONF, ACTION_MESSAGE)

    def getPlayerMove(self, valid_moves):
        return self.getPlayerResponse(valid_moves, self.clue_map, PICK_MOVE_MESSAGE, MOVE_CONF, MOVE_MESSAGE)

    # Helper function to get an action/move selection and display the appropriate confirmation dialogue
    def getPlayerResponse(self, valid_actions, click_area, pick_text, conf_text, success_text):
        if len(valid_actions) == 0:
            raise NoPossibleActionError
        self.postMessage(pick_text)
        click_area.highlight(valid_actions, self.screen)
        done = False
        response = ""
        while not done:
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                    response = click_area.getClicked(event.pos)
                    if response in valid_actions:
                        click_area.select(response, self.screen)
                        response_conf_text = conf_text + response.text + "?"
                        conf_dialogue = ConfirmationDialogue(self.font, response_conf_text, self.center)
                        conf_dialogue.draw(self.screen)
                        done = conf_dialogue.getResponse()
                        self.clear()
                        if not done:
                            click_area.highlight(valid_actions, self.screen)
        success_text += response.text + "!"
        self.postMessage(success_text)
        return response

    # In progress - gets a player, location, and weapon card from a dialogue for a suggestion/accusation
    def getPlayerSuggestion(self, location):
        return self.getSuggestionOrAccusation(PICK_SUGGESTION_MESSAGE, location)

    def getPlayerAccusation(self):
        return self.getSuggestionOrAccusation(PICK_ACCUSATION_MESSAGE)

    def getSuggestionOrAccusation(self, text, location=None):
        pygame.event.pump()
        suggestion_dialogue = SuggestionDialogue(self.font, text, self.center, self.gui_size[0], self.card_deck, location)
        suggestion_dialogue.draw(self.screen)
        response = suggestion_dialogue.getResponse(self.screen)
        self.clear()
        return response

    def startLobby(self):
        self.lobby = Lobby()

    def getPlayerName(self):
        return self.lobby.getPlayerName()

    def giveStartButton(self):
        self.lobby.getStart("FNBC")
        return True

    def quitLobby(self):
        self.lobby.close()

    def run(self):
        while self.running:
            time.sleep(0.1)
            if self.screen is not None:
                pygame.event.pump()
            if not self.request_queue.empty():
                request = self.request_queue.get()
                print(request)
                self.handleClientRequest(request)

    def handleClientRequest(self, request):
        response = None
        if request.id == ClientRequests.LOBBYINIT:
            self.startLobby()
        elif request.id == ClientRequests.LOBBYNAME:
            response = self.getPlayerName()
        elif request.id == ClientRequests.LOBBYSTART:
            response = self.giveStartButton()
        elif request.id == ClientRequests.LOBBYQUIT:
            self.quitLobby()
        elif request.id == ClientRequests.GUIINIT:
            self.initGUI(request.player, request.player_list)
        elif request.id == ClientRequests.GUIUPDATE:
            self.updateGUI(request.player_list)
        elif request.id == ClientRequests.PLAYERACTION:
            response = self.getPlayerAction(request.valid_actions)
        elif request.id == ClientRequests.PLAYERMOVE:
            response = self.getPlayerMove(request.valid_moves)
        elif request.id == ClientRequests.PLAYERSUGGESTION:
            response = self.getPlayerSuggestion(request.location)
        elif request.id == ClientRequests.PLAYERACCUSATION:
            response = self.getPlayerAccusation()
        elif request.id == ClientRequests.GUIMESSAGE:
            self.postMessage(request.message_text, request.message_color)
        elif request.id == ClientRequests.GUIQUIT:
            self.quit()
        if response is not None:
            self.client.response_lock.acquire()
            try:
                self.client.response = response
            finally:
                self.client.response_lock.release()

    def quit(self):
        self.information_center.quit()
        self.screen.close()
        pygame.quit()
        self.running = False

gui = ClueGUI()