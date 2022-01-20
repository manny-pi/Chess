import pygame
import random

# Import the common actions that
from pygame.locals import (
    K_a,  # Arrow up
    K_d,  # Arrow down
    K_w,  # Arrow left
    K_s,  # Arrow right
    QUIT  # 'X' button on GUI interface
)

# GAME WINDOW DIMENSIONS
# - - - - - - - - -
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 400


# Sprite classes
# - - - - - - - - - - - -
# Player Sprite
class Player(pygame.sprite.Sprite):
    flashing_lights_count = 0

    def __init__(self, img=None):
        super(Player, self).__init__()

        # Define a surface to hold the 'player' sprite; width = height = 50
        self.surface = pygame.Surface((70, 20))
        self.image = img

        # Player sprite color
        __WHITE = (255, 255, 255)
        self.surface.fill(__WHITE)  # Fill the surface
        self.rect = self.surface.get_rect(topleft=(50, int(WINDOW_HEIGHT / 2)))  # Use to move 'player' sprite

        # The value by which the 'player' sprite is displaced for each action
        self.speed = 5

    def update(self, pressed_keys):
        """ Used to update the location of the 'player' sprite """

        # Execute if the player pressed the 'UP' arrow key
        if pressed_keys[K_w]:

            # Execute if we're not out of left bound
            if self.rect.top - self.speed >= 0:
                self.rect.move_ip(0, -self.speed)

        # Execute if the player pressed the 'DOWN' arrow key
        if pressed_keys[K_s]:

            # Execute if we're not out of bottom bound
            if self.rect.bottom + self.speed <= WINDOW_HEIGHT:
                self.rect.move_ip(0, self.speed)

        # Execute if the player pressed the 'LEFT' arrow key
        if pressed_keys[K_a]:

            # Execute if we're not out of the left bound
            if self.rect.left - self.speed >= 0:
                self.rect.move_ip(-self.speed, 0)

        # Execute if the player pressed the 'RIGHT' arrow key
        if pressed_keys[K_d]:

            # Execute if we're not out of the right bound
            if self.rect.right + self.speed <= WINDOW_WIDTH:
                self.rect.move_ip(self.speed, 0)

    def speed_up(self):
        if self.speed < 10:
            self.speed += 1

    def flashing_lights(self):
        self.surface.fill((random.randint(0, 255), random.randint(0, 255),
                           random.randint(0, 255)))
        if Player.flashing_lights_count < 100:
            Player.flashing_lights_count += 1
        else:
            Player.flashing_lights_count = 0


# Enemy Sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        # Create the 'Surface' object we'll draw on; (30x30)
        self.surface = pygame.Surface((30, 30))

        # Initialize the x, y coordinates of the 'Rect' we'll use to draw
        # the 'Enemy' sprite
        __init_x = random.randint(int(WINDOW_WIDTH * (2 / 3)), WINDOW_WIDTH)
        __init_y = random.randint(0, WINDOW_HEIGHT)

        self.rect = self.surface.get_rect(center=(__init_x, __init_y))
        self.surface.fill((255, 0, 0))

        # Set the speed at which the sprite moves
        self.speed = 6

    def update(self, collisionDetected=False):
        """ Returns 'True' when the player's life should be reduced """

        # Execute if 'Player' collided with 'Enemy'
        if collisionDetected:
            self.rect.left = WINDOW_WIDTH
            self.rect.top = random.randint(0, WINDOW_HEIGHT - 30)

        # Execute if 'Enemy' is about to move off screen
        elif self.rect.right - self.speed <= 0:
            self.rect.left = WINDOW_WIDTH
            self.rect.top = random.randint(0, WINDOW_HEIGHT)

            # Return True if the 'Enemy' made it to the end of the screen,
            # and now the player loses a life
            return True

        # General purpose motion of 'Enemy'; move the sprite leftward
        else:
            self.rect.move_ip(-self.speed, 0)

    def speed_up(self):
        if self.speed < 20:
            self.speed += 3


# GAME class
# - - - - - - - - - - - -
class Demo:
    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Setup the game window
        # -  -  -  -  -  -  -  -  -
        # 'display=1' sets the 'game_window' to open on the primary screen
        game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), display=0)

        # Setup the player sprite and data
        # -  -  -  -  -  -  -  -  -
        img = pygame.image.load("/Users/Omani/Desktop/Python/Python Projects/PyGame Projects/"
                                "Raindrops/Images/bg.png")
        self.player = Player(img=img)
        self.enemy = Enemy()

        # PLAYER SCORE
        PLAYER_SCORE = 0

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # LIFE METER [not the best implementation]
        life_color = (0, 255, 0)
        initial_life = '| | | | | | | | | | |'
        life_left_arr = initial_life.split(' ')
        life_left_img = pygame.font.SysFont(None, 30).render(initial_life, True, life_color)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        # Game Loop
        running = True
        while running:

            # Event Handler
            events = pygame.event.get()  # Retrieve events from the event queue
            for event in events:
                if event.type == QUIT:  # Execute if the player hits the EXIT button
                    running = False

            # Check if any keys were pressed; Update the game accordingly
            pressed_keys = pygame.key.get_pressed()
            self.player.update(pressed_keys)

            # Check if the 'player' collided with 'enemy'
            if pygame.sprite.collide_rect(self.player, self.enemy):
                self.enemy.update(collisionDetected=True)

                # Increase the player's score
                PLAYER_SCORE += 1

                if PLAYER_SCORE % 5 == 0:
                    self.enemy.speed_up()
                    self.player.speed_up()

            else:
                reduceLife = self.enemy.update()

                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                if reduceLife:
                    try:
                        life_left_arr.remove('|')
                        life_left_img = pygame.font.SysFont(None, 30). \
                            render(f"{' '.join(life_left_arr)}", True, life_color)
                    except ValueError:
                        GAME_OVER = pygame.font.SysFont(None, 50).render("GAME OVER", True, (255, 0, 0))
                        game_window.blit(GAME_OVER, (0, 0))

                        pygame.display.flip()
                        pygame.time.wait(30000)

                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

            # Fill 'game_window' background
            BLACK = (0, 0, 0)
            game_window.fill(BLACK)

            # Draw the 'Player' and 'Enemy' sprites on the 'game_window'
            game_window.blit(self.enemy.surface, self.enemy.rect)
            game_window.blit(self.player.surface, self.player.rect)

            # Draw the SCORE on 'game_window'
            game_window.blit(Demo.get_score_text(PLAYER_SCORE), (WINDOW_WIDTH - 100, 20))

            # Draw the LIFE LEFT on 'game_window'
            game_window.blit(life_left_img, (WINDOW_WIDTH - 150, 50))

            # Update the frame
            pygame.display.flip()

    @staticmethod
    def get_score_text(score=0):
        text_color = (255, 255, 255)

        img = pygame.font.SysFont(None, 30).render(f"Score:{score}",
                                                   True, text_color)
        return img


# Create the 'Runner' game object
demo = Demo()
