import pygame
import pygame.mouse

from board import *
from piece import * 


WIDTH = HEIGHT = 600 
GAME_WINDOW = pygame.display.set_mode((WIDTH, HEIGHT), display=0)

board = Board()

tile: Tile = board.boardMatrix[Number.THREE.value][Letter.E.value]
pawn: Pawn = Pawn(key=tile.key, pos=tile.pos)

tile.holdPiece(pawn)

print(tile)
print(pawn)
print(tile.rect)


def run(): 

    running = True
    while running:  

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                running = False 

            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos() 
                board.selectTile(x, y)

        for tile in board: 
            GAME_WINDOW.blit(tile.surface, tile.rect) 
        tile.surface.blit(pawn.image, pawn.rect)
        GAME_WINDOW.blit(tile.surface, tile.rect)


        pygame.display.flip() 
    pygame.quit() 


if __name__ == '__main__': 
    run() 
