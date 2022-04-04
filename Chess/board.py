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

    def __lt__(self, other): 
        """ Returns True if this Number is nominally greater than other """
        
        return self.value > other.value

    def __gt__(self, other): 
        """ Returns True if this Number is nominally less than other """

        return self.value < other.value

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

    def __lt__(self, other): 
        return self.value < other.value 

    def __gt__(self, other): 
        return self.value > other.value 

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
            self.__moveKnight(targetTile) 

        elif isinstance(piece, Bishop):
            self.__moveBishop(targetTile)

        elif isinstance(piece, Queen): 
            self.__moveQueen(targetTile)
        
        elif isinstance(piece, King): 
            self.__moveKing(targetTile) 
 
    # Pawn methods 
    def __movePawn(self, targetTile): 
        """ Moves the Pawn from source to target if possible""" 

        pawn = self.activeTile.pieceHolding 

        sourceKey = self.activeTile.key 
        sKNum, sKLetter = sourceKey

        targetKey = targetTile.key
        tKNum, tKLetter = targetKey

        singleStep = abs(tKNum - sKNum) == 1
        doubleStep = abs(tKNum - sKNum) == 2
        canDoubleStep = pawn.canDoubleStep()

        moveVertically = tKLetter == sKLetter
        moveDiagonally = abs(tKLetter - sKLetter) >= 1

        targetIsEmpty = targetTile.pieceHolding == None 

        # Execute if Pawn is moving one step vertically or diagonally / Pawn is advancing or attacking
        if singleStep: 

            # ADVANCING 
            # - - - - - - - - - - - - - - - - - - - - - - - - 
            # Execute if Pawn is advancing (not attacking) / Pawn is moving vertically
            if moveVertically: 

                # Execute if there's no piece at targetTile / Advance Pawn
                if targetIsEmpty: 

                    # Execute if Pawn is White / White Pawn can only move UP vertically 
                    goingUp = tKNum - sKNum == 1
                    if pawn.team == Team.WHITE and goingUp:
                        targetTile.holdPiece(pawn)
                        self.activeTile.disposePiece()

                        pawn.singleStep()

                    # Execute if Pawn is Black / Black Pawn can only move DOWN vertically
                    elif pawn.team == Team.BLACK and not goingUp: 
                        targetTile.holdPiece(pawn) 
                        self.activeTile.disposePiece() 

                        # This Pawn can only take one step at a time now 
                        pawn.singleStep()
                
            # ATTACKING 
            # - - - - - - - - - - - - - - - - - - - - - - - - 
            # Execute if Pawn is attacking / Pawn is moving diagonally
            elif moveDiagonally: 

                # Execute if there's a piece at targetTile / Attack Enemy
                if not targetIsEmpty:

                    # Execute if Pawn is White and targetTile has a Black piece
                    whiteCanAttack = pawn.team is Team.WHITE and targetTile.pieceHolding.team is Team.BLACK
                    if whiteCanAttack: 
                        
                        # Move the Pawn to targetTile 
                        targetTile.disposePiece() 
                        targetTile.holdPiece(pawn) 

                        # Remove piece from activeTile
                        self.activeTile.disposePiece()

                        # This Pawn can only take one step at a time now 
                        pawn.singleStep()

                    # Execute if Pawn is Black and targetTile has a White piece 
                    blackCanAttack = pawn.team is Team.BLACK and targetTile.pieceHolding.team is Team.WHITE
                    if blackCanAttack: 

                        # Move the Pawn to targetTile
                        targetTile.disposePiece() 
                        targetTile.holdPiece(pawn) 

                        # Remove piece from activeTile
                        self.activeTile.disposePiece()

                        # This Pawn can only take one step at a time now 
                        pawn.singleStep()

        # Execute if Pawn is taking two steps forward vertically / Pawn is advancing two steps
        if doubleStep and canDoubleStep:  
            
            # Execute if Pawn is White and can take two steps 
            firstTileIsEmpty = self.__getTile(key=(tKNum, tKLetter)).pieceHolding == None 
            whiteCanMove =  firstTileIsEmpty and targetIsEmpty
            if whiteCanMove: 

                # Move the Pawn to targetTile 
                targetTile.holdPiece(pawn)
                self.activeTile.disposePiece()

            # This Pawn can only take one step at a time now 
            pawn.singleStep()

    # Rook methods 
    def __moveRook(self, targetTile): 
        """ Moves the Rook from activeTile to targetTile if possible """ 

        rook = self.activeTile.pieceHolding

        sourceKey = self.activeTile.key 
        sKNum, sKLetter = sourceKey

        targetKey = targetTile.key
        tKNum, tKLetter = targetKey

        moveVertically = tKLetter == sKLetter
        moveHorizontally = tKNum == sKNum

        # Execute if the Rook is moving vertically 
        if moveVertically: 

            # Check if the Rook can move vertically 
            if self.__rookCanMoveVert(rook, numFrom=sKNum, numTo=tKNum, letter=sKLetter): 
                pieceAtTarget = targetTile.pieceHolding != None 
                
                # Execute if there is no piece at target / Move rook to target 
                if pieceAtTarget: 
                    targetTile.disposePiece() 

                # Execute 
                targetTile.holdPiece(rook)

                # Dispose of the piece from activeTile    
                self.activeTile.disposePiece()
            
        # Execute if the Rook is moving horizontally 
        elif moveHorizontally: 
            # Check if the Rook can move vertically 
            if self.__rookCanMoveHor(rook, letterFrom=sKLetter, letterTo=tKLetter, num=sKNum): 
                pieceAtTarget = targetTile.pieceHolding != None 
                
                # Execute if there is no piece at target / Move rook to target 
                if pieceAtTarget: 
                    targetTile.disposePiece() 

                # Execute 
                targetTile.holdPiece(rook)

                # Dispose of the piece from activeTile    
                self.activeTile.disposePiece()

    def __rookCanMoveVert(self, rook: Rook, numFrom=None, numTo=None, letter=None) -> bool: 
        """ Checks wether or not rook can move vertically. Returns True if it can """

        # Execute so we traverse the numbers array properly / Very weird fix / Reimplement later 
        nums = list() 
        if numFrom > numTo: 
            nums = [n for n in Number]  # Regular order: 1, 2, ...
        else: 
            for num in Number: 
                nums.insert(0, num)     # Reverse order: 8, 7, ...

        checkTile = False 
        for num in nums:
            if checkTile: 

                # Execute if a piece was found between the rows 
                piece = self.boardMatrix[num.value][letter.value].pieceHolding
                if piece is not None: 
                    
                    # Execute if the piece is at the target tile
                    atTarget = num is numTo
                    if atTarget: 

                        # Execute if the piece is an enemy piece / Return True / Rook can move there 
                        if piece.team is not rook.team: 
                            return True 
                        
                        # Execute if the piece is the same team as the Rook / Rook can't move there 
                        else: 
                            return False

                    # Execute if the piece is not at the target tile / The piece is before the target tile 
                    else: 
                        return False 

            # Execute if we've processed this row 
            if num is numFrom: 
                checkTile = True 

            # Execute if we've reached the targetTile / End iteration 
            if num is numTo: 
                break 
            
        return True 
            
    def __rookCanMoveHor(self, rook: Rook, letterFrom=None, letterTo=None, num=None) -> bool: 
        """ Check wether or not rook can move horizontally. Returns True if it can """

        # Execute so we traverse the letters array properly / Very weird fix / Reimplement later 
        letters = list() 
        if letterFrom < letterTo: 
            letters = [l for l in Letter]   # Normal array; A, B, ...
        else: 
            for l in Letter: 
                letters.insert(0, l)      # Reverse array: H, G, ... 

        checkTile = False 
        for letter in letters: 
            if checkTile: 
                
                # Execute if a piece was found between letterFrom and letterTo 
                piece = self.boardMatrix[num.value][letter.value].pieceHolding
                if piece is not None: 
                    
                    # Execute if the piece is at the target tile
                    atTarget = letter is letterTo
                    if atTarget: 

                        # Execute if the piece is an enemy piece / Return True / Rook can move there 
                        if piece.team is not rook.team: 
                            return True 
                        
                        # Execute if the piece is the same team as the Rook / Rook can't move there 
                        else: 
                            return False

                    # Execute if the piece is not at the target tile / The piece is before the target tile 
                    else: 
                        return False 

            # Execute if we're past the letterFrom 
            if letter is letterFrom: 
                checkTile = True 

            # Execute if we've reached the targetTile / End iteration 
            if letter is letterTo: 
                break 
            
        return True
            
    # Knight methods 
    def __moveKnight(self, targetTile): 
        """ Move Knight from activeTile to targetTile if possible """ 

        pass 

    # Bishop methods 
    def __moveBishop(self, targetTile): 
        """ Move Bishop from activeTile to targetTile if possible """ 

        bishop = self.activeTile.pieceHolding
        sourceKeyNum, sourceKeyLetter, targetKeyNum, targetKeyLetter = self.__breakUp(self.activeTile, targetTile)

        # A bishop's move is legal if the number of moves vertically equals the number of moves horizontally 
        validMove = abs(targetKeyLetter - sourceKeyLetter) == abs(targetKeyNum - sourceKeyNum) 


    def __bishopCanMove(self, bishop: Bishop, tiles: list, target: Tile) -> bool: 
        """ Returns True if Bishop can move from activeTile to targetTile """ 
        
        numVertMoves = numTo - numFrom
        numHorMoves = letterTo - letterFrom
        movingDiagonally = abs(numVertMoves) == abs(numHorMoves)
        if movingDiagonally: 
            
            pass 
            
        
        return False 
        
    # Queen methods 
    def __moveQueen(self, targetTile): 
        """ Moves Queen from activeTile to targetTile if possible """ 

        pass 

    def __moveKing(self, targetTile): 
        """ Moves the King from activeTile to targetTile if possible """

        king = self.activeTile.pieceHolding
        if self.__kingCanMove(king, targetTile): 
            pieceAtTarget = targetTile.pieceHolding is not None
            if pieceAtTarget: 
                targetTile.disposePiece() 
            targetTile.holdPiece(king)
            self.activeTile.disposePiece()

    # King methods 
    def __kingCanMove(self, king, targetTile) -> bool: 
        """ Returns True if the King can move from the activeTile to the targetTile """ 

        sourceKey = self.activeTile.key 
        sKNum, sKLetter = sourceKey

        targetKey = targetTile.key
        tKNum, tKLetter = targetKey

        singleStep = abs(tKNum - sKNum) <= 1 and abs(sKLetter - tKLetter) <= 1

        # Execute if the King is taking a single step 
        if singleStep: 

            pieceAtTarget = targetTile.pieceHolding is not None 
            if pieceAtTarget: 
                enemyTeam = targetTile.pieceHolding.team is not king.team 
                if enemyTeam: 
                    return True
                else: 
                    return False 
            else: 
                return True 
            pass 

        return False 

    # Used in determining if pieces can move 
    def __breakUp(self, *tiles): 
        """ Returns a tuple containing the Number and Letter for a key """

        retVal = list() 
        for tile in tiles: 
            num, letter = tile.key
            retVal.append(num)
            retVal.append(letter)

        return retVal 

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
