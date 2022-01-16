from sys import path 
path.append("/Users/Omani/Desktop/Personal/Education/Computer Science/Python/Python\
 Projects/PyGame-Projects/Tetris/blocks")

import pygame 
from basicblock import BasicBlock 
from blockattributes import * 
from iblock import IBlock
from pygame import mouse 

# Test the blocks 
def testBlock(): 

    # Initialize pygame 
    pygame.init()  

    # Set game dimensions 
    W, H = 500, 600
    WINDOW = pygame.display.set_mode((W, H), display=0)
    pygame.display.set_caption("iblock_test")
    FRAMES_PER_SECOND = 1.5
    frames_passed = 0 
    
    # Create I-Block to test 
    i_init_x, i_init_y = 100, 150
    iblock = IBlock(i_init_x, i_init_y, Color.BLUE, Orientation.UP, 0)
    print(repr(iblock))
    
    # Game clsk 
    clock = pygame.time.Clock() 

    # Game loop
    running = True 
    while running: 

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False

            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_a: 
                    print("Go left")
                    iblock.goLeft() 

                elif event.key == pygame.K_f:
                    iblock.goRight() 

                elif event.key == pygame.K_SPACE: 
                    iblock.changeOrientation() 

        # Move the block down 
        # - - - - - - - - - -   
        iblock.goDown() 
        
        # Clear the window 
        # - - - - - - - - - -   
        WINDOW.fill(Color.BLACK.value)

        # Render graphics 
        # - - - - - - - - - - 
        for block in iblock:                                     # Render IBlock graphic
            WINDOW.blit(block.surface, block.rect)
        
        # Update the frame 
        pygame.display.flip() 

        # - - - - - - -
        clock.tick(FRAMES_PER_SECOND)
        frames_passed += 1 
        # print(frames_passed)

    pygame.quit() 


if __name__ == "__main__":   
    testBlock()
