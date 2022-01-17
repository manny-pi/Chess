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

    def __init__(self, name="tile", color='B', key=(Number.ONE, Letter.A), pos=()): 
        super().__init__() 

        self.name = name    # String name of the tile 
        self.key = key      # Key used to access board matrix 
     
        self.color = color 
        self.colorTuple = (0, 0, 0) if color == 'B' else (255, 255, 255)

        self.surface = Surface((75, 75))
        self.surface.fill(self.colorTuple)

        self.pos = pos 
        self.rect = self.surface.get_rect(topleft=self.pos)

        self.isActive = False

        self.pieceHolding: Piece = None

    def pieceHolding(self): 
        """ Returns the piece that's on the tile """

        return self.pieceHolding 

    def holdPiece(self, piece): 
        """ Sets the piece that's on this tile """

        self.pieceHolding = piece
        self.surface.blit(self.pieceHolding.image, self.pieceHolding.rect)
 
    def activate(self): 
        self.isActive = True 
        self.surface.fill((0, 0, 255))
        
        if self.pieceHolding: 
            self.surface.blit(self.pieceHolding.image, (0, 0))
        
    def deactivate(self): 
        self.isActive = False
        self.surface.fill(self.colorTuple)
        
        if self.pieceHolding: 
            self.surface.blit(self.pieceHolding.image, (0, 0))


    def __repr__(self): 
        n = self.name 
        k = self.key 
        ph = self.pieceHolding.name if self.pieceHolding is not None else None
        phC = self.pieceHolding.team.name if self.pieceHolding is not None else ''
        c = self.color 
        p = self.pos

        return f'Tile(n={n}, k={k}, piece={ph}|{phC}, c={c}, pos={p})'
    

class Board: 

    def __init__(self): 

        self.boardMatrix: List[List[Tile]] = [[] for i in range(8)]
        self.pieces = []

        self.isActive = False 
        self.activeTile = None

        # Use for iteration 
        self.row = self.col = 0

        self.__generateTiles()   # Initialize the board tiles
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

        print(f'Active Tile: {self.activeTile}')
        
    def __updateBoard(self): 
        """ Adjust the locations of pieces on the board during the game """ 

        if self.isActive: 
            self.isActive = False 
        else: 
            self.isActive = True 

    def __generateTiles(self):
        """ Generates the tiles of the board """ 

        colorPicker = 1 
        for n in Number:
            self.col = 0
            for l in Letter: 
                name = f'{l.name}:{n.name}'
                color = 'B' if colorPicker % 2 == 0 else 'W'

                x = 75 * self.col
                y = 75 * self.row 

                key = (n, l) 
                pos = (x, y) 

                tile = Tile(name=name, color=color, key=key, pos=pos)
                self.boardMatrix[self.row].append(tile) 
                self.col += 1
                colorPicker += 1

            self.row += 1
            colorPicker -= 1      # Offset 'c' to make sure tiles are properly colored
        self.row = self.col = 0   # Reset for iteration 

    def __generatePieces(self): 
        """ Generates and initializes the chess pieces on the board """
        
        self.__generatePawns()
        self.__generateRooks()
        self.__generateKnights()
        self.__generateBishops()
        self.__generateQueens()
        self.__generateKings()

    def __generatePawns(self): 
        """ Generate and initialize the pawns for the game """ 
        
        kNums = (Number.TWO, Number.SEVEN) 
        for kNum in kNums: 
            for kLetter in Letter: 
                tileKey = (kNum, kLetter)
                tile = self.__getTile(tileKey)
                team = Team.WHITE if kNum is Number.TWO else Team.BLACK
                pawn = Pawn(key=tileKey, team=team)
                tile.holdPiece(pawn)

    def __generateRooks(self): 
        """ Generate and initialize the rooks for the game """ 

        kNums = (Number.ONE, Number.EIGHT)
        kLetters = (Letter.A, Letter.H)
        for kNum in kNums: 
            for kLetter in kLetters: 
                tileKey = (kNum, kLetter)
                tile = self.__getTile(tileKey)      
                team = Team.WHITE if kNum is Number.ONE else Team.BLACK
                rook = Rook(key=tileKey, team=Team.BLACK)
                tile.holdPiece(rook)

    def __generateKnights(self):
        """ Generate and initialize the knights for the game """

        kNums = (Number.ONE, Number.EIGHT)
        kLetters = (Letter.B, Letter.G)
        for kNum in kNums: 
            for kLetter in kLetters: 
                tileKey = (kNum, kLetter)
                tile = self.__getTile(tileKey)      
                team = Team.WHITE if kNum is Number.ONE else Team.BLACK
                knight = Knight(key=tileKey, team=Team.BLACK)
                tile.holdPiece(knight)

    def __generateBishops(self): 
        """ Generate and initialize the bishops for the game """ 

        kNums = (Number.ONE, Number.EIGHT)
        kLetters = (Letter.C, Letter.F)
        for kNum in kNums: 
            for kLetter in kLetters: 
                tileKey = (kNum, kLetter)
                tile = self.__getTile(tileKey)      
                team = Team.WHITE if kNum is Number.ONE else Team.BLACK
                knight = Bishop(key=tileKey, team=Team.BLACK)
                tile.holdPiece(knight)

    def __generateKings(self): 
        """ Generate and initialize the kings for the game """ 

        kNums = (Number.ONE, Number.EIGHT)
        kLetter = Letter.E
        for kNum in kNums: 
            tileKey = (kNum, kLetter)
            tile = self.__getTile(tileKey)      
            team = Team.WHITE if kNum is Number.ONE else Team.BLACK
            knight = Bishop(key=tileKey, team=Team.BLACK)
            tile.holdPiece(knight)        

    def __generateQueens(self): 
        """ Generate and initialize the queens for the game """

        kNums = (Number.ONE, Number.EIGHT)
        kLetter = Letter.D
        for kNum in kNums: 
            tileKey = (kNum, kLetter)
            tile = self.__getTile(tileKey)      
            team = Team.WHITE if kNum is Number.ONE else Team.BLACK
            knight = Bishop(key=tileKey, team=Team.BLACK)
            tile.holdPiece(knight)       

    def __getTile(self, key=()) -> Tile: 
        """ Returns a tile with key=key """

        kNum, kLetter = key                     # Unpack the row and column values
        
        kNum = kNum.value
        kLetter = kLetter.value 

        tile = self.boardMatrix[kNum][kLetter]  # Get the tile from the boardMatrix

        return tile

    def __iter__(self) -> Tile:
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
    Board() 
