import pygame 
from robot import Robot 


class Environment:
    
    def __init__(self): 
        """Declare the environment variables"""

        self.width = 1250
        self.height = 500
        self.window = pygame.display.set_mode((self.width, self.height))
        self.robot = Robot(self)

    def run(self): 
        running = True 
        while running: 
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    running = False 

                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_SPACE:
                        self.robot.jump()
            
            # Displace the Robot along the y-axis
            if self.robot.isJumping(): 
                self.robot.y_displ()

            # Update Robot location
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_LEFT]: self.robot.goLeft(); print(self.robot.rect)
            elif pressed_keys[pygame.K_RIGHT]: self.robot.goRight(); print(self.robot.rect)

            self.clearWindow()
            self.window.blit(self.robot.surface, self.robot.rect)
            pygame.display.flip()

    def clearWindow(self): 
        """ 
        Clears the window
        """

        self.window.fill((0, 0, 0))

Environment().run()
