from pygame.sprite import Sprite, Group 
from pygame.surface import Surface 

from enum import Enum
from math import floor 

from piece import * 

class Number(Enum): 
    EIGHT   = 0 
    SEVEN   = 1
    SIX     = 2
    FIVE    = 3
    FOUR    = 4
    THREE   = 5 
    TWO     = 6 
    ONE     = 7 

    def __repr__(self):
        return self.name


class Letter(Enum): 
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5
    G = 6
    H = 7

    def __repr__(self):
        return self.name


class Tile(Sprite): 

    def __init__(self, name="tile", color='B', key=(Number.ONE, Letter.A), pos=(0, 0)): 
        super().__init__() 

        self.name = name    # String name of the tile 
        self.key = key      # Key used to access board matrix 
     
        self.color = color 
        self.colorTuple = (0, 0, 0) if color == 'B' else (255, 255, 255)

        self.surface  = Surface((75, 75))
        self.surface.fill(self.colorTuple)

        self.pos = pos 
        self.rect = self.surface.get_rect(topleft=self.pos)

        self.isActive = False

        self.pieceHolding = None
        
    def pieceHolding(self): 
        """ Returns the piece that's on the tile """

        return self.pieceHolding 

    def setPosition(self, left, top): 
        self.rect.update((left, top), (75, 75))

    def activate(self): 
        self.isActive = True 
        self.surface.fill((0, 0, 255))
        
        if self.pieceHolding: 
            self.surface.blit(self.pieceHolding.image, self.pieceHolding.rect)
        
    def deactivate(self): 
        self.isActive = False
        self.surface.fill(self.colorTuple)
        
        if self.pieceHolding: 
            self.surface.blit(self.pieceHolding.image, self.pieceHolding.rect)

    def holdPiece(self, piece): 
        self.pieceHolding = piece
        self.surface.blit(piece.image, piece.rect)
        print(piece.rect)

    def __str__(self): 
            return f'Tile(key={self.key}, color={self.color}'
        
    def __repr__(self): 
        return f'Tile(name=(), key={self.key}, color={self.color})'
    

class Board: 

    def __init__(self): 

        self.boardMatrix = [[] for i in range(8)]
        self.pieces = []

        self.isActive = False 
        self.activeTile = None

        # Use for iteration 
        self.row = self.col = 0

        colorPicker = 1 
        for number in Number:
            self.col = 0
            for letter in Letter: 
                color = 'B' if colorPicker % 2 == 0 else 'W'
                x = 75 * self.col
                y = 75 * self.row 
                tile = Tile(color=color, key=(number, letter), pos=(x, y))
                self.boardMatrix[self.row].append(tile) 
                self.col += 1
                colorPicker += 1

            self.row += 1
            colorPicker -= 1      # Offset 'c' to make sure tiles are properly colored

        self.row = self.col = 0  # Reset to use for iteration 

        self.__generatePieces()  # Initialize the game pieces 

    def selectTile(self, x, y): 
        """ Deactivates an active tile and/or activates the selected tile """ 
        
        x = floor(x/75)
        y = floor(y/75)
        selectedTile = self.boardMatrix[y][x]
        
        # Execute if a different tile has already been selected on the board
        if self.isActive: 

            # Execute if active tile is also the currently selected tile 
            if selectedTile.isActive: 
                # Deactivatee the selected tile 
                selectedTile.deactivate() 

                self.isActive = False
                self.activeTile = None

            # Deactivate the tile that was already active 
            elif not selectedTile.isActive: 
                # Deactivate the currently active tile 
                self.activeTile.deactivate() 

                # Activate the selected tile 
                selectedTile.activate()
                self.activeTile = selectedTile

        # Execute if there is no active tile on the board / Activate a tile 
        elif not self.isActive: 
            selectedTile.activate() 

            self.isActive = True 
            self.activeTile = selectedTile
            
    def __updateBoard(self): 
        """ Adjust the locations of pieces on the board """ 

        if self.isActive: 
            self.isActive = False 
        else: 
            self.isActive = True 

    def __generatePieces(self): 
        """ Initializes the game pieces on the board """
        
        key = (Number.EIGHT.value, Letter.A.value)
        tile, tilePos = self.__getTile(key)

        pawn = Pawn(key=key, pos=tilePos, team=Team.BLACK)
        tile.holdPiece(pawn) 

    def __getTile(self, key=()): 
        """ Returns the tile and its actual position """

        kNum, kLetter = key                     # Unpack the row and column values
        tile = self.boardMatrix[kNum][kLetter]  # Get the tile from the boardMatrix
        tilePos = tile.pos                      # Get the position of the tile 
        
        return tile, tilePos


    def __iter__(self):
        return self 

    def __next__(self): 
        if self.row == 7 and self.col == 8: 
            self.row = self.col = 0
            raise StopIteration 

        else: 
            if self.col == 8: 
                self.col = 0
                self.row += 1

            self.col += 1

            return self.boardMatrix[self.row][self.col-1]
            

if __name__ == '__main__': 
    Tile() 
    Board(90, 0) 
