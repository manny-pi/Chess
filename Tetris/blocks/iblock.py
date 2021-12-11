from basicblock import BasicBlock
from blockattributes import * 

class IBlock: 
    """ The 'I' shape """

    def __init__(self, color, x, y, orientation, speed): 
        self.color       = color 
        self.orientation = orientation   
        self.speed       = speed

        self.blocks      = None         # Store all the BasicBlocks in the shape 
        self.ref_block   = None         # Reference block used when changing orientation

        # NOTE: find another way to implement index for __next__  
        self.index       = 0 

        # Execute if the Block should be in the default 
        if self.orientation   == Orientation.UP: 

            # Set the coordinates of the trailing blocks 
            self.blocks = [BasicBlock(color, x + 50 * i, y, speed) for i in range(0, 4)]
            self.ref_block = self.blocks[0]

        elif self.orientation == Orientation.LEFT :
            pass 

        elif self.orientation == Orientation.RIGHT:
            pass 
        
        elif self.orientation == Orientation.DOWN: 
            pass 

    def goLeft(self): 
        """ Used to move the block left """
        
        for block in self.blocks: 
            if self.orientation == Orientation.UP: 
                if self.ref_block.x >= 0: 
                    block.x -= 50

            elif self.orientation == Orientation.RIGHT: 
                if self.ref_block.x >= 0: 
                    block.x -= 50
        
    def goRight(self): 
        """ Used to move the block right """ 

        for block in self.blocks: 
            if self.orientation == Orientation.UP: 
                if self.ref_block.x < 450:  
                    block.x += 50 
 
    def goDown(self): 
        """ Used to control natural descent of block """   

        for block in self.blocks: 
            if self.orientation == Orientation.UP: 
                if self.ref_block.y < 550: 
                    block.y += 50

            elif self.orientation == Orientation.RIGHT: 
                if self.ref_block.y < 450: 
                    block.y += 50

            elif self.orientation == Orientation.DOWN: 
                if self.ref_block.y < 550: 
                    block.y += 50 
                    
    def speedUp(self): 
        """ Used when the user wants the block to descend faster """
        pass 

    # Set kwarg 'orientation' to None for testing purposes
        # During actual gameplay, the orientation of the block 
        # will be decided internally by the changeOrientation function itself 
    def changeOrientation(self, orientation=None): 
        # Execute if we're testing 
        if orientation is not None: 
            if orientation == Orientation.UP: 
                pass 

            elif orientation == Orientation.LEFT: 
                pass 

            elif orientation == Orientation.DOWN: 
                self.orientation = Orientation.DOWN     # Set the orientation of the block
                i = 1
                off_set = 50       # off_set with go down 
                for block in self.blocks: 
                    if block is self.ref_block: 
                        block.x += 50 + off_set    # Move reference block [x] unit right 
                        block.y += 50              # Move reference block [y] units up 
                    else: 
                        block.x = self.ref_block.x - 50 * i 
                        block.y = self.ref_block.y 
                        i += 1 

            elif orientation == Orientation.RIGHT:
                self.orientation = Orientation.RIGHT    # Set the orientation of the block
                i = 1
                for block in self.blocks: 
                    if block is self.ref_block: 
                        block.x += 100      # Move reference block 3 units right 
                        block.y -= 50       # Move reference block 1 unit up 
                    else: 
                        block.x = self.ref_block.x 
                        block.y = self.ref_block.y + 50 * i 
                        i += 1
            
            return 
        
        # Execute if we're running game play 

    def __iter__(self):
        return self 

    def __next__(self): 
        if self.index == len(self.blocks)-1: 
            self.index = 0      # Reset the index 
            raise StopIteration 
        self.index += 1
        return self.blocks[self.index]
        
    def __repr__(self): 
        return f"ComplexBlock('I', {self.color}, {self.orientation})"


    # DEBUGGER METHODS 
    # - - - - - - - - - - - - - - - - 
    # Used in debugging; returns the x coordinate of the ref_block 
    def x(self): 
        return self.ref_block.x 
    
    # Used in debugging; returns the y coordinate of the ref_block 
    def y(self): 
        return self.ref_block.y 
