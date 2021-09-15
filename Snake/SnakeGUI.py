import pygame

class Snake(pygame.sprite.Sprite):

    pass

class SnakeGUI:
    def __init__(self):
        # Invariables
        WIDTH = 500
        HEIGHT = 500
        self.gameWindow = pygame.display.set_mode([WIDTH, HEIGHT])

        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update the game display
            pygame.display.flip()


s = SnakeGUI()
