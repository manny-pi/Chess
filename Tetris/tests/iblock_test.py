from sys import path 
path.append("/Users/Omani/Desktop/Personal/Education/Computer Science/Python/Python\
 Projects/PyGame-Projects/Tetris/blocks")

import pygame 
from basicblock import BasicBlock 
from iblock import IBlock
from blockattributes import * 

# Test the blocks 
def testBlock(): 

    # Initialize pygame 
    pygame.init() 

    # Set game dimensions 
    W, H = 500, 600
    WINDOW = pygame.display.set_mode((W, H), display=0)
    FRAMES_PER_SECOND = 2
    frames_passed = 0 
    
    # Create a block to test
    block = BasicBlock(Color.BLUE, 50, 150, 10) 

    # Create I-Block to test 
    i_init_x, i_init_y = 0, 100
    iblock = IBlock(Color.BLUE, i_init_x, i_init_y, Orientation.UP, 0)
    
    # Game clock 
    clock = pygame.time.Clock() 

    # Game loop
    running = True 
    while running: 

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False

        # Update the blocks location
        # - - - - - - - - - - 
        # block.y += 50
        iblock.goLeft() 
        iblock.goRight() 
        iblock.goDown() 

        # Change orientation of block when y = 
        if iblock.orientation != Orientation.RIGHT and frames_passed == 3: 
            iblock.changeOrientation(orientation=Orientation.RIGHT)
            print(" - - orientation changed - - up -> right ")
            print(repr(iblock))

        if iblock.orientation != Orientation.DOWN and frames_passed == 6: 
            iblock.changeOrientation(orientation=Orientation.DOWN)
            print(" - - orientation changed - - right -> down ")
            print(repr(iblock))
        
        # Clear the window 
        # - - - - - - - - - -   
        WINDOW.fill(Color.BLACK.value)

        # Render graphics 
        # - - - - - - - - - - 
        # window.blit(block.surface, (block.x, block.y))         # Render BasicBlock graphic
        for block in iblock:                                     # Render IBlock graphic
            WINDOW.blit(block.surface, (block.x, block.y))
        
        # Update the frame 
        pygame.display.flip() 

        # - - - - - - -
        clock.tick(FRAMES_PER_SECOND)
        frames_passed += 1 
        print(frames_passed)

    pygame.quit() 


if __name__ == "__main__":   
    testBlock()
