from enum import Enum

class ClientRequests(Enum):
    LOBBYINIT = 0
    LOBBYNAME = 1
    LOBBYSTART = 2
    LOBBYQUIT = 3
    GUIINIT = 4
    GUIUPDATE = 5
    PLAYERACTION = 6
    PLAYERMOVE = 7
    PLAYERSUGGESTION = 8
    PLAYERACCUSATION = 9
    GUIMESSAGE = 10
    GUIQUIT = 11

class ClientRequest:
    def __init__(self, request_id):
        self.id = request_id

class LobbyInitRequest(ClientRequest):
    def __init__(self):
        ClientRequest.__init__(self, ClientRequests.LOBBYINIT)

class NameRequest(ClientRequest):
    def __init__(self):
        ClientRequest.__init__(self, ClientRequests.LOBBYNAME)

class StartRequest(ClientRequest):
    def __init__(self):
        ClientRequest.__init__(self, ClientRequests.LOBBYSTART)

class LobbyQuitRequest(ClientRequest):
    def __init__(self):
        ClientRequest.__init__(self, ClientRequests.LOBBYQUIT)

class GUIInitRequest(ClientRequest):
    def __init__(self, player, player_list):
        ClientRequest.__init__(self, ClientRequests.GUIINIT)
        self.player = player
        self.player_list = player_list

class UpdateRequest(ClientRequest):
    def __init__(self, player_list):
        ClientRequest.__init__(self, ClientRequests.GUIUPDATE)
        self.player_list = player_list

class ActionRequest(ClientRequest):
    def __init__(self, valid_actions):
        ClientRequest.__init__(self, ClientRequests.PLAYERACTION)
        self.valid_actions = valid_actions

class MoveRequest(ClientRequest):
    def __init__(self, valid_moves):
        ClientRequest.__init__(self, ClientRequests.PLAYERMOVE)
        self.valid_moves = valid_moves

class SuggestionRequest(ClientRequest):
    def __init__(self, location):
        ClientRequest.__init__(self, ClientRequests.PLAYERSUGGESTION)
        self.location = location

class AccusationRequest(ClientRequest):
    def __init__(self):
        ClientRequest.__init__(self, ClientRequests.PLAYERACCUSATION)

class MessageRequest(ClientRequest):
    def __init__(self, message_text, message_color):
        ClientRequest.__init__(self, ClientRequests.GUIMESSAGE)
        self.message_text = message_text
        self.message_color = message_color

class GUIQuitRequest(ClientRequest):
    def __init__(self):
        ClientRequest.__init__(self, ClientRequests.GUIQUIT)