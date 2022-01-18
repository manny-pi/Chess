import pygame
import pygame.mouse

from board import *
from piece import * 

from math import floor 

WIDTH = HEIGHT = 600 
GAME_WINDOW = pygame.display.set_mode((WIDTH, HEIGHT), display=0)

board = Board()
def run(): 

    running = True
    while running:  

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                running = False 

            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos() 
                kLetter = floor(x/75)
                kNum = floor(y/75)
                board.selectTile(key=(kNum, kLetter))

        for tile in board: 
            GAME_WINDOW.blit(tile.surface, tile.rect) 
        # tile.surface.blit(pawn.image, pawn.rect)
        # GAME_WINDOW.blit(tile.surface, tile.pos)


        pygame.display.flip() 
    pygame.quit() 


if __name__ == '__main__': 
    run() 
