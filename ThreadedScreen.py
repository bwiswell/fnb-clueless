import threading

import pygame

import GUIConstants

# Screen class for updating the display from multiple threads
class ThreadedScreen():
    def __init__(self, size=None):
        # Initialize the screen at the given size, or as a fullscreen
        # display if no size is provided
        self.screen = None
        if size is None:
            self.screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(size)
        self.screen.fill(GUIConstants.WHITE)

        # Lock to prevent concurrent access
        self.lock = threading.Lock()

    # Getter for the size of the display
    def get_size(self):
        return self.screen.get_size()

    # Method to draw to the display. The lock must be acquired before
    # any drawing can occur. The lock is released after drawing is 
    # complete.
    def draw(self, surface):
        self.lock.acquire()
        try:
            self.screen.blit(surface, surface.position)
            pygame.display.update()
        finally:
            self.lock.release()

    def close(self):
        pygame.display.quit()