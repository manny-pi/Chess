from pygame.sprite import Sprite, Group 
from pygame.surface import Surface 

from enum import Enum

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

    def __sub__(self, other): 
        return -(self.value - other.value) 

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

    def __sub__(self, other):
        return self.value - other.value 

    def __repr__(self):
        return self.name


class Tile(Sprite): 

    def __init__(self, name="tile", color='B', key=(Number.ONE, Letter.A), pos=()): 
        super().__init__() 

        self.name = name    # String name of the tile 
        self.key = key      # Key used to access board matrix 
     
        self.color = color  # String value of the color of the tile 
        self.colorTuple = (0, 0, 0) if color == 'B' else (255, 255, 255)

        self.surface = Surface((75, 75))
        self.surface.fill(self.colorTuple)

        self.pos = pos 
        self.rect = self.surface.get_rect(topleft=self.pos)

        self.isActive = False
        self.pieceHolding = None

    def holdPiece(self, piece): 
        """ Set this tile to hold the piece """

        self.pieceHolding = piece

        if self.pieceHolding is not None:
            self.surface.blit(self.pieceHolding.image, self.pieceHolding.rect)

    def disposePiece(self):
        """ Disposes the piece that is on this tile """ 

        self.pieceHolding = None 
        self.surface.fill(self.colorTuple)

    def activate(self): 
        """ Highlight this tile blue to show its been selected """ 

        self.isActive = True 
        self.surface.fill((0, 0, 255))
        
        if self.pieceHolding: 
            self.surface.blit(self.pieceHolding.image, (0, 0))
        
    def deactivate(self): 
        """ Remove highlight from this tile to show its been deselected """ 

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

        self.hasActiveTile = False 
        self.activeTile: Tile = None

        # Use for iteration 
        self.row = self.col = 0

        self.__generateTiles()   # Initialize the board tiles
        self.__generatePieces()  # Initialize the game pieces 

    def selectTile(self, key=()): 
        """ Selects or deselects a tile; Also used to move pieces around """ 
        
        kNum, kLetter = key 
        selectedTile = self.boardMatrix[kNum][kLetter]
        
        # Execute if a tile is already active 
        if self.hasActiveTile: 

            # Execute if selectedTile is activeTile / Deselect selectedTile
            if selectedTile is self.activeTile: 

                # Deactivate selectedTile 
                self.activeTile.deactivate() 

                self.hasActiveTile = False
                self.activeTile = None

            # Execute if selectedTile is not activeTile 
            elif selectedTile is not self.activeTile: 
                
                # Execute if activeTile is holding a piece / Process the piece's move
                if self.activeTile.pieceHolding: 
                    
                    # Move the piece from activeTile to selectedTile if possible 
                    self.__movePiece(selectedTile)

                    # Deactivate activeTile 
                    self.activeTile.deactivate() 
                    self.activeTile = None 
                    self.hasActiveTile = False

                # Execute if activeTile isn't holding a piece / Deactivate activeTile
                else: 

                    # Deactivate the currently active tile 
                    self.activeTile.deactivate() 

                    # Activate the selected tile / Set selectedTile as activeTile 
                    selectedTile.activate()
                    self.activeTile = selectedTile
            
        # Execute if there is no active tile / Activate selectedTile 
        elif not self.hasActiveTile: 

            # Activate selectedTile  
            selectedTile.activate() 

            # Set selectedTile as activeTile 
            self.hasActiveTile = True 
            self.activeTile = selectedTile

        print(f'Active Tile: {self.activeTile}')
        
    def __updateBoard(self): 
        """ Adjust the locations of pieces on the board during the game """ 

        if self.hasActiveTile: 
            self.hasActiveTile = False 
        else: 
            self.hasActiveTile = True 

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
                rook = Rook(key=tileKey, team=team)
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
                knight = Knight(key=tileKey, team=team)
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
                knight = Bishop(key=tileKey, team=team)
                tile.holdPiece(knight)

    def __generateQueens(self): 
        """ Generate and initialize the queens for the game """

        kNums = (Number.ONE, Number.EIGHT)
        kLetter = Letter.D
        for kNum in kNums: 
            tileKey = (kNum, kLetter)
            tile = self.__getTile(tileKey)      
            team = Team.WHITE if kNum is Number.ONE else Team.BLACK
            knight = Queen(key=tileKey, team=team)
            tile.holdPiece(knight)       

    def __generateKings(self): 
        """ Generate and initialize the kings for the game """ 

        kNums = (Number.ONE, Number.EIGHT)
        kLetter = Letter.E
        for kNum in kNums: 
            tileKey = (kNum, kLetter)
            tile = self.__getTile(tileKey)      
            team = Team.WHITE if kNum is Number.ONE else Team.BLACK
            knight = King(key=tileKey, team=team)
            tile.holdPiece(knight)        

    def __getTile(self, key=()) -> Tile: 
        """ Returns a tile with key=key """

        kNum, kLetter = key                     # Unpack the row and column values
        
        kNum = kNum.value
        kLetter = kLetter.value 

        tile = self.boardMatrix[kNum][kLetter]  # Get the tile from the boardMatrix

        return tile

    def __movePiece(self, targetTile): 
        """ Move the piece on activeTile to targetTile if possible """

        piece = self.activeTile.pieceHolding 

        if isinstance(piece, Pawn): 
            self.__movePawn(targetTile)

        elif isinstance(piece, Rook):
            self.__moveRook(targetTile) 

        elif isinstance(piece, Knight):
            self.__moveRook(targetTile) 

        elif isinstance(piece, Bishop):
            self.__moveRook(targetTile) 

        elif isinstance(piece, Queen): 
            self.__moveQueen(targetTile)
        
        elif isinstance(piece, King): 
            self.__moveKing(targetTile) 

    def __movePawn(self, targetTile): 
        """ Moves the Pawn from source to target. Returns true if the move is legal """ 

        pawn = self.activeTile.pieceHolding 

        sourceKey = self.activeTile.key 
        sKNum, sKLetter = sourceKey

        targetKey = targetTile.key
        tKNum, tKLetter = targetKey

        # Execute if the Pawn is WHITE
        if pawn.team is Team.WHITE: 

            # Execute if targetTile is taking one step forward or diagonally
            if tKNum - sKNum == 1: 

                # Execute if Pawn is advancing (not attacking)
                if tKLetter == sKLetter: 

                    # Execute if there's no piece at targetTile / Advance Pawn
                    if not targetTile.pieceHolding: 
                        targetTile.holdPiece(pawn)
                        self.activeTile.disposePiece()
                
                # Execute if Pawn is attacking 
                if abs(tKLetter - sKLetter) == 1: 

                    # Execute if targetTile is holding an enemy piece
                    pieceAtTarget = targetTile.pieceHolding 
                    if pieceAtTarget.team is Team.BLACK: 
                        
                        # Move the Pawn to targetTile 
                        targetTile.disposePiece() 
                        targetTile.holdPiece(pawn) 

                        # Remove piece from activeTile
                        self.activeTile.disposePiece()

            # Execute if target is one step forward 
            if tKNum - sKNum == 2: 
                targetTile.holdPiece(pawn)
                self.activeTile.holdPiece(None)

                self.hasActiveTile = False 
                self.activeTile = None 

            pass 

    def __moveRook(self, sourceTile, targetTile) -> bool: 
        """ Moves the Rook from source to target. Returns true if the move is legal """ 

        pass 

    def __moveKnight(self, sourceTile, targetTile) -> bool: 
        """ Moves the Knight from source to target. Returns true if the move is legal """ 

        pass 

    def __moveBishop(self, sourceTile, targetTile) -> bool: 
        """ Moves the Bishop from source to target. Returns true if the move is legal """ 

        pass 

    def __moveQueen(self, sourceTile, targetTile) -> bool: 
        """ Moves the Queen from source to target. Returns true if the move is legal """ 

        pass 

    def __moveKing(self, sourceTile, targetTile) -> bool: 
        """ Moves the King from source to target. Returns true if the move is legal """ 

        pass 

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
    Board() 
