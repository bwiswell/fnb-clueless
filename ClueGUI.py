import pygame
from ClueMap import ClueMap

MAPVIEW_SIZE = (832, 832)

pygame.init()

screen = pygame.display.set_mode(MAPVIEW_SIZE)

clue_map = ClueMap(MAPVIEW_SIZE)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(clue_map.getClicked(event.pos))
    pygame.event.pump()
    clue_map.draw(screen)
    pygame.display.update()