import pygame
from pygame import mixer 
from pygame import time 

from pygame.font import SysFont
from random import randint as rint
from sprites import * 

from datetime import datetime

pygame.init() 

def thisSecond(): 
    second = int(datetime.now().ctime().split(" ")[3].split(":")[2])

    return second


def getScoreboard(kills=0):
    """ Returns a Surface with the game score """

    white = (255, 255, 255)
    img = SysFont(None, 30)
    img = img.render(f"KILLS: {kills}", True, white)
    
    return img


def getLevelPrompt(level):
    """ Returns a Surface with a prompt for the next level """ 

    white = (255, 255, 255)
    img = SysFont(None, 50)
    img = img.render(f"LEVEL: {level}", True, text_color)

    return img


def run():

    WINDOW_WIDTH  = 1200
    WINDOW_HEIGHT = 600
    GAME_WINDOW   = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), display=0)

    SCORE = 0

    spaceship = Spaceship()
    Spaceship.setBorders(0, WINDOW_HEIGHT) 

    aliens = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    timeToAlien = 2000
    generateAlien = pygame.event.Event(pygame.USEREVENT)
    time.set_timer(generateAlien.type, timeToAlien)

    scoreboard = getScoreboard() 

    running = True
    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == generateAlien.type: 
                alien = Alien(WINDOW_WIDTH, rint(0, WINDOW_HEIGHT))
                aliens.add(alien)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e or event.key == pygame.K_i or event.key == pygame.K_KP8: 
                    spaceship.moveUp() 
                
                if event.key == pygame.K_d or event.key == pygame.K_k or event.key == pygame.K_KP5:
                    spaceship.moveDown() 

                if event.key == pygame.K_SPACE:
                    bullet = spaceship.shoot()
                    bullets.add(bullet)

        # Get Bullets and Aliens that collide
        # - - - - - - - - - - - - - 
        collidedSprites = pygame.sprite.groupcollide(bullets, aliens, dokilla=True, dokillb=True)

        # Update the player score
        # - - - - - - - - - - - - - 
        for sprite in collidedSprites:
            SCORE += 1
            scoreboard = getScoreboard(kills=SCORE)

        # Draw Spaceship, Bullets, and Aliens
        # - - - - - - - - - - - - - 
        GAME_WINDOW.fill((100, 125, 75))

        GAME_WINDOW.blit(scoreboard, scoreboard.get_rect(right=WINDOW_WIDTH))

        GAME_WINDOW.blit(spaceship.image, spaceship.rect)

        for bullet in bullets:
            GAME_WINDOW.blit(bullet.image, bullet.rect)
            bullet.moveRight()

        for alien in aliens:
            GAME_WINDOW.blit(alien.image, alien.rect)
            alien.moveLeft()

        # Update the display
        pygame.display.flip() 

    pygame.quit()



if __name__ == '__main__': 
    run() 
