import math
import numpy as np 
import pygame 
pygame.init() 


# Set game dimensions 
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500 
GAME_WINDOW = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH), display=0)

# unit circle data 
MIN = 0 
MAX = 2 * np.pi
THETA = np.arange(MIN, MAX, np.pi/60)
index = 0
theta = THETA[index]
xo = yo = 250 # origin
RADIUS = 100
x_cor = xo + int(RADIUS * np.cos(theta))
y_cor = yo + int(RADIUS * np.sin(theta))

# point data
point_surface = pygame.Surface((20, 20)) 
point_surface.fill((255, 0, 0))
point_rect = point_surface.get_rect(center=(x_cor, y_cor))

# animation data 
UPDATE_THETA = pygame.USEREVENT + 1
TIME_TO_UPDATE = 50
pygame.time.set_timer(UPDATE_THETA, TIME_TO_UPDATE)

# animation loop
running = True 
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False

        if event.type == UPDATE_THETA: 
            index = index + 1 if index + 1 < len(THETA) else 0 
            theta = THETA[index]

            old_x = x_cor 
            old_y = y_cor
            x_cor = xo + int(RADIUS * np.cos(theta))
            y_cor = yo + int(RADIUS * np.sin(theta))    

            disp_x = x_cor - old_x
            disp_y = y_cor - old_y

            point_rect.move_ip(disp_x, -disp_y)
            
    GAME_WINDOW.fill((0, 0, 0))
    GAME_WINDOW.blit(point_surface, point_rect)
    pygame.display.flip()


