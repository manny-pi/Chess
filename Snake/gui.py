import pygame 
import pygame.font as font

from pygame.time import Clock

from snake import Snake
from food import Food 

def snakeFoundFood(snake, food): 
    return snake.head.currPos == food.pos

def run(): 
    font.init() 

    WIDTH, HEIGHT = 800, 400
    GAME_WINDOW = pygame.display.set_mode((WIDTH, HEIGHT), display=0)

    GAME_CLOCK = Clock() 
    FRAMES_PER_SECOND = 6

    snake = Snake([0, 0]) 
    snake.setBoundaries(0, WIDTH, 0, HEIGHT) 
    food = Food([250, 100]) 

    SCORE            = 0 
    SCORE_TEXT       = font.SysFont(None, 30)
    SCORE_TEXT_COLOR = (255, 255, 255)
    SCORE_BOARD      = SCORE_TEXT.render(f'SCORE: {SCORE}', True, SCORE_TEXT_COLOR) 
    SPEED_UP         = False 

    running = True
    while running: 
        
        # EVENT HANDLING
        # - - - - - - - - - - - - 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                running = False 

            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_e or event.key == pygame.K_KP8: 
                    snake.goUp() 

                elif event.key == pygame.K_d or event.key == pygame.K_KP5: 
                    snake.goDown()  

                elif event.key == pygame.K_s or event.key == pygame.K_KP4: 
                    snake.goLeft()  

                elif event.key == pygame.K_f or event.key == pygame.K_KP6: 
                    snake.goRight() 

        # Execute if Snake found Food 
        # - - - - - - - - - 
        if snakeFoundFood(snake, food): 
            SCORE += 1
            SCORE_BOARD = SCORE_TEXT.render(f'SCORE: {SCORE}', True, SCORE_TEXT_COLOR) 

            snake.addSegment()
            food.changeLocation(WIDTH, HEIGHT) 

            if SCORE % 5 == 0: 
                SPEED_UP = True 

        if SPEED_UP:  
            FRAMES_PER_SECOND += 1
            SPEED_UP = False 

        print(snake)

        # Update Snake's position 
        # - - - - - - - - -    
        snake.updateSnake() 

        # Execute if Snake bit herself 
        # - - - - - - - - -    
        if snake.bitHerself(): 
            print(" - - - - DEAD - - - - " )

        # Draw Snake and Food 
        # - - - - - - - - -    
        GAME_WINDOW.fill((0, 0, 0)) 
        GAME_WINDOW.blit(food.surface, (food.x, food.y))
        for segment in snake: 
            GAME_WINDOW.blit(segment.surface, (segment.x, segment.y))

        # Draw score board 
        # - - - - - - - - -    
        GAME_WINDOW.blit(SCORE_BOARD, (10, 10))

        # Update the window 
        # - - - - - - - - -    
        pygame.display.flip() 
        GAME_CLOCK.tick(FRAMES_PER_SECOND)


if __name__ == '__main__': 
    run() 