from enum import Enum, IntEnum

class Locations(IntEnum):
    STUDY = 0
    HW1 = 1
    HALL = 2
    HW2 = 3
    LOUNGE = 4
    HW3 = 5
    HW4 = 6
    HW5 = 7
    LIBRARY = 8
    HW6 = 9
    BILLIARD = 10
    HW7 = 11
    DINING = 12
    HW8 = 13
    HW9 = 14
    HW10 = 15
    CONSERVATORY = 16
    HW11 = 17
    BALLROOM = 18
    HW12 = 19
    KITCHEN = 20

class Rooms(IntEnum):
    STUDY = 0
    HALL = 2
    LOUNGE = 4
    LIBRARY = 8
    BILLIARD = 10
    DINING = 12
    CONSERVATORY = 16
    BALLROOM = 18
    KITCHEN = 20

class Weapons(Enum):
    CANDLESTICK = 0
    REVOLVER = 1
    ROPE = 2
    LEADPIPE = 3
    KNIFE = 4
    WRENCH = 5

class Characters(Enum):
    MSSCARLET = 0
    REVGREEN = 1
    MRSPEACOCK = 2
    CNLMUSTARD = 3
    MRSWHITE = 4
    PROFPLUM = 5

class Actions(Enum):
    MOVE = 0
    SUGGEST = 1
    ACCUSE = 2
    ENDTURN = 3