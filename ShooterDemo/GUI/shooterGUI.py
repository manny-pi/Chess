import pygame
import pygame.mixer
import pygame.time as ptime
from pygame.locals import *
from _SpriteBodies.spritebodies import OtherSprite, EnemySprite, PlayerSprite
from random import randint as r


class Shooter(PlayerSprite):
    SHOOTER_IMAGE = pygame.image.load("./ShooterDemo/images/shooter.png")
    SHOOTER_IMAGE = pygame.transform.scale(SHOOTER_IMAGE, (60, 60))

    def __init__(self, surf_w, surf_h, init_x=0, init_y=0, speed=5):
        super().__init__(surf_w, surf_h, init_x, init_y, speed, img=Shooter.SHOOTER_IMAGE)

    def update(self, pressed_keys, window_width,
               window_height):

        # Move Shooter up
        if pressed_keys[K_w]:
            if self.rect.top - self.speed >= 0:
                self.rect.move_ip(0, -self.speed)

        # Move Shooter down
        if pressed_keys[K_s]:
            if self.rect.bottom + self.speed <= window_height:
                self.rect.move_ip(0, self.speed)

    # Create a Bullet object that initially appears at the same location as Shooter 
    def shoot(self):
        b_init_x = self.rect.left
        b_init_y = self.rect.top + 20
        return Bullet(init_x=b_init_x + 20, init_y=b_init_y)


class Enemy(EnemySprite):
    ENEMY_IMAGE = pygame.image.load("./ShooterDemo/images/enemy.png")
    ENEMY_IMAGE = pygame.transform.scale(ENEMY_IMAGE, (60, 20))
    SPEED = 5

    def __init__(self, init_x=0, init_y=0):
        super().__init__(init_x, init_y, speed=Enemy.SPEED, img=Enemy.ENEMY_IMAGE)

    def update(self):
        self.rect.move_ip(-self.speed, 0)

    @classmethod
    def speedUp(cls):
        if cls.SPEED <= 20:
            cls.SPEED += 3


class Bullet(OtherSprite):
    SPEED = 10
    BULLET_IMAGE = pygame.image.load("./ShooterDemo/images/bullet.png")
    BULLET_IMAGE = pygame.transform.scale(BULLET_IMAGE, (20, 10))

    def __init__(self, init_x=0, init_y=0):
        super().__init__(init_x, init_y, speed=Bullet.SPEED, img=Bullet.BULLET_IMAGE)

    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.right > 800:
            self.kill()


class ShooterGUI:
    # Initialize the 'pygame' module
    pygame.init()

    # Initialize the 'pygame.mixer' module
    pygame.mixer.init()

    # GAME WINDOW INVARIABLES
    # - - - - - - - - - - - - - - - - - -
    # GAME WINDOW 
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 400
    WINDOW_BACKGROUND = pygame.image.load("./ShooterDemo/images/background.png")

    ENEMIES_LIMIT = 10
    LEVEL = 0

    # GAME AUDIO 
    filename = "./ShooterDemo/audio/shooteraudio.ogg"
    SHOOTER_SOUND = pygame.mixer.Sound(filename)

    # SHOOTER VARIABLES
    # - - - - - - - - - - - - - - - - - -
    PLAYER_SCORE = 0

    def __init__(self):
        # Create the game window 
        self.game_window = pygame.display.set_mode((800, 400), display=0)

        # Create the game sprites 
        # - - - - - - - - - - - - - - - - - - 
        # Create the Shooter; the Shooter img is generated at position (0, 0), top-left of the game window
        p_initial_x = 0
        p_initial_y = 0
        self.player = Shooter(surf_w=10, surf_h=20, init_x=p_initial_x,
                              init_y=p_initial_y, speed=7)

        # Create the Enemy group; the group will contain all the Enemy sprites generated 
        self.enemies = pygame.sprite.Group()

        # Create a Sprite group to hold all the Bullet sprites 
        self.bullets = pygame.sprite.Group()

        # User Events
        # - - - - - - - - - - - - - - - - - -
        # Event to generate Enemy / Generate Enemy every 4 seconds
        self.timeToEnemy = 4000
        self.generateEnemy = pygame.event.Event(pygame.USEREVENT)
        ptime.set_timer(self.generateEnemy.type, self.timeToEnemy)

        # Event for next level / Generate next level prompt every 30 seconds
        self.timeToNextLevel = 30000
        self.nextLevel = pygame.event.Event(pygame.USEREVENT + 1)
        ptime.set_timer(self.nextLevel.type, self.timeToNextLevel)
        self.displayNextLevelPrompt = False

        # GAME LOOP
        # - - - - - - - - - - - - - - - - - -
        running = True
        while running:

            # Event Handling
            # - - - - - - - - - - - - - - - - - -
            for event in pygame.event.get():

                # QUIT GAME 
                if event.type == pygame.QUIT:
                    running = False

                # Execute if the user pressed a key on the keyboard
                if event.type == pygame.KEYDOWN:

                    # Execute if the "space bar" was pressed; add bullets to group of bullets fired
                    # REVIEW: Try using constant at condition: 
                    if event.key == K_SPACE:
                        # Create a Bullet object; add it to the group of bullets
                        bullet = self.player.shoot()
                        self.bullets.add(bullet)

                        # Play audio for shooting
                        # ShooterGUI.SHOOTER_SOUND.play()

                # Execute if the event is generate Enemy
                if event.type == pygame.USEREVENT:
                    enemy = Enemy(ShooterGUI.WINDOW_WIDTH, r(10, ShooterGUI.WINDOW_HEIGHT - 10))
                    self.enemies.add(enemy)

                # Execute if the event is move on to the next level
                if event.type == pygame.USEREVENT + 1:
                    self.next_level_prompt(1)

                    self.displayNextLevelPrompt = True
                else:
                    self.displayNextLevelPrompt = False

            # Update Sprite locations / Handle Sprite collisions / Update player score
            # - - - - - - - - - - - - - - - - - -
            # Returns the state of all the keys in the keyboard in array; use to update Shooter sprite location
            pressed_keys = pygame.key.get_pressed()

            # Update Shooter sprite location, and draw Shooter sprite
            self.player.update(pressed_keys, ShooterGUI.WINDOW_WIDTH, ShooterGUI.WINDOW_HEIGHT)

            # Remove Bullet and Enemy sprites that collide with each other from their sprite groups
            bullets_and_enemies = pygame.sprite.groupcollide(self.bullets, self.enemies,
                                                             dokilla=True, dokillb=True)

            # Update the player score
            # * * NOTE: Need to make a more sensible method for increasing the score
            if len(bullets_and_enemies) != 0:
                ShooterGUI.PLAYER_SCORE += 1

            # Increase the speed of the enemies
            if self.PLAYER_SCORE % 10 == 0 and self.PLAYER_SCORE != 0:
                Enemy.SPEED += 2

                # Draw graphics to the window
            # - - - - - - - - - - - - - - - - - -
            self.render_screen()

        # Close pygame
        pygame.quit()

    def render_screen(self):
        # Draw background
        self.game_window.blit(ShooterGUI.WINDOW_BACKGROUND, (0, 0))

        # Draw the Shooter sprite on the game window
        self.game_window.blit(self.player.surface, self.player.rect)

        # Draw Bullet sprites on the game window
        for bullet in self.bullets:
            bullet.update()
            self.game_window.blit(bullet.surface, bullet.rect)

        # Draw the Enemy sprites on the game window
        for enemy in self.enemies:
            enemy.update()
            self.game_window.blit(enemy.surface, enemy.rect)

        # Display the player score on the screen
        scoreText = ShooterGUI.get_score_text(ShooterGUI.PLAYER_SCORE)
        self.game_window.blit(scoreText, (700, 10))

        # Display the next level prompt on the screen
        if self.displayNextLevelPrompt is True:
            nextLevelText = self.next_level_prompt(level=1)
            self.game_window.blit(nextLevelText, (50, 50))

        # Update the frame
        pygame.display.flip()

        if self.displayNextLevelPrompt is True:
            ptime.delay(5000)

    def get_score_text(self, score=0):
        """Returns a Surface with the game score"""
        text_color = (255, 255, 255)

        img = pygame.font.SysFont(None, 30).render(f"KILLS: {score}",
                                                   True, text_color)
        return img

    def next_level_prompt(self, level):
        # Create the Surface for the next level prompt
        text_color = (255, 255, 255)
        img = pygame.font.SysFont(None, 100).render(f"LEVEL: {level}",
                                                    True, text_color)
        return img

    @staticmethod
    def life(livesLeft):
        pass


shooterGUI = ShooterGUI()
