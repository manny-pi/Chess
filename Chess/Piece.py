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

    def __repr__(self): 
        self.name 


class Piece(Sprite): 

    def __init__(self, name="Piece", filepath=None, key=(), s="Letter-Name", team=None):
        super().__init__() 

        self.name = name 
        self.team  = team 

        if filepath is not None: 
            self.image = pygame.image.load(filepath).convert_alpha() 
        else: 
            self.image = self.__getLetter(s) 

        self.image = pygame.transform.scale(self.image, (75, 75))
        self.key   = key
        self.rect  = self.image.get_rect(topleft=(0, 0))

    def __getLetter(self, s):
        """ Returns a surface object with the given letter drawn on it """

        color =  (0, 255, 0) if self.team == Team.WHITE else (255, 0, 0)
        img = SysFont(None, 75)
        img = img.render(f"{s}", True, color)
        
        return img

    def __repr__(self):
        n = self.name 
        k = self.key 

        kNum, kLetter = self.key 
        kNum = kNum.name 
        kLetter = kLetter.name
        t = f'{kLetter}:{kNum}'

        return f'Piece(name={n}, key={k}, tileOn={t})'


class Pawn(Piece): 

    def __init__(self, key=(), team=Team.WHITE): 
        super().__init__(name="Pawn", filepath=None, key=key, s="P", team=team)
        
    def advance(self): 
        """ Moves the pawn """
        pass
        

class Rook(Piece): 

    def __init__(self, key=(), team=Team.WHITE): 
        super().__init__(name="Rook", filepath=None, s="R", team=team)


class Knight(Piece): 
    def __init__(self, key=(), team=Team.WHITE): 
        super().__init__(name="Rook", filepath=None, s="K", team=team)
    

class Bishop(Piece): 
    def __init__(self, key=(), team=Team.WHITE): 
        super().__init__(name="Rook", filepath=None, s="B", team=team)
    

class Queen(Piece): 
    def __init__(self, key=(), team=Team.WHITE): 
        super().__init__(name="Rook", filepath=None, s="Q", team=team)

    
class King(Piece): 
    def __init__(self, key=(), team=Team.WHITE): 
        super().__init__(name="King", filepath=None, s="1", team=team)


if __name__ == '__main__': 
    Piece()  
