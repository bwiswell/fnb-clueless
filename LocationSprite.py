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

# Colors
RED = (255, 0, 0)

# Assets filename
LOCATION_ASSETS = "location_assets.png"

# Spritesheet and font
sprite_sheet = None
font = None

# Basic Sprite subclass for a sprite with a name and initial position
class LocationSprite(pygame.sprite.Sprite):
    def __init__(self, name, asset, position):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image = asset
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

# Add text names to rooms for debugging
def addText(name, asset):
    text = font.render(name, True, RED)
    text_rect = text.get_rect()
    asset_rect = asset.get_rect()
    text_x = asset_rect.size[0] // 2 - text_rect.size[0] // 2
    text_y = asset_rect.size[1] // 2 - text_rect.size[1] // 2
    asset.blit(text, (text_x, text_y), text_rect)

# Create a single sprite from an asset
def loadAsset(name, asset_position, sprite_position):
    asset = pygame.Surface(asset_position.size).convert()
    asset.blit(sprite_sheet, (0, 0), asset_position)
    addText(name, asset)                                        # For debugging
    return LocationSprite(name, asset, sprite_position)

# Create all location (room and hallway) sprites and set their names and locations
def loadAll():
    # Initialize spritesheet and font
    global sprite_sheet, font
    sprite_sheet = pygame.image.load(LOCATION_ASSETS).convert()
    font = pygame.font.SysFont(None, 24)

    location_sprites = pygame.sprite.Group()

    # Create all room sprites
    for i in range(N_ROOMS):
        room_name = ROOM_NAMES[i]
        room_asset_position = pygame.Rect(0, i * ROOM_ASSET_SIZE, ROOM_ASSET_SIZE, ROOM_ASSET_SIZE)
        room_sprite_position = ROOM_POSITIONS[i]
        location_sprites.add(loadAsset(room_name, room_asset_position, room_sprite_position))

    # Create all horizontal hallway sprites
    for i in range(N_H_HALLWAYS):
        hallway_name = "H Hallway " + str(i + 1)
        hallway_asset_position = pygame.Rect(HALLWAY_ASSET_X_OFFSET, 0, H_HALLWAY_ASSET_SIZE[0], H_HALLWAY_ASSET_SIZE[1])
        hallway_sprite_position = H_HALLWAY_POSITIONS[i]
        location_sprites.add(loadAsset(hallway_name, hallway_asset_position, hallway_sprite_position))

    # Create all vertical hallway sprites
    for i in range(N_V_HALLWAYS):
        hallway_name = "V Hallway " + str(i + 1)
        hallway_asset_position = pygame.Rect(HALLWAY_ASSET_X_OFFSET, V_HALLWAY_Y_OFFSET, V_HALLWAY_ASSET_SIZE[0], V_HALLWAY_ASSET_SIZE[1])
        hallway_sprite_position = V_HALLWAY_POSITIONS[i]
        location_sprites.add(loadAsset(hallway_name, hallway_asset_position, hallway_sprite_position))

    return location_sprites