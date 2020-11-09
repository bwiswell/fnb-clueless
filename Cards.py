import pygame
import os

card_dim = (30, 40)
path = os.path.dirname(os.path.realpath(__file__)) + "\\assets\\"

def loadandscale(path, w, h):
	img = pygame.image.load(path)
	scaledimg = pygame.transform.scale(img, (w, h))
	return scaledimg

"""
def loadImg(self, images):
    images[]

    for image in os.listdir('images'):
        images.append(pygame.image.load(image))
"""



#Players
Blue = loadandscale(path + 'Blue.png', card_dim[0], card_dim[1])
Red = loadandscale(path + 'Red.png', card_dim[0], card_dim[1])
Green = loadandscale(path + 'Green.png', card_dim[0], card_dim[1])
Purple = loadandscale(path + 'Purple.png', card_dim[0], card_dim[1])
White = loadandscale(path + 'White.png', card_dim[0], card_dim[1])
Yellow = loadandscale(path + 'Yellow.png', card_dim[0], card_dim[1])

#Weapons
Candle = loadandscale(path + 'CandleStick.png', card_dim[0], card_dim[1])
Revolver = loadandscale(path + 'Revolver.png', card_dim[0], card_dim[1])
Ropes = loadandscale(path + 'kitchen.png', card_dim[0], card_dim[1])
Lead = loadandscale(path + 'study.png', card_dim[0], card_dim[1])
Knife = loadandscale(path + 'lounge.png', card_dim[0], card_dim[1])
Wrench = loadandscale(path + 'library.png', card_dim[0], card_dim[1])



PLAYER_LIST = ["Purple", "Blue", "Green", "Red", "Yellow", "White"]
WEAPON_LIST = ["Candlestick", "Knife", "Ropes", "Revolver", "Lead", "Wrench"]
ROOMNAME_LIST = ["Study", "Lounge", "Ballroom", "Library", "Billiard Room", "Hall", "Dining Room", "Conservatory", "Kitchen"]


class Cards(pygame.Surface):
    def __init__(self, image):
        pygame.Surface.__init__(self, card_dim)
        self.name = name
        self.blit(image, 0, 0)
        





"""
    def nextPlayerCard(self):
        self.players = []

        for image in self.PLAYER_LIST:
            images.append(pygame.image.load(image))
"""

        