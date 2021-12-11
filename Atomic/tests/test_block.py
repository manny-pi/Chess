from sys import path 
path.append('/Users/Omani/Desktop/Personal/Education/Computer Science/Python/Python Projects/PyGame-Projects/Atomic/objects')

import pygame
import pygame.mouse as mouse
from block import Block 
from random import randint as rand

# Test the blocks 
def testBlock(): 

    # Initialize pygame 
    pygame.init() 

    # Set game dimensions 
    W, H = 500, 600
    WINDOW = pygame.display.set_mode((W, H), display=0)
    FRAMES_PER_SECOND = 10
    frames_passed = 0 
    
    # Create a block to test
    init_x, init_y = 150, 250
    block = Block(init_x, init_y) 

    
    # Game clock 
    clock = pygame.time.Clock() 

    # Game loop
    running = True 
    while running: 

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False

        # Execute if the mouse was left clicked 
        if mouse.get_pressed()[0] == 1: 
            x, y = mouse.get_pos()
            hor_bound = x >= block.x and x <= block.x + block.width
            vert_bound = y >= block.y and y <= block.y + block.height
            if hor_bound and vert_bound:          
                print("explosion") 
                block.x = rand(0, W-block.width)
                block.y = rand(0, H-block.height)

 
        # Update the blocks location
        # - - - - - - - - - - 


        
        # Clear the window 
        # - - - - - - - - - -   
        WINDOW.fill((0, 0, 0))

        # Render graphics 
        # - - - - - - - - - - 
        WINDOW.blit(block.surface, (block.x, block.y))
        
        # Update the frame 
        pygame.display.flip() 

        # - - - - - - -
        clock.tick(FRAMES_PER_SECOND)
        frames_passed += 1 

    pygame.quit() 


if __name__ == "__main__":   
    testBlock()
