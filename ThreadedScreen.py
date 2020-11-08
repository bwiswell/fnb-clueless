import threading

import pygame

class ThreadedScreen():
    def __init__(self, size=None):
        self.screen = None
        if size is None:
            self.screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(size)
        self.lock = threading.Lock()

    def get_size(self):
        return self.screen.get_size()

    def draw(self, surface):
        self.lock.acquire()
        try:
            self.screen.blit(surface, surface.position)
            pygame.display.update()
        finally:
            self.lock.release()