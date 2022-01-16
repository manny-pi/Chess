import pygame 
from pygame.sprite import Group, spritecollideany, groupcollide 

from blockattributes import * 
from iblock import IBlock
from jblock import JBlock 
from lblock import LBlock
from oblock import OBlock 
from sblock import SBlock
from tblock import TBlock
from pygame import mouse 

from random import randint as r 
from math import ceil 

# Test the blocks 
def testBlock(): 

    # Initialize pygame 
    pygame.init() 

    # Set game dimensions 
    W, H = 600, 800
    WINDOW = pygame.display.set_mode((W, H), display=0)
    pygame.display.set_caption("stacking_test")

    FRAMES_PER_SECOND = 4
    clock = pygame.time.Clock()         
    frames_passed = 0
    
    # First block of the game 
    falling_block = gen_block(W)    

    # Store the blocks that have been generated in the game 
    game_blocks = [falling_block]  

    # Store constituent blocks / Used for collision detection 
    block_const = Group() 

    # Game loop
    running = True 
    while running: 
        
        # EVENT HANDLING 
        # - - - - - - - - - - - - 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False

            # Execute if a user presses a key 
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_a: 
                    falling_block.goLeft() 

                elif event.key == pygame.K_f:
                    falling_block.goRight() 

                elif event.key == pygame.K_SPACE:
                    falling_block.changeOrientation() 

        # Check if 'falling_block' landed on any existing blocks
        # - - - - - - - - - - - - 
        if len(game_blocks) > 1: 
            print(falling_block)
            

        #     # Iterate over the constituents of the falling block
        #     for block in falling_block: 
        #         print(" - - - - - - - - - - - - - - - - - - -")
                
        #         in_set = spritecollideany(block, block_const, collision)   # Store the blocks that falling_block landed on
        #         if in_set: 
        #             print(" - - - - Collision Detected - - - -")
        #             print(in_set, '\n')
        #             store_constituents(falling_block, block_const)
        #             falling_block = gen_block(W)
        #             game_blocks.append(falling_block)

        #     # Execute if falling_block didn't land on anything, and is at the bottom of the screen 
        #         if falling_block.y() == H - 50: 
        #             store_constituents(falling_block, block_const)      # Store the constituent blocks of falling block 
        #             falling_block = gen_block(W)                        # Create a falling_block 
        #             game_blocks.append(falling_block)                   # Add it to the list of game_blocks 

        # Execute if only one block has been generated so far
        else: 
            if falling_block.y() == H - 50: 
                store_constituents(falling_block, block_const)      # Store the constituent blocks of falling block 
                falling_block = gen_block(W)                        # Create a falling_block 
                game_blocks.append(falling_block)                   # Add it to the list of game_blocks

        # Move 'falling_block' down
        # - - - - - - - - - - - - 
        falling_block.goDown() 
        
        # Fill the window background
        # - - - - - - - - - - - - 
        WINDOW.fill((0, 0, 0))

        # Render all game blocks 
        # - - - - - - - - - - - - 
        for complexBlock in game_blocks: 
            for block in complexBlock:                            
                WINDOW.blit(block.surface, (block.x, block.y))

        # Update the frame 
        # - - - - - - - - - - - - 
        pygame.display.flip() 

        # Next Frame
        # - - - - - - - - - - - - 
        clock.tick(FRAMES_PER_SECOND)
        frames_passed += 1 

    pygame.quit() 

def collision(block_a, block_b): 

    if block_a.bottom() == block_b.top() and block_a.x == block_b.x:
        return True

    return False 

def gen_block(W): 
    """ Generates a random block """

    block_choice = r(1, 6) 
    color_choice = r(1, 6)
    x = 50 * ceil( r(0, W-100) / 50 )
    
    if color_choice == 1: 
        color = Color.RED

    if color_choice == 2: 
        color = Color.BLUE

    if color_choice == 3: 
        color = Color.GREEN

    if color_choice == 4: 
        color = Color.SKY_BLUE

    if color_choice == 5: 
        color = Color.YELLOW

    if color_choice == 6: 
        color = Color.ORANGE

    if block_choice == 1: 
        return IBlock(x, -100, color, Orientation.UP, 0)

    if block_choice == 2: 
        return JBlock(x, -100, color, Orientation.UP, 0)

    if block_choice == 3: 
        return LBlock(x, -100, color, Orientation.UP, 0)

    if block_choice == 4: 
        return OBlock(x, -100, color, Orientation.UP, 0)

    if block_choice == 5: 
        return SBlock(x, -100, color, Orientation.UP, 0)

    if block_choice == 6: 
        return TBlock(x, -100, color, Orientation.UP, 0)

def store_constituents(block, sprite_group): 
    for b in block: 
        sprite_group.add(b)


if __name__ == "__main__":   
    testBlock()
