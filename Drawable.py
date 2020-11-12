import pygame

from Constants import WHITE, GRAY, BLACK, BORDER_RADIUS

class Drawable(pygame.Surface):
    def __init__(self, size, position, transparent=False):
        if transparent:
            pygame.Surface.__init__(self, size, pygame.SRCALPHA)
        else:
            pygame.Surface.__init__(self, size)
            self.fill(WHITE)
        self.size = size
        self.position = position
        self.rect = pygame.Rect(position, size)
        self.center = self.rect.center

    def update(self):
        # Make some changes to the Drawable object
        pass

    def draw(self, surface, size=None):
        if size is None:
            surface.blit(self, self.position)
        else:
            surface.blit(self, self.position, pygame.Rect(self.position, size))

class CenteredDrawable(Drawable):
    def __init__(self, size, center):
        position = (center[0] - size[0] // 2, center[1] - size[1] // 2)
        Drawable.__init__(self, size, position)
        self.center = center

class Button(CenteredDrawable):
    def __init__(self, text_obj, center, return_value=None, size=None):
        if size is None:
            size = (text_obj.get_width() + BORDER_RADIUS * 4, text_obj.get_height() + BORDER_RADIUS * 4)
        CenteredDrawable.__init__(self, size, center)
        self.fill(GRAY)
        pygame.draw.rect(self, BLACK, self.get_rect(), BORDER_RADIUS)
        self.blit(text_obj, (size[0] // 2 - text_obj.get_width() // 2, size[1] // 2 - text_obj.get_height() // 2))
        self.return_value = return_value