import pygame
import random
from pygame.locals import *
from _SpriteBodies import SpriteBodies

# GAME INVARIABLES
# - - - - - - - - - - -
windowWidth = 800
windowHeight = 700

class Bucket(SpriteBodies.PlayerSprite):
    def __init__(self, init_x=0, init_y=0, speed=5, img=None):
        super().__init__(100, 10, init_x, init_y, speed, img)

    def update(self, pressed_keys):
        if pressed_keys[K_a]:
            if self.rect.left - self.speed >= 0:
                self.rect.move_ip(-self.speed, 0)

        if pressed_keys[K_d]:
            if self.rect.right + self.speed <= windowWidth:
                self.rect.move_ip(self.speed, 0)


class Raindrop(SpriteBodies.EnemySprite):
    def __init__(self, init_x=0, init_y=0, speed=5, img=None):
        super().__init__(init_x, init_y, speed, img)

    def update(self, collisionDetected=False):
        if self.rect.top >= 700 or collisionDetected:
            self.kill()
        else:
            self.rect.move_ip(0, self.speed)


class StatusBar:
    pass


class RaindropsGUI:
    def __init__(self):
        # Initialize the 'pygame' modules
        pygame.init()

        # Set up the 'game_window'
        self.game_window = pygame.display.set_mode((windowWidth, windowHeight))
        bg = "/Users/Omani/Desktop/Python/Python Projects/PyGame Projects/Raindrops/Images/bg.png"
        background_img = pygame.image.load(bg).convert_alpha()
        background_img.set_colorkey((255, 255, 255))

        # Load the images
        rain = "/Users/Omani/Desktop/Python/Python Projects/PyGame Projects/Raindrops/Images/rain.png"
        bucket = "/Users/Omani/Desktop/Python/Python Projects/PyGame Projects/Raindrops/Images/bucket.png"

        rain_img = pygame.image.load(rain)
        bucket_img = pygame.image.load(bucket).convert_alpha()

        # Set up the sprites and sprite groups
        self.bucket = Bucket(init_x=0, init_y=580, speed=100)
        self.raindrops = pygame.sprite.Group()

        # Create custom event to generate raindrops
        add_rain = pygame.USEREVENT + 1
        # Add the event to the 'event queue' every 250 milliseconds
        pygame.time.set_timer(add_rain, 1000)

        # Player information
        self.PLAYER_SCORE = 0

        # Game Loop
        running = True
        while running:

            # Event handler
            for event in pygame.event.get():
                # QUIT GAME
                if event.type == pygame.QUIT:
                    running = False

                # Handle user event
                elif event.type == pygame.KEYDOWN:
                    pressed_keys = pygame.key.get_pressed()
                    self.bucket.update(pressed_keys)

                # Generate raindrops
                elif event.type == add_rain:
                    rain = Raindrop(init_x=random.randint(0, 800))
                    self.raindrops.add(rain)

            # Check if some 'rain' entered the bucket
            collectedRain = pygame.sprite.spritecollideany(self.bucket, self.raindrops)
            if collectedRain is not None:
                collectedRain.update(collisionDetected=True)

                # Increase PLAYER_SCORE
                self.PLAYER_SCORE += 1
                print(self.PLAYER_SCORE)

            # Update the rain positions
            for raindrop in self.raindrops:
                raindrop.update()

            # Refresh the background
            self.game_window.fill((0, 0, 0))

            # Draw the sprites
            self.game_window.blit(self.bucket.surface, self.bucket.rect)
            for raindrop in self.raindrops:
                self.game_window.blit(raindrop.surface, raindrop.rect)

            # Update the display
            pygame.display.flip()


gui = RaindropsGUI()
