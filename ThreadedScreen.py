from threading import Lock

from pygame import display, FULLSCREEN

from Constants import WHITE

# Screen class for updating the display from multiple threads
class ThreadedScreen():
    def __init__(self, size=None):
        # Initialize the screen at the given size, or as a fullscreen
        # display if no size is provided
        self.screen = None
        if size is None:
            self.screen = display.set_mode(flags=FULLSCREEN)
        else:
            self.screen = display.set_mode(size)
        self.screen.fill(WHITE)

        # Lock to prevent concurrent access
        self.lock = Lock()

    # Getter for the size of the display
    def get_size(self):
        return self.screen.get_size()

    # Method to draw to the display. The lock must be acquired before
    # any drawing can occur. The lock is released after drawing is 
    # complete.
    def blit(self, drawable, drawable_pos, draw_rect=None):
        self.lock.acquire()
        try:
            if draw_rect is not None:
                self.screen.blit(drawable, drawable_pos, draw_rect)
                display.update(draw_rect)
            else:
                self.screen.blit(drawable, drawable_pos)
                display.update()
        finally:
            self.lock.release()

    def close(self):
        display.quit()