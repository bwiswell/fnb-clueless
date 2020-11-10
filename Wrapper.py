import Player as pl


class Wrapper:
    def __init__(self):
        print("hello")
    
class MsgPlayerReady:
    def __init__(self):
        pass #stuff

class MsgPlayerReadyResp:
    def __init__(self):
        pass #stuff

class MsgUpdateGame():
    def __init__(self, info):
        self.info = info

class MsgLobbyReady():
    def __init__(self):
        self.start = "start_game"

class MsgPassPlayer():
    def __init__(self,player):
        self.player = player

class MsgPassPlayerNum():
    def __init__(self,num):
        self.playerNum = num

class MsgPassInformation():
    def __init__(self,info):
        self.info = info

class MsgUpdatePlayer():
    def __init__(self,player):
        self.player = player
    
class HeaderNew:
    ids = {
        MsgPlayerReady: 100,
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
