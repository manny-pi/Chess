from pygame.sprite import Sprite 
from pygame import Surface
from pygame import image
from pygame import transform 


class BasicSprite(Sprite): 

    def __init__(self):
        super().__init__()

    def getX(self): 
        """ Returns the x-coordinate of the top left corner of the rect """ 
        
        return self.rect.left 

    def getY(self): 
        """ Returns the y-coordinate of the top left corner of the rect """ 

        return self.rect.top 
        

class Spaceship(BasicSprite):
    DELTA = 60
    TOP_BODER = 0
    BOTTOM_BORDER = 0
    
    def __init__(self): 
        super().__init__() 

        self.image = image.load('spaceship.png').convert() 
        self.image = transform.scale(self.image, (60, 60))

        self.rect  = self.image.get_rect(left=40)

    def moveUp(self):
        """ Move Spaceship up """

        if self.rect.top > Spaceship.TOP_BORDER: 
            self.rect.move_ip(0, -Spaceship.DELTA)

    def moveDown(self):
        """ Move Spaceship down """

        if self.rect.bottom < Spaceship.BOTTOM_BORDER:
            self.rect.move_ip(0, Spaceship.DELTA)

    def shoot(self):
        """ Returns a Bullet object """ 
        
        b_pos = self.rect.center
        return Bullet(b_pos)

    def __repr__(self): 

        return f'Spaceship(Pos=[{self.getX()}, {self.getY()}]'

    @classmethod 
    def setBorders(cls, *args): 
        cls.TOP_BORDER = args[0]
        cls.BOTTOM_BORDER = args[1]


class Alien(BasicSprite):
    DELTA = 5

    def __init__(self, x, y):
        super().__init__()

        self.image = image.load('alien.png').convert() 
        self.image = transform.scale(self.image, (60, 40))

        self.rect  = self.image.get_rect(topleft=(x, y))

    def moveLeft(self): 
        """ Move alien to the left """

        self.rect.move_ip(-Alien.DELTA, 0)


class Bullet(BasicSprite):
    DELTA = 10
    
    def __init__(self, pos):
        super().__init__()

        self.image = image.load('bullet.png').convert() 
        self.image = transform.scale(self.image, (40, 20))
        
        self.rect = self.image.get_rect(center=pos)
        

    def moveRight(self): 
        """ Move Bullet to the right """

        self.rect.move_ip(Bullet.DELTA, 0)
