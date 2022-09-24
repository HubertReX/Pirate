VERTICAL_TILE_NUMBER = 11 # 11 17
TILE_SIZE = 64 
#VERTICAL_OFFSET = -(TILE_SIZE * (17 - VERTICAL_TILE_NUMBER))

SCREEN_HEIGHT = VERTICAL_TILE_NUMBER * TILE_SIZE
SCREEN_WIDTH = 1200 # 1200 1920

# macbook air 2560 1600
FULL_SCREEN = False

# toggle wether screen resolution should be scaled in full screen mode
SCALED = False # True

# playback backgroud music flag
ENABLE_SOUND_ON_START = True

# playback sound effects flag
ENABLE_SOUND_EFFECTS = True

# clouds on the sky moiving along with player
MOVING_CLOUDS = False

# horizon level as % of screen height
HORIZON_LEVEL = 0.65

# immortal mode for debug
GOD_MODE = True

# how many levels are available on start
START_MAX_LEVEL = 0

# maximum amount of health on start
START_MAX_HEALTH = 100

# show debug info on start (press '~' or 'x' on gamepad to toggle)
SHOW_DEBUG_INFO = True

# show touchscreen buttons
SHOW_TOUCHSCREEN = True

# amount of health recovered by a heart
HEART_RECOVERY = 10

# max fps (cut-off for fast machines)
MAX_FPS = 50

MESSAGE_LOG = ""