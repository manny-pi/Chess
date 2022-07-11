import math
import numpy as np 
import pygame 
pygame.init() 


class AtomicGUI: 

    def __init__(self):

        # Set game dimensions 
        WINDOW_WIDTH = 500
        WINDOW_HEIGHT = 500 
        GAME_WINDOW = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH), display=0)

        # unit circle
        THETA = np.arange(0, 2*np.pi, (1/16)*np.pi)
        index = 0
        theta = THETA[0]
        xo = yo = 250
        RADIUS = 50
        x_cor = int(RADIUS * np.cos(theta))
        y_cor = int(RADIUS * np.sin(theta))

        LANDMARK = 300 # landmark for animation

        point_surface = pygame.Surface((20, 20)) 
        point_surface.fill((255, 0, 0))
        point_rect = point_surface.get_rect(center=(xo + x_cor, yo + y_cor))

        # animation data 
        UPDATE_THETA = pygame.USEREVENT + 1
        TIME_TO_UPDATE = 1000
        pygame.time.set_timer(UPDATE_THETA, TIME_TO_UPDATE)

        # Game loop
        running = True 

        while running: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    running = False

                if event.type == UPDATE_THETA: 
                    index = index + 1 if index + 1 < len(THETA) else 0 
                    theta = THETA[index]
                   
                    x_distance_from_landmark =  int(RADIUS * np.cos(theta) - LANDMARK)
                    y_distance_from_landmark = int(RADIUS * np.sin(theta) - LANDMARK)

                    x_cor = LANDMARK - x_distance_from_landmark
                    y_cor = LANDMARK - y_distance_from_landmark

                    point_rect.move_ip(x_cor, y_cor)
                    
            GAME_WINDOW.fill((0, 0, 0))
            GAME_WINDOW.blit(point_surface, point_rect)
            pygame.display.flip()


AtomicGUI() 
