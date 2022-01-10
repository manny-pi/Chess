from pygame.sprite import Sprite 
from pygame.surface import Surface 
from random import randint as r 
from math import ceil

class Food(): 
    def __init__(self, pos=[]): 
        self.x = pos[0]
        self.y = pos[1]

        self.pos = [self.x, self.y]

        self.surface = Surface((25, 25))
        self.surface.fill((255, 255, 0))
    
    def changeLocation(self, W, H): 
        self.x = 25 * ceil( r(0, W - 25) / 25 )
        self.y = 25 * ceil( r(0, H - 25) / 25 )

        self.pos = [self.x, self.y]
