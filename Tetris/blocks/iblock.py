from basicblock import BasicBlock
from blockattributes import * 
import pygame


class IBlock: 
    """ The 'I' shape """

    def __init__(self, x, y, color, orientation, speed): 
        self.color       = color 
        self.orientation = orientation   

        self.blocks      = None         # Store all the blocks / used for iteration 
        self.ref_block   = None         # Reference block used when changing orientation

        self.group        = Group()     # Use to test for collision

        # Index for the iterator
        self.index = 0 

        # Execute if the IBlock should be in the default orientation / Setup IBlock in Orientation.UP 
        if self.orientation   == Orientation.UP: 

            # Intialize constituent blocks of the IBlock; Assign a reference block 
            self.blocks = [BasicBlock(color, x + (50 * i), y, speed) for i in range(0, 4)]
            self.ref_block = self.blocks[0]

        elif self.orientation == Orientation.LEFT :
            pass 

        elif self.orientation == Orientation.RIGHT:
            pass 
        
        elif self.orientation == Orientation.DOWN: 
            pass 

        self.group.add(*self.blocks)

    def goLeft(self): 
        """ Used to move the block left """

        if self.orientation == Orientation.UP: 
            # if self.ref_block.x > 0: 
            for block in self.blocks: 
                block.x -= 50
    
        if self.orientation == Orientation.RIGHT: 
            # if self.ref_block.x > 0: 
            for block in self.blocks: 
                block.x -= 50

        if self.orientation == Orientation.DOWN:
            # if self.ref_block.x > 150: 
            for block in self.blocks: 
                block.x -= 50
        
        if self.orientation == Orientation.LEFT: 
            # if self.ref_block.x > 0: 
            for block in self.blocks: 
                block.x -= 50           
        
    def goRight(self): 
        """ Used to move the block right """ 

        if self.orientation == Orientation.UP: 
            # if self.ref_block.x < 300: 
            for block in self.blocks: 
                block.x += 50
    
        if self.orientation == Orientation.RIGHT: 
            # if self.ref_block.x < 450: 
            for block in self.blocks: 
                block.x += 50

        if self.orientation == Orientation.DOWN:
            # if self.ref_block.x < 450: 
            for block in self.blocks: 
                block.x += 50
        
        if self.orientation == Orientation.LEFT: 
            # if self.ref_block.x < 450: 
            for block in self.blocks: 
                block.x += 50                
 
    def goDown(self): 
        """ Used internally to control natural descent of block """   
        
        for block in self.blocks: 
            block.y += 50
    
    def speedUp(self): 
        """ Used when the user wants the block to descend faster """
        pass 

    def changeOrientation(self, orientation=None): 

        # Change from UP -> RIGHT 
        if self.orientation == Orientation.UP: 
            self.orientation = Orientation.RIGHT 
            
            i = 1
            for block in self.blocks: 
                if block is self.ref_block: 
                    block.x += 100
                    block.y -= 50
                else: 
                    block.x = self.ref_block.x
                    block.y = self.ref_block.y + 50 * i
                    i += 1
            return 

        # Change from RIGHT -> DOWN 
        if self.orientation == Orientation.RIGHT: 
            self.orientation = Orientation.DOWN 

            i = 1
            for block in self.blocks: 
                if block is self.ref_block: 
                    block.x -= 100
                    block.y += 100
                else: 
                    block.x = self.ref_block.x + 50 * i 
                    block.y = self.ref_block.y 
                    i += 1
            return 

        # Change from DOWN -> LEFT 
        if self.orientation == Orientation.DOWN: 
            self.orientation = Orientation.LEFT

            i = 1 
            for block in self.blocks: 
                if block is self.ref_block: 
                    block.x += 50
                    block.y -= 100
                else: 
                    block.x = self.ref_block.x
                    block.y = self.ref_block.y + 50 * i 
                    i += 1
            return 
        
        # Change from LEFT -> UP 
        if self.orientation == Orientation.LEFT:
            self.orientation = Orientation.UP
            
            i = 1 
            for block in self.blocks: 
                if block is self.ref_block: 
                    block.x -= 50
                    block.y += 50
                else: 
                    block.x = self.ref_block.x + 50 * i
                    block.y = self.ref_block.y 
                    i += 1 
            return 

    def __iter__(self):
        return self 

    def __next__(self): 
        if self.index <= len(self.blocks) - 1: 
            self.index += 1
            return self.blocks[self.index - 1]
        else: 
            self.index = 0
            raise StopIteration

    def __repr__(self): 
        return f"ComplexBlock('I', {self.ref_block.x}, {self.ref_block.y}, {self.color}, {self.orientation})"

    # DEBUGGER METHODS 
    # - - - - - - - - - - - - - - - - 
    # Used in debugging; returns the x coordinate of the ref_block 
    def x(self): 
        return self.ref_block.x 
    
    # Used in debugging; returns the y coordinate of the ref_block 
    def y(self): 
        return self.ref_block.y 

def random_color(): 
    from random import randint as r 
    i = r(1, 5)
    if i == 1: 
        return Color.RED
    if i == 2: 
        return Color.BLUE
    if i == 3: 
        return Color.CUTE 
    if i == 4: 
        return Color.PINK
    if i == 5: 
        return Color.GREEN
        