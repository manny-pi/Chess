import pygame 


class AtomicGUI: 

    def __init__(self):

        # Initialize pygame 
        pygame.init() 

        # Set game dimensions 
        WINDOW_HEIGHT = 600 
        WINDOW_WIDTH = 500
        GAME_WINDOW = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH), display=0)

        # Game loop
        running = True 

        while running: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    running = False


AtomicGUI() 
