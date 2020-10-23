import pygame
from ClueMap import ClueMap

# Size of the game board in the GUI
MAPVIEW_SIZE = (896, 896)

# Must be called before any pygame functionality
pygame.init()

# Temporarily limited to the size of the game board pending a control panel
screen = pygame.display.set_mode(MAPVIEW_SIZE)

# Create the game board GUI pane
clue_map = ClueMap(MAPVIEW_SIZE)

# Main loop for testing only - to be replaced by server updates
running = True
while running:
    # Handle clicks
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
    # Discard other events
    pygame.event.pump()

    # Render the game board
    clue_map.draw(screen)
    pygame.display.update()