import pickle

class Player:
    def __init__(self, name=None, number=None, location=None):
        self.name = name
        self.location = location
        self.cards = ""
        self.turnOrder = 0
        self.number = number

    