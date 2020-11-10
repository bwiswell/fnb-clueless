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
    
class HeaderNew:
    ids = {
        MsgPlayerReady: 100,
        MsgPlayerReadyResp: 101,
        MsgPassPlayer: 102,
        MsgUpdateGame: 500,
        MsgLobbyReady: 1000,
    }
    
    def __init__(self, data):
        self.id = self.ids.get(type(data), 0)
        self.data = data

        #msg = HeaderNew(mydataobj)
