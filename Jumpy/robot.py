from pygame.sprite import Sprite 
from pygame import Surface

from time import time

class Robot(Sprite): 
    def __init__(self, env): 
        self.env = env 

        self.width = self.height = 25
        self.surface = Surface((self.width, self.height))

        self.rect = self.surface.get_rect(bottomleft=(200, env.height))
        self.x, self.y = self.rect.bottomleft
        self.color = (0, 255, 0) 
        self.surface.fill(self.color) 

        self.jumping = False 
        self.timeSinceJump = 0
    
        self.VELOCITY = -30
        self.ACCEL = 1.8

    def jump(self): 
        """
        Sets jumping to True
        """ 
        
        self.jumping = True 

    def isJumping(self): 
        """
        Return True if Robot is jumping / False if Robot is not jumping
        """ 
        
        return self.jumping
    
    def y_displ(self):
        """
        Determines the displacement of the robot along the y-axis / Updates y-cor
        """

        # Execute if Robot is already jumping
        self.timeSinceJump += 0.45
        self.y = self.env.height + self.VELOCITY*self.timeSinceJump + self.ACCEL*(self.timeSinceJump ** 2)
        self.rect = self.surface.get_rect(bottomleft=(self.x, self.y))

        # Reset the jump parameters if Robot has landed
        if self.y >= self.env.height: 
            self.jumping = False
            self.timeSinceJump = 0

            print('<<< landed >>>')

        # Execute if Robot just started jumping
        else: 
            self.jumping = True

    def goLeft(self): 
        """
        Move the Robot left
        """ 
        
        self.x -= 5
        self.rect.move_ip(-5, 0)

    def goRight(self): 
        """
        Move the Robot right
        """
        
        self.x += 5
        self.rect.move_ip(5, 0)

    def __repr__(self): 
        return f'Robot([{self.x}, {self.y:.3f}])'