import pygame

# Replace with a room class
N_ROOMS = 9
ROOM_NAMES = ["Study", "Hall", "Lounge", "Library", "Billiard Room", "Dining Room", "Conservatory", "Ballroom", "Kitchen"]

ROOM_ASSET_SIZE = 192

N_H_HALLWAYS = N_V_HALLWAYS = 6
HALLWAY_ASSET_X_OFFSET = 192
V_HALLWAY_Y_OFFSET = 64
H_HALLWAY_ASSET_SIZE = (128, 64)
V_HALLWAY_ASSET_SIZE = (64, 128)

# Replace with rescaling logic
ROOM_POSITIONS = [(0, 0), (320, 0), (640, 0), (0, 320), (320, 320), (640, 320), (0, 640), (320, 640), (640, 640)]
H_HALLWAY_POSITIONS = [(192, 64), (512, 64), (192, 384), (512, 384), (192, 704), (512, 704)]
V_HALLWAY_POSITIONS = [(64, 192), (64, 512), (384, 192), (384, 512), (704, 192), (704, 512)]

class LocationSprite(pygame.sprite.Sprite):
    def __init__(self, name, asset, position):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image = asset
        self.position = position
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

def loadAll():
    location_assets = pygame.image.load('location_assets.png').convert()
    location_sprites = pygame.sprite.Group()
    for i in range(N_ROOMS):
        room_name = ROOM_NAMES[i]
        room_y_offset = i * ROOM_ASSET_SIZE
        room_asset_position = pygame.Rect(0, room_y_offset, ROOM_ASSET_SIZE, ROOM_ASSET_SIZE)
        room_asset = pygame.Surface(room_asset_position.size).convert()
        room_asset.blit(location_assets, (0, 0), room_asset_position)
        room_position = ROOM_POSITIONS[i]
        location_sprites.add(LocationSprite(room_name, room_asset, room_position))
    for i in range(N_H_HALLWAYS):
        hallway_name = "H Hallway " + str(i + 1)
        hallway_asset_position = pygame.Rect(HALLWAY_ASSET_X_OFFSET, 0, H_HALLWAY_ASSET_SIZE[0], H_HALLWAY_ASSET_SIZE[1])
        hallway_asset = pygame.Surface(hallway_asset_position.size).convert()
        hallway_asset.blit(location_assets, (0, 0), hallway_asset_position)
        hallway_position = H_HALLWAY_POSITIONS[i]
        location_sprites.add(LocationSprite(hallway_name, hallway_asset, hallway_position))
    for i in range(N_V_HALLWAYS):
        hallway_name = "V Hallway " + str(i + 1)
        hallway_asset_position = pygame.Rect(HALLWAY_ASSET_X_OFFSET, V_HALLWAY_Y_OFFSET, V_HALLWAY_ASSET_SIZE[0], V_HALLWAY_ASSET_SIZE[1])
        hallway_asset = pygame.Surface(hallway_asset_position.size).convert()
        hallway_asset.blit(location_assets, (0, 0), hallway_asset_position)
        hallway_position = V_HALLWAY_POSITIONS[i]
        location_sprites.add(LocationSprite(hallway_name, hallway_asset, hallway_position))
    return location_sprites


