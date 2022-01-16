from basicblock import BasicBlock
from blockattributes import * 

from pygame.sprite import Group 

class LBlock: 
    """ The 'L' shape """

    def __init__(self, x, y, color, orientation, speed): 
        self.color        = color 
        self.orientation  = orientation 

        self.ref_block    = None        # Store reference block 
        self.short_app    = None        # Store the 'short' part of the 'L'
        self.long_app     = None        # Store the 'long' part of the 'L'

        self.blocks       = None        # Store all the blocks / used for iteration

        self.group        = Group()     # Use to test for collision
        
        # Index for the iterator
        self.index = 0  

        # Execute if the LBlock should be in the default orientation / Setup iblock in Orientation.UP 
        if self.orientation   == Orientation.UP: 

            # Intialize constituent blocks of the IBlock; Assign a reference block 
            self.blocks = [BasicBlock(color, x + (50 * i), y, speed) for i in range(0, 4)]

            # Assign the 1. reference block, 2. short appendage, and 3. long appendage 
            self.ref_block = self.blocks[0]
            self.short_app = self.blocks[1]
            self.long_app  = [self.blocks[2], self.blocks[3]]

            # Set the L-block 
            self.ref_block.x = x 
            self.ref_block.y = y 

            # Set the location of the short appendage 
            self.short_app.x = self.ref_block.x + 50
            self.short_app.y = self.ref_block.y 

            # Set the location of the long appendage 
            i = 1
            for block in self.long_app: 
                block.x = self.ref_block.x 
                block.y = self.ref_block.y - 50 * i 
                i += 1

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
                block.x += 50
        
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

    def changeOrientation(self): 
        """ Change the orientation of the shape """ 

        # Change UP -> RIGHT 
        if self.orientation == Orientation.UP:
            self.orientation = Orientation.RIGHT 

            # Move ref block 2 units up 
            self.ref_block.y -= 100

            # Move short_app underneath ref block 
            self.short_app.x = self.ref_block.x 
            self.short_app.y = self.ref_block.y + 50 

            # Move long_app to the right of ref block
            i = 1
            for block in self.long_app: 
                block.x = self.ref_block.x + 50 * i 
                block.y = self.ref_block.y 
                i += 1

            return

        # Change RIGHT -> DOWN 
        if self.orientation == Orientation.RIGHT:
            self.orientation = Orientation.DOWN 

            # Move ref block 2 units right 
            self.ref_block.x += 100

            # Move short_app to the left of ref block 
            self.short_app.x = self.ref_block.x - 50
            self.short_app.y = self.ref_block.y

            # Move long_app underneath ref block 
            i = 1 
            for block in self.long_app: 
                block.x = self.ref_block.x 
                block.y = self.ref_block.y + 50 * i
                i += 1

            return  

        # Change DOWN -> LEFT 
        if self.orientation == Orientation.DOWN: 
            self.orientation = Orientation.LEFT

            # Move ref block 2 units down 
            self.ref_block.y += 100
            
            # Move short_app above ref block 
            self.short_app.x = self.ref_block.x 
            self.short_app.y = self.ref_block.y - 50

            # Move long_app to the left of ref block 
            i = 1 
            for block in self.long_app: 
                block.x = self.ref_block.x - 50 * i 
                block.y = self.ref_block.y 
                i += 1

            return  

        # Change LEFT -> UP 
        if self.orientation == Orientation.LEFT: 
            self.orientation = Orientation.UP

            # Move ref block 2 units left 
            self.ref_block.x -= 100

            # Move short_app to the right of ref block 
            self.short_app.x = self.ref_block.x + 50 
            self.short_app.y = self.ref_block.y 

            # Move long_app above ref block 
            i = 1
            for block in self.long_app: 
                block.x = self.ref_block.x 
                block.y = self.ref_block.y - 50 * i 
                i += 1

            return 

    # DEBUGGER METHODS 
    # - - - - - - - - - - - - - - - - 
    # Used in debugging; returns the x coordinate of the ref_block 
    def x(self): 
        return self.ref_block.x 
    
    # Used in debugging; returns the y coordinate of the ref_block 
    def y(self): 
        return self.ref_block.y 

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
        return f"ComplexBlock('L', {self.ref_block.x}, {self.ref_block.y}, {self.color}, {self.orientation})"


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
 