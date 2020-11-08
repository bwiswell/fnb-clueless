# Colors   
BLACK = (0, 0, 0)
MID_GRAY = (127, 127, 127)
GRAY = (191, 191, 191)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# GUI dialogue and message text
NAME_PROMPT = "Please enter a character name between 1 and 8 characters."
START_MESSAGE = "Waiting for the game to start..."
PICK_ACTION_MESSAGE = "It's your turn - select an action!"
PICK_MOVE_MESSAGE = "You have chosen to move - select a valid location!"
ACTION_CONF = "Are you sure you want to "
MOVE_CONF = "Are you sure you want to move to the "
INVALID_ACTION = "Pick a valid action to perform!"
INVALID_MOVE = "Pick a valid move to make!"
ACTION_MESSAGE = "You have chosen to "
MOVE_MESSAGE = "You moved to the "
PICK_SUGGESTION_MESSAGE = "Pick a player card, weapon card, and location card to make a suggestion!"
SUGGESTION_DISPROVEN_PRE = "Your suggestion was disproven by "
SUGGESTION_DISPROVEN_POST = " with the "
SUGGESTION_NOT_DISPROVEN = "Nobody had a card that disproved your suggestion!"
SUGGESTION_NOTIFICATION_PRE = " suggested that it was "
SUGGESTION_NOTIFICATION_MID = " in the "
SUGGESTION_NOTIFICATION_POST = " with the "
SUGGESTION_NOTIFICATION_DISPROVEN = " but was disproven."
SUGGESTION_NOTIFICATION_NOT_DISPROVEN = " and was not disproven."
ACCUSATION_RESPONSE = "Your accusation was "
ACCUSATION_NOTIFICATION_PRE = " accused "
ACCUSATION_CORRECT = " and was right!"
ACCUSATION_INCORRECT = " but was wrong!"

# GUI font information
GUI_FONT_SIZES = [16, 24, 32, 40, 48]
GUI_FONT_THRESHOLDS = [0, 1280, 1600, 1920, 2560]

# General display information
BORDER_RADIUS = 1

# Map asset and size information
BACKGROUND_ASSET_FILE_PATH = "\\assets\\background_asset.png"
OVERLAY_ASSET_FILE_PATH = "\\assets\\overlay_asset.png"
MAP_SIZE = (1152, 896)

# Location asset information
ROOM_SIZE = (256, 192)
H_HALLWAY_SIZE = (160, 64)
V_HALLWAY_SIZE = (64, 128)
ROOM_CAPTION_OFFSET = (7, 14)
ROOM_PLAYER_OFFSETS = [(64, 32), (128, 32), (64, 96), (128, 96)]
H_HALLWAY_PLAYER_OFFSET = (48, 0)
V_HALLWAY_PLAYER_OFFSET = (0, 32)
LOCATION_DATA_FILE_PATH = "\\assets\\location_assets_data.json"
LOCATION_ASSET_FILE_PATH = "\\assets\\location_assets.png"

# Character asset information
CHARACTER_ASSET_FILE_PATH = "\\assets\\character_assets.png"
NUM_CHARACTERS = 4
CHARACTER_ASSET_SIZE = (64, 64)
CHARACTER_IMAGE_Y_OFFSET = 12
CHARACTER_IMAGE_POS = (0, 12)
CHARACTER_IMAGE_SIZE = (64, 52)
CHARACTER_NAME_FONT_SIZE = 18

# Control panel information
ACTION_OPTION_TEXT = ["Move", "Suggest", "Accuse", "End Turn"]
ACTION_OPTIONS = ["move", "suggest", "accuse", "end turn"]