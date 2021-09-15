import pygame

class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, surf_w, surf_h, init_x=0, init_y=0, speed=5, img=None):
        super(PlayerSprite, self).__init__()
        self.surface = pygame.Surface((surf_w, surf_h))
        self.rect = self.surface.get_rect(topleft=(init_x, init_y))

        # Set the sprite speed
        self.speed = speed

        # Set the sprite graphic
        if img is not None:
            self.surface = img.convert()
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
    def __init__(self, init_x=0, init_y=0, speed=10):
        super(OtherSprite, self).__init__()
        self.surface = pygame.Surface((30, 10  ))
        self.surface.fill((255, 215, 0))
        self.rect = self.surface.get_rect(topleft=(init_x, init_y))
        self.speed = speed
