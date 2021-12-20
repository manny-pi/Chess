from basicblock import BasicBlock
from blockattributes import * 

class SBlock: 
    """ The 'snake-like' shape """

    def __init__(self, x, y, color, orientation, speed): 
        self.color        = color 
        self.orientation  = orientation 

        self.ref_block    = None        # Store reference block 
        self.left_app     = None        # Store left appendage 
        self.bottom_app   = None        # Store top appendage 
        self.right_app    = None        # Store right appendage
        self.blocks       = None        # Store all the blocks / used for iteration

        # Index for the iterator
        self.index = 0  

        # Execute if the LBlock should be in the default orientation / Setup iblock in Orientation.UP 
        if self.orientation   == Orientation.UP: 

            # Intialize constituent blocks of the IBlock; Assign a reference block 
            self.blocks = [BasicBlock(random_color(), x + (50 * i), y, speed) for i in range(0, 4)]

            # Set the appendages
            self.ref_block  = self.blocks[0]
            self.left_app   = self.blocks[1]
            self.bottom_app = self.blocks[2]
            self.right_app  = self.blocks[3]

            # Set left_app below and to the left of ref block 
            self.left_app.x = self.ref_block.x - 50
            self.left_app.y = self.ref_block.y + 50

            # Set the bottom_app below ref block
            self.bottom_app.x = self.ref_block.x 
            self.bottom_app.y = self.ref_block.y + 50

            # Set the right_app to the right of ref block
            self.right_app.x = self.ref_block.x + 50
            self.right_app.y = self.ref_block.y

    def goLeft(self): 
        """ Used to move the block left """
        
        for block in self.blocks: 
            block.x -= 50 

    def goRight(self): 
        """ Used to move the block right """ 
        
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

            # Move left_app 1 unit left and 1 unit above ref block 
            self.left_app.x = self.ref_block.x - 50 
            self.left_app.y = self.ref_block.y - 50 

            # Move bottom_app 1 unit left of ref block 
            self.bottom_app.x = self.ref_block.x - 50
            self.bottom_app.y = self.ref_block.y

            # Move right_app under ref block
            self.right_app.x = self.ref_block.x 
            self.right_app.y = self.ref_block.y + 50

            return

        # Change RIGHT -> UP 
        if self.orientation == Orientation.RIGHT:
            self.orientation = Orientation.UP 

            # Move left_app 1 unit down and 1 unit left of ref block
            self.left_app.x = self.ref_block.x - 50
            self.left_app.y = self.ref_block.y + 50

            # Move bottom_app under ref block
            self.bottom_app.x = self.ref_block.x 
            self.bottom_app.y = self.ref_block.y + 50

            # Move right_app to the right of ref block
            self.right_app.x = self.ref_block.x + 50
            self.right_app.y = self.ref_block.y

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
 