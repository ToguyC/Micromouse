"""Fichier contenant uniquement les constantes dont le programme à besoin
"""

WINDOW_WIDTH        : int = 1580
WINDOW_HEIGHT       : int = 710
DEFAULT_MAZE_WIDTH  : int = 5
DEFAULT_MAZE_HEIGHT : int = 5
BITMAP_WIDTH        : int = 700
BITMAP_HEIGHT       : int = 700

C_N         : int = 0x0001
C_E         : int = 0x0002
C_S         : int = 0x0004
C_W         : int = 0x0008
C_ROBOT_N   : int = 0x0010
C_ROBOT_E   : int = 0x0020
C_ROBOT_S   : int = 0x0040
C_ROBOT_W   : int = 0x0080
C_START     : int = 0x0100
C_GOAL      : int = 0x0200
C_EMPTY     : int = 0x0400
C_PATH      : int = 0x0800
C_VISITED   : int = 0x1000

WHITE : tuple = (255, 255, 255)
BLACK : tuple = (0, 0, 0)
GREEN : tuple = (50, 168, 82)
ORANGE: tuple = (247, 175, 20)
YELLOW: tuple = (250, 218, 142)
BLUE  : tuple = (101, 135, 171)