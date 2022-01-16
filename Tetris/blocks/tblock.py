from basicblock import BasicBlock
from blockattributes import * 

from pygame.sprite import Group 

class TBlock: 
    """ The 'T' shape """

    def __init__(self, x, y, color, orientation, speed): 
        self.color        = color 
        self.orientation  = orientation 
        
        self.ref_block    = None        # Store reference block 
        self.left_app     = None        # Store the 'left' part of 'T'
        self.right_app    = None        # Store the 'right' part of 'T'
        self.bottom_app   = None        # Store the 'bottom' part of 'T'
        self.blocks       = None        # Store all the blocks / used for iteration
    
        self.group        = Group()     # Use to test for collision

        # Index for the iterator
        self.index = 0    

        if orientation == Orientation.UP: 
            self.blocks = [BasicBlock(color, x + (50 * i), y, speed) for i in range(0, 4)]

            self.ref_block  = self.blocks[0]
            self.left_app   = self.blocks[1]
            self.right_app  = self.blocks[2]
            self.bottom_app = self.blocks[3]

            # Set ref block 
            self.ref_block.x = x 
            self.ref_block.y = y

            # Set left_app 
            self.left_app.x = self.ref_block.x - 50 
            self.left_app.y = self.ref_block.y 

            # Set right_app 
            self.right_app.x = self.ref_block.x + 50 
            self.right_app.y = self.ref_block.y 

            # Set bottom_app 
            self.bottom_app.x = self.ref_block.x
            self.bottom_app.y = self.ref_block.y + 50

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
            
            # Move right_app under ref block 
            self.right_app.x = self.ref_block.x 
            self.right_app.y = self.ref_block.y + 50

            # Move left_app above ref block 
            self.left_app.x = self.ref_block.x 
            self.left_app.y = self.ref_block.y - 50

            # Move bottom_app to the left of ref block
            self.bottom_app.x = self.ref_block.x - 50
            self.bottom_app.y = self.ref_block.y 

            return 

        # Change from RIGHT -> DOWN 
        if self.orientation == Orientation.RIGHT: 
            self.orientation = Orientation.DOWN 

            # Move left_app to the right of ref block 
            self.left_app.x = self.ref_block.x + 50 
            self.left_app.y = self.ref_block.y 

            # Move right_app to the left of ref block
            self.right_app.x = self.ref_block.x - 50
            self.right_app.y = self.ref_block.y

            # Move bottom_app above the ref block 
            self.bottom_app.x = self.ref_block.x
            self.bottom_app.y = self.ref_block.y - 50 

            return 

        # Change from DOWN -> LEFT 
        if self.orientation == Orientation.DOWN: 
            self.orientation = Orientation.LEFT

            # Move left_app under ref block 
            self.left_app.x = self.ref_block.x 
            self.left_app.y = self.ref_block.y + 50

            # Move right_app above ref block 
            self.right_app.x = self.ref_block.x 
            self.right_app.y = self.ref_block.y - 50 

            # Move bottom_app to the right of ref block 
            self.bottom_app.x = self.ref_block.x + 50 
            self.bottom_app.y = self.ref_block.y

            return 
        
        # Change from LEFT -> UP 
        if self.orientation == Orientation.LEFT:
            self.orientation = Orientation.UP
            
            # Set left_app 
            self.left_app.x = self.ref_block.x - 50 
            self.left_app.y = self.ref_block.y 

            # Set right_app 
            self.right_app.x = self.ref_block.x + 50 
            self.right_app.y = self.ref_block.y 

            # Set bottom_app 
            self.bottom_app.x = self.ref_block.x
            self.bottom_app.y = self.ref_block.y + 50

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
        return f"ComplexBlock('T', {self.ref_block.x}, {self.ref_block.y}, {self.color}, {self.orientation})"



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
