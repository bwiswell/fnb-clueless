import pickle

class Player:
    def __init__(self, name=None, number=None, location=None, character=None, cards=None):
        self.name = name
        self.location = location
        self.character = character
        self.cards = cards
        self.turnOrder = 0
        self.number = number

    