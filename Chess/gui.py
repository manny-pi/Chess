import pygame 
from board import Board 


pygame.init() 

def run(): 
    WIDTH, HEIGHT = 560, 560 
    GAME_WINDOW = pygame.display.set_mode((WIDTH, HEIGHT), display=0)

    board = Board() 
    
    running = True
    while running:  

        pygame.display.flip() 
    pygame.quit() 


if __name__ == '__main__': 
    run() 
