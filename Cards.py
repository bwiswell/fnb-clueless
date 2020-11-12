import pygame
import os
from PlayerSprite import PlayerSprite

CARD_DIM = (30, 40)
path = os.path.dirname(os.path.realpath(__file__)) + "\\assets\\"

def loadandscale(path, w, h):
	img = pygame.image.load(path)
	scaledimg = pygame.transform.scale(img, (w, h))
	return scaledimg


#Players
Blue = loadandscale(path + 'Blue.png', CARD_DIM[0], CARD_DIM[1])
Red = loadandscale(path + 'Red.png', CARD_DIM[0], CARD_DIM[1])
Green = loadandscale(path + 'Green.png', CARD_DIM[0], CARD_DIM[1])
Purple = loadandscale(path + 'Purple.png', CARD_DIM[0], CARD_DIM[1])
White = loadandscale(path + 'White.png', CARD_DIM[0], CARD_DIM[1])
Yellow = loadandscale(path + 'Yellow.png', CARD_DIM[0], CARD_DIM[1])

#Weapons
Candle = loadandscale(path + 'CandleStick.png', CARD_DIM[0], CARD_DIM[1])
Revolver = loadandscale(path + 'Revolver.png', CARD_DIM[0], CARD_DIM[1])
Ropes = loadandscale(path + 'Ropes.png', CARD_DIM[0], CARD_DIM[1])
Lead = loadandscale(path + 'Lead.png', CARD_DIM[0], CARD_DIM[1])
Knife = loadandscale(path + 'Knife.png', CARD_DIM[0], CARD_DIM[1])
Wrench = loadandscale(path + 'Wrench.png', CARD_DIM[0], CARD_DIM[1])

#Rooms
Study = loadandscale(path + 'Study.png', CARD_DIM[0], CARD_DIM[1])
Lounge = loadandscale(path + 'Lounge.png', CARD_DIM[0], CARD_DIM[1])
Ballroom = loadandscale(path + 'Ballroom.png', CARD_DIM[0], CARD_DIM[1])
Library = loadandscale(path + 'Library.png', CARD_DIM[0], CARD_DIM[1])
BilliardsRoom = loadandscale(path + 'BilliardsRoom.png', CARD_DIM[0], CARD_DIM[1])
Hall = loadandscale(path + 'Hall.png', CARD_DIM[0], CARD_DIM[1])
DiningRoom = loadandscale(path + 'DiningRoom.png', CARD_DIM[0], CARD_DIM[1])
Hall = loadandscale(path + 'Hall.png', CARD_DIM[0], CARD_DIM[1])
Conservatory = loadandscale(path + 'Conservatory.png', CARD_DIM[0], CARD_DIM[1])
Kitchen = loadandscale(path + 'Kitchen.png', CARD_DIM[0], CARD_DIM[1])


PLAYER_LIST = [Purple, Blue, Green, Red, Yellow, White]
WEAPON_LIST = [Candle, Knife, Ropes, Revolver, Lead, Wrench]
ROOM_LIST = [Study, Lounge, Ballroom, Library, BilliardsRoom, Hall, DiningRoom, Conservatory, Kitchen]


class Cards(pygame.Surface):
    def __init__(self, name, image, list, rect):
        pygame.Surface.__init__(self)
        self.image = image
        self.rect = rect
        self.list = list
        self.blit(image, rect)

          
    #different method for each card type seems inefficient, probs a better way to
    #do this, but how do you distinguish which cards to draw onto the GUI rectangles?
    def loadWeaponCard(self, name, image):
        for weapon in WEAPON_LIST:
            self.weapon = name 
            self.image = image
        return weapon

    def loadRoomCard(self, name, image):
        for room in ROOM_LIST:
            self.name = name 
            self.image = room
        return room

    def loadPlayerCard(self, name):
        for playerSprite in PLAYER_LIST:    #ask Ben about playerSprite 
            self.player = name 
        return playerSprite



    #method to get the next card the in specified list of cards
    def nextImg(self, rect, event, list):
        self.rect = rect
        self.list = list
        self.event = event
        index = 0
        if rect.collidepoint(event.pos):
                    index += 1 
                    # Modulo to cycle through list.
                    index %= len(list)
    
    #method to get the previous card the in specified list of cards
    def prevImg(self, rect, event, list):
        self.rect = rect
        self.list = list
        self.event = event
        index = 0
        if rect.collidepoint(event.pos):
                    index -= 1 
                    # Modulo to cycle through list.
                    index %= len(list) #might need to reverse this



"""

    #method to draw the card onto a specified area
    def draw(self, screen):
        screen.blit(self, self.position)
        pygame.display.update()


    # organize cards into respective folders and use the below 
    # method to load all the images
    def loadImg(self, images):
        images[]

        for image in os.listdir('images'):
            images.append(pygame.image.load(image))
"""
