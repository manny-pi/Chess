import _SpriteBodies.SpriteBodies as spritebody
import pygame
from pygame.locals import *
import random


class Shooter(spritebody.PlayerSprite):
    SHOOTER_IMAGE = pygame.image.load("./ShooterDemo/GUI/shooter.png")
    SHOOTER_IMAGE = pygame.transform.scale(SHOOTER_IMAGE, (60, 60))

    def __init__(self, surf_w, surf_h, init_x=0, init_y=0, speed=5):
        super().__init__(surf_w, surf_h, init_x, init_y, speed, img=Shooter.SHOOTER_IMAGE) 

    def update(self, pressed_keys, window_width,
               window_height):
        # Move player up
        if pressed_keys[K_w]:
            if self.rect.top - self.speed >= 20:
                self.rect.move_ip(0, -self.speed)

        # Move player down
        if pressed_keys[K_s]:
            if self.rect.bottom + self.speed <= window_height - 20:
                self.rect.move_ip(0, self.speed)

    def shoot(self):
        b_init_x = self.rect.left
        b_init_y = self.rect.top + 20
        return Bullet(init_x=b_init_x, init_y=b_init_y)


class Enemy(spritebody.EnemySprite):
    ENEMY_IMAGE = pygame.image.load("./ShooterDemo/GUI/enemy.png")
    ENEMY_IMAGE = pygame.transform.scale(ENEMY_IMAGE, (60, 20))

    def __init__(self, init_x=0, init_y=0, speed=8):
        super().__init__(init_x, init_y, speed, img=Enemy.ENEMY_IMAGE)

    def update(self, collisionDetected=False):
        self.rect.move_ip(-self.speed, 0)

        # Reset position of enemy at other end of the screen
        if self.rect.left <= 0 or collisionDetected:
            self.rect.left = 800
            self.rect.top = random.randint(50, 350)

    def speedUp(self):
        if self.speed < 26:
            self.speed += 2


class Bullet(spritebody.OtherSprite):
    SPEED = 10
    BULLET_IMAGE = pygame.image.load("./ShooterDemo/GUI/bullet.png")
    BULLET_IMAGE = pygame.transform.scale(BULLET_IMAGE, (20, 10))

    def __init__(self, init_x=0, init_y=0):
        super().__init__(init_x, init_y, speed=Bullet.SPEED, img=Bullet.BULLET_IMAGE)

    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.right > 800:
            self.kill()

    @staticmethod
    def speedUp():
        if Bullet.SPEED < 15:
            Bullet.SPEED += 1


class ShooterGUI:
    # Initialize the 'pygame' module
    pygame.init()

    # GAME WINDOW INVARIABLES
    # - - - - - - - - - - - - - -
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 400
    WINDOW_BACKGROUND = pygame.image.load("./ShooterDemo/GUI/bg.png")
    
    # PLAYER VARIABLES
    # - - - - - - - - - - - - - -
    PLAYER_SCORE = 0

    def __init__(self):
        self.game_window = pygame.display.set_mode((800, 400),
                                                   display=0)

        # Create the player; the player img is generated at position (30, 400)
        p_initial_x = 30
        p_initial_y = ShooterGUI.WINDOW_HEIGHT / 2
        self.player = Shooter(surf_w=10, surf_h=20, init_x=p_initial_x,
                              init_y=p_initial_y, speed=8)

        # Create the enemy
        e_initial_x = 770
        e_initial_y = ShooterGUI.WINDOW_HEIGHT / 2
        self.enemy = Enemy(init_x=e_initial_x, init_y=e_initial_y, speed=9)

        # Sprite Groups
        self.bullets = pygame.sprite.Group()

        # GAME LOOP
        running = True
        while running:
            # Event Handler
            for event in pygame.event.get():
                # Quit game
                if event.type == pygame.QUIT:
                    running = False

                # Execute if the 'Player' is shooting
                if event.type == pygame.KEYDOWN:
                    if event.key == 32:  # Check if the "space bar" was pressed
                        bullet = self.player.shoot()
                        self.bullets.add(bullet)

            # Get the keys that were pressed
            pressed_keys = pygame.key.get_pressed()

            # Update sprite locations, and draw sprites
            self.player.update(pressed_keys, ShooterGUI.WINDOW_WIDTH,
                               ShooterGUI.WINDOW_HEIGHT)

            # Check if 'enemy' got hit by any bullets; dispose of the bullet
            usedBullet = pygame.sprite.spritecollideany(self.enemy, self.bullets)
            if usedBullet is not None:
                self.enemy.update(collisionDetected=True)

                # Increase PLAYER_SCORE
                ShooterGUI.PLAYER_SCORE += 1
                print(ShooterGUI.PLAYER_SCORE)

                # Increase the speed of 'Enemy' every 10 points
                if ShooterGUI.PLAYER_SCORE % 10 == 0:
                    self.enemy.speedUp()
                    Bullet.speedUp()

                    print(f"SPEED UP: {self.enemy.speed}")

            else:
                self.enemy.update()

            # Draw background
            self.game_window.blit(ShooterGUI.WINDOW_BACKGROUND, (0, 0))

            # Draw sprites on 'game_window'
            for bullet in self.bullets:
                bullet.update()
          
                self.game_window.blit(bullet.surface, bullet.rect)

            # Update the score
            self.game_window.blit(self.player.surface, self.player.rect)
            self.game_window.blit(self.enemy.surface, self.enemy.rect)

            # Display the score on the screen
            self.game_window.blit(ShooterGUI.get_score_text(ShooterGUI.PLAYER_SCORE)
                                  , (700, 10))

            # Update the frame
            pygame.display.flip()

    @staticmethod
    def get_score_text(score=0):
        text_color = (255, 255, 255)

        img = pygame.font.SysFont(None, 30).render(f"Score:{score}",
                                                   True, text_color)
        return img


shooterGUI = ShooterGUI()