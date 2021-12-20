from basicblock import BasicBlock
from blockattributes import * 

class OBlock: 
    """ The 'J' shape """

    def __init__(self, x, y, color, orientation, speed): 
        self.color        = color 
        self.orientation  = Orientation.UP 

        self.ref_block    = None        # Store reference block 
        self.blocks       = None        # Store all the blocks / used for iteration

        # Index for the iterator
        self.index = 0  

        # Execute if the LBlock should be in the default orientation / Setup iblock in Orientation.UP 
        if self.orientation   == Orientation.UP: 

            # Intialize constituent blocks of the IBlock; Assign a reference block 
            self.blocks = [BasicBlock(random_color(), x + (50 * i), y, speed) for i in range(0, 4)]

            self.ref_block = self.blocks[0]

            self.blocks[1].x = self.ref_block.x 
            self.blocks[1].y = self.ref_block.y - 50 

            self.blocks[2].x = self.ref_block.x + 50
            self.blocks[2].y = self.ref_block.y - 50       

            self.blocks[3].x = self.ref_block.x + 50
            self.blocks[3].y = self.ref_block.y  

        elif self.orientation == Orientation.LEFT :
            pass
        
        elif self.orientation == Orientation.RIGHT:
            pass
        
        elif self.orientation == Orientation.DOWN: 
            pass

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
    
    def changeOrientation(self, orientation=None): 
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
 