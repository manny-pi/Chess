import pygame

""" This module contains basic sprite bodies.  It allows you to add images to your sprites, and set the speed at which your sprite will move
"""

class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, surf_w, surf_h, init_x=0, init_y=0, speed=5, img=None):
        
        # Call the Constructor of the parent class 
        super(PlayerSprite, self).__init__()
        
        # Set the dimensions of the surface that we'll draw shapes and images to
        self.surface = pygame.Surface((surf_w, surf_h))
        
        # Get the rectangular area which images are drawn to 
        self.rect = self.surface.get_rect(topleft=(init_x, init_y))

        # Set the sprite speed
        self.speed = speed

        # Set the sprite graphic
        if img is not None:
            self.surface = pygame.transform.scale(img.convert(), (20, 20)) 
        else:
            self.surface.fill((255, 255, 255))


class EnemySprite(pygame.sprite.Sprite):
    def __init__(self, init_x=0, init_y=0, speed=5, img=None):
        super(EnemySprite, self).__init__()
        self.surface = pygame.Surface((40, 40))
        self.rect = self.surface.get_rect(center=(init_x, init_y))

        # Set the sprite speed
        self.speed = speed

        # Set the sprite graphic
        if img is not None:
            self.surface = img.convert()
        else:
            self.surface.fill((255, 0, 0))


class OtherSprite(pygame.sprite.Sprite):
    def __init__(self, init_x=0, init_y=0, speed=10, img=None):
        super(OtherSprite, self).__init__()
        
        self.surface = pygame.Surface((30, 10))
        self.rect = self.surface.get_rect(topleft=(init_x, init_y))
        
        # Set the sprite speed
        self.speed = speed

        # Set the sprite graphic
        if img is not None: 
          # Use the convert method to speed up blitting
          self.surface = img.convert()  

        # Set the surface color as gold 
        else: 
          self.surface.fill((255, 215, 0))

        
