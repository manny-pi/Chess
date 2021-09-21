import _SpriteBodies.spritebodies as spritebody
import pygame
import pygame.mixer 
from pygame.locals import * 
import random


class Shooter(spritebody.PlayerSprite):
    SHOOTER_IMAGE = pygame.image.load("./ShooterDemo/images/shooter.png")
    SHOOTER_IMAGE = pygame.transform.scale(SHOOTER_IMAGE, (60, 60))

    def __init__(self, surf_w, surf_h, init_x=0, init_y=0, speed=40):
        super().__init__(surf_w, surf_h, init_x, init_y, speed, img=Shooter.SHOOTER_IMAGE) 

    def update(self, pressed_keys, window_width,
               window_height):
        
        # Move Shooter up
        if pressed_keys[K_w]:
            if self.rect.top - self.speed >= 20:
                self.rect.move_ip(0, -self.speed)

        # Move Shooter down
        if pressed_keys[K_s]:
            if self.rect.bottom + self.speed <= window_height - 20:
                self.rect.move_ip(0, self.speed)

    # Create a Bullet object that initially appears at the same location as Shooter 
    def shoot(self):
        b_init_x = self.rect.left
        b_init_y = self.rect.top + 20
        return Bullet(init_x=b_init_x, init_y=b_init_y)


class Enemy(spritebody.EnemySprite):
    ENEMY_IMAGE = pygame.image.load("./ShooterDemo/images/enemy.png")
    ENEMY_IMAGE = pygame.transform.scale(ENEMY_IMAGE, (60, 20))

    def __init__(self, init_x=0, init_y=0, speed=8):
        super().__init__(init_x, init_y, speed, img=Enemy.ENEMY_IMAGE)

    def update(self):
        self.rect.move_ip(-self.speed, 0)

    def speedUp(self):
        if self.speed < 26:
            self.speed += 2


class Bullet(spritebody.OtherSprite):
    SPEED = 10
    BULLET_IMAGE = pygame.image.load("./ShooterDemo/images/bullet.png")
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

    # Initalize the 'pygame.mixer' module 
    pygame.mixer.init() 


    # GAME WINDOW INVARIABLES
    # - - - - - - - - - - - - - - - - - -
    # GAME WINDOW 
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 400
    WINDOW_BACKGROUND = pygame.image.load("./ShooterDemo/images/background.png")
    
    # GAME AUDIO 
    filename = "./ShooterDemo/audio/shooteraudio.ogg"
    SHOOTER_SOUND = pygame.mixer.Sound(filename)

    # SHOOTER VARIABLES
    # - - - - - - - - - - - - - - - - - -
    PLAYER_SCORE = 0
    LEVEL = 0 
    

    def __init__(self):
        self.game_window = pygame.display.set_mode((800, 400), display=0)

        # Create the game sprites 
        # - - - - - - - - - - - - - - - - - - 
        # Create the Shooter; the Shooter img is generated at position (0, 0), top-left of the game window
        p_initial_x = 0
        p_initial_y = 0
        self.player = Shooter(surf_w=10, surf_h=20, init_x=p_initial_x, init_y=p_initial_y, speed=15)

        # Create the Enemy group; the group will contain all the Enemy sprites generated 
        self.enemies = pygame.sprite.Group() 

        # Create a Sprite group to hold all the Bullet sprites 
        self.bullets = pygame.sprite.Group()


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


                        enemy = Enemy(800, random.randint(0, 400))
                        self.enemies.add(enemy)

                        # Play audio for shooting
                        # REVIEW: Not working :( 
                        ShooterGUI.SHOOTER_SOUND.play() 
                        # print("Audio played")
                        

            # Update Sprite locations / Handle Sprite collisions / Update player score
            # - - - - - - - - - - - - - - - - - -
            # Returns the state of all the keys in the keyboard in array; use to update Shooter sprite location
            pressed_keys = pygame.key.get_pressed()

            # Update Shooter sprite location, and draw Shooter sprite
            self.player.update(pressed_keys, ShooterGUI.WINDOW_WIDTH, ShooterGUI.WINDOW_HEIGHT)

            # Remove sprites that collide from their groups
            bullets_and_enemies = pygame.sprite.groupcollide(self.bullets, self.enemies, dokilla=True, dokillb=True)

            # Update the player score; Change the mechanism 
            if len(bullets_and_enemies) != 0: 
              ShooterGUI.PLAYER_SCORE += 1
              

            # Draw graphics to the window 
            # - - - - - - - - - - - - - - - - - -
            # Draw background
            self.game_window.blit(ShooterGUI.WINDOW_BACKGROUND, (0, 0))

            # Draw Bullet sprites on the game window
            for bullet in self.bullets:
                bullet.update()
          
                self.game_window.blit(bullet.surface, bullet.rect)

            # Draw the Enemy sprites on the game window 
            for enemy in self.enemies: 
              enemy.update() 
              self.game_window.blit(enemy.surface, enemy.rect)

            # Update the score
            self.game_window.blit(self.player.surface, self.player.rect)
            # self.game_window.blit(self.enemy.surface, self.enemy.rect)
        

            # Display the score on the screen
            self.game_window.blit(ShooterGUI.get_score_text(ShooterGUI.PLAYER_SCORE)
                                  , (700, 10))

            # Update the frame
            pygame.display.flip()

    @staticmethod
    def get_score_text(score=0):
        text_color = (255, 255, 255)

        img = pygame.font.SysFont(None, 30).render(f"KILLS: {score}",
                                                   True, text_color)
        return img

    @staticmethod
    def next_level_prompt(leve): 
        text_color = (255, 255, 255)

        img = pygame.font.SysFont(None, 100).render(f"Level: {leve}", 
                                                    True, text_color)

        return img

shooterGUI = ShooterGUI()