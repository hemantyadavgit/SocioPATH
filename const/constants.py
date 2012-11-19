# =======================================
# used by path finding
# =======================================
XOFFSET   = (0, 1, 0, -1)
YOFFSET   = (-1, 0, 1, 0)
DAXOFFSET = (1, 1, -1, -1)
DAYOFFSET = (-1, 1, 1, -1)
DBXOFFSET = (-1, 1, 1, -1)
DBYOFFSET = (-1, -1, 1, 1)

NORMAL  = '0'
BLOCKED = '1'
SOURCE  = 'S'
TARGET  = 'T'

OPENED = 'P'
CLOSED = 'C'

SCALE = 10
DIST  = 10
DDIST = 14 # diagonal distance
INF   = int(1e9)

MANHATTAN = 0
EUCLIDEAN = 1
CHEBYSHEV = 2
UNIFORMCOST = 4

ASTARM   = 0
ASTARE   = 1
ASTARC   = 2
ASTARU   = 3
DIJKSTRA = 4
BDBFS    = 5

OSOURCE = 1
OTARGET = 2
CSOURCE = 1
CTARGET = 2

# =======================================
# used by C/S communication
# =======================================
TERM = '<end>' # line terminator
RUNNING = 0
STOPPED = 1



# =======================================
# used by GUI
# =======================================
CAPTION = 'SocioPATH'

NODE_SIZE  = 20
RESOLUTION = (500, 500)
MAP_SIZE = (500, 500)

FPS_LIMIT  = 30

FONT_NAME = 'freesansbold.ttf'

ICON_NAME = 'ico.png'

# speed settings
DEFAULT_SPEED = 128
SPEED_MAX = 4096

# countdown settings
COUNTDOWN_COOLDOWN = 5

# color table
BACKGROUND_COLOR         = 'gray95'
GRID_LINE_COLOR          = 'black'
NORMAL_COLOR             = 'white'
BLOCKED_COLOR            = 'brown'
OPENED_COLOR             = 'orange'
CLOSED_COLOR             = 'green'
SOURCE_COLOR             = 'blue'
TARGET_COLOR             = 'yellow'
PARENT_LINE_COLOR        = 'red'
NODE_INFO_COLOR          = 'gray30'
CONTROL_FONT_COLOR       = 'white'
SELECTED_COLOR           = 'tomato1'
HELP_FONT_COLOR          = 'white'
PATH_COLOR               = 'white'
SPEED_FONT_COLOR         = 'white'
CONNECTION_FAILURE_COLOR = 'red'
CONNECTION_SUCCESS_COLOR = 'green'

PATH_WIDTH = 5 # path line width

NODE_INFO_FONT_SIZE = 7
MARGIN = 3

# control info
CONTROL_FONT_SIZE = 11
CONTROL_POS = (15, 15)
CONTROL_TEXT_POS = (20, 20)
CONTROL_Y_OFFSET = 16


# help info
HELP_FONT_SIZE = 11
HELP_POS = (190, 15)
HELP_TEXT_POS = (195, 20)
HELP_Y_OFFSET = 16

# connection info
CONNECTION_FAILURE_FONT_SIZE = 0
CONNECTION_FAILURE_Y = 270

CONNECTION_COUNTDOWN_FONT_SIZE = 30
CONNECTION_COUNTDOWN_Y = 320

CONNECTION_SUCCESS_POS = (5, 680)
CONNECTION_SUCCESS_FONT_SIZE = 0
CONNECTION_SUCCESS_TEXT_POS = (10, 683)

# gui status
DRAWING   = 0
RECEIVING = 1
EXIT      = 2
