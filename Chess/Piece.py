""" Module containing the chess pieces for the game """


from pygame.sprite import Sprite
from pygame.surface import Surface

import pygame.image 
import pygame.transform

from pygame.font import SysFont
pygame.font.init() 

import enum


class Team(enum.Enum):                                                                                                                                              
    BLACK = enum.auto() 
    WHITE = enum.auto() 


class Piece(Sprite): 

    def __init__(self, name="Piece", filepath=None, key=(), pos=(), s="x", team=None):
        self.name = name 
        if filepath is not None: 
            self.image = pygame.image.load(filepath).convert_alpha() 
        else: 
            self.image = getLetter(s)
        self.image = pygame.transform.scale(self.image, (75, 75))

        self.key = key 
        self.pos = pos 
        self.rect = self.image.get_rect(topleft=self.pos)
        
        self.team = team 


class Pawn(Piece): 

    def __init__(self, key=(), pos=(), team=Team.WHITE): 
        super().__init__(name="Pawn", filepath=None, key=key, pos=pos, s="P", team=team)
        
    def advance(self): 
        pass
        

class Rook(Piece): 

    def __init__(self, pos=(), team=Team.WHITE): 
        super().__init__(name="Rook", filepath=None, pos=pos, s="R", team=team)


def getLetter(s, team=Team.WHITE):
    """ Returns a surface object with the given letter drawn on it """

    color =  (0, 255, 0) if team == Team.WHITE else (255, 0, 0)
    img = SysFont(None, 30)
    img = img.render(f"{s}", True, color)
    
    return img


if __name__ == '__main__': 
    Piece()  