from pygame.sprite import Sprite, Group 
from pygame.surface import Surface 
from collections import namedtuple

class Tile(Sprite): 

    def __init__(self, name, color): 
        super().__init__() 

        self.name     = name       # List containing letter and number pair 
        self.color    = color      # The color of the tile 
    
        self.surface  = Surface((70, 70))
        self.surface.fill(color)

    def whatPiece(self): 
        """ Returns the piece that's on the tile """

        return self.pieceOn 
    
    def isActive(self): 
        """ Returns True if the tile is active / False otherwise """
        
        return self.active 


class Board(): 

    def __init__(self, width, height): 
        self.width = width 
        self.height = height

        # Initialize and store tiles 
        self.tiles = Group()
        tiles = [[l, n] for l in 'abcdefg' for n in '12345678']
        i = 0 
        while i < len(tiles): 
            color = (0, 0, 0) if i % 2 == 0 else (255, 255, 255)
            self.tiles.add(Tile(tiles[i], color, None) 
            i += 1


        





    