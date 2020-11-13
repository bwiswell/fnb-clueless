import Player as pl


class Wrapper:
    def __init__(self):
        print("hello")
# Not implimented    
class MsgGameStart:
    def __init__(self,indviPlayer,gameInfo):
        self.indviPlayer = indviPlayer
        self.gameInfo = gameInfo
        self.clientMessage = " Game is starting"
# Not implimented    
class MsgPlayerReadyResp:
    def __init__(self):
        pass #stuff
# used to update the info class 
class MsgUpdateGame():
    def __init__(self, info):
        self.info = info
# wrapper for starting message
class MsgLobbyReady():
    def __init__(self):
        self.start = "start_game"
    def __str__(self):
        return "msg: start game"
# wrapper used to pass player objects
class MsgPassPlayer():
    def __init__(self,player):
        self.player = player

# used to pass player numbers/positions
class MsgPassPlayerNum():
    def __init__(self,num):
        self.playerNum = num

# used to update the info class / can be replaced with MsgUpdateGame??
class MsgPassInformation():
    def __init__(self,info):
        self.info = info
# wrapper to update players
class MsgUpdatePlayer():
    def __init__(self,player):
        self.player = player
    
class HeaderNew:
    # dict of keys based on classes to give ids to check later
    ids = {
        MsgGameStart: 100,
        MsgPlayerReadyResp: 101,
        MsgPassPlayer: 102,
        MsgPassPlayerNum: 103,
        MsgUpdatePlayer: 104,
        MsgUpdateGame: 500,
        MsgPassInformation: 501,
        MsgLobbyReady: 1000,
    }
    
    def __init__(self, data):
        self.id = self.ids.get(type(data), 0)
        print(self.id)
        self.data = data

