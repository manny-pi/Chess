from enum import Enum

# ENUMERATIONS
# - - - - - - - - - - - - 
class Color(Enum): 
    RED      = (255, 0, 0) 
    GREEN    = (0, 255, 0)
    BLUE     = (0, 0, 255)
    YELLOW   = (252, 249, 56)
    ORANGE   = (252, 128, 56)
    BLACK    = (0, 0, 0)
    WHITE    = (255, 255, 255)


class Orientation(Enum):
    UP       = 5        # 'natural orientation' of the block
    LEFT     = 6
    RIGHT    = 7
    DOWN     = 8


class Move(Enum): 
    LEFT     = None 
    RIGHT    = None 
    SPEED_UP = None     # Equivalent to 'DOWN'
    pass 
