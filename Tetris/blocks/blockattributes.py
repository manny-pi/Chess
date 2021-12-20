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
    PINK     = (255, 94, 193)
    SKY_BLUE = (99, 226, 255)
    LIME     = (213, 255, 43)
    CUTE     = (82, 255, 148) 


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
