import pygame
import Cards
import os


pygame.init()
width=800
height=800
screen = pygame.display.set_mode( (width, height ) )
BLACK = (255,255,255)


x = width//4; # x coordnate of image
y = height//4; # y coordinate of image

path = os.path.dirname(os.path.realpath(__file__)) + "\\assets\\"

def loadandscale(path, w, h):
	img = pygame.image.load(path)
	scaledimg = pygame.transform.scale(img, (w, h))
	return scaledimg


#load the image
card_dim = (150, 200)
Candle = loadandscale(path + 'CandleStick.png', card_dim[0], card_dim[1])
Study = loadandscale(path + 'Study.png', card_dim[0], card_dim[1])
Red = loadandscale(path + 'Red.png', card_dim[0], card_dim[1])


#player cards
playerRect = pygame.Rect(175, 300, 150, 200)    #set rect dimensions
pygame.draw.rect(screen, BLACK, playerRect, 1)  #draw rect to screen
screen.blit(Red, playerRect)                    #blit image onto rect

#weapon cards
weaponsRect = pygame.Rect(325, 300, 150, 200)
pygame.draw.rect(screen, BLACK, weaponsRect, 1)
screen.blit(Candle, weaponsRect)

##TEST CARD
#room cards
roomRect = pygame.Rect(475, 300, 150, 200)
pygame.draw.rect(screen, BLACK, roomRect, 1)
screen.blit(Study, roomRect)



upTick = [[200,275], [300,275],[250,250]]
downTick = [[200,525], [300,525], [250,550]]
xOffset = 150

#scroll buttons
for i in range(3):
    pygame.draw.polygon(screen, BLACK, upTick)
    pygame.draw.polygon(screen, BLACK, downTick)
    upTick = [[x+xOffset,y] for [x,y] in upTick]
    downTick = [[x+xOffset,y] for [x,y] in downTick]


# paint screen one time
pygame.display.flip()

running = True
while (running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Set the x, y postions of the mouse click
            x, y = event.pos
#loop over, quite pygame
pygame.quit()