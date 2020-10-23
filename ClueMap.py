import pygame
import LocationSprite

class ClueMap:
    def __init__(self, size):
        self.size = size
        background_asset = pygame.image.load("background_asset.png")
        background_asset_position = pygame.Rect(0, 0, size[0], size[1])
        self.background = pygame.Surface(size).convert()
        self.background.blit(background_asset, (0, 0), background_asset_position)
        self.locations = LocationSprite.loadAll()
        overlay_asset = pygame.image.load("overlay_asset.png")
        overlay_asset_position = pygame.Rect(32, 32, size[0], size[1])
        self.overlay = pygame.Surface(size).convert()
        self.overlay.blit(overlay_asset, (0, 0), overlay_asset_position)
        self.overlay.set_colorkey((0, 0, 0))

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        self.locations.draw(surface)
        surface.blit(self.overlay, (0, 0))

    def getClicked(self, position):
        for location in self.locations:
            if location.rect.collidepoint(position):
                return location.name
        return "none"