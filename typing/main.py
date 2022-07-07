import pygame
from pygame.sprite import Sprite 
from pygame import Surface
from pygame.font import SysFont
from pygame import transform 
from pygame.time import Clock 
from random import randint

pygame.init()


class Letter(Sprite):
    
    def __init__(self, l: str): 
        super().__init__() 

        self.delta = 10
        self.letter = l 
        self.surf = SysFont('Arial', 70).render(l, True, (100, 150, 200))
        self.rect = self.surf.get_rect(bottomleft=(randint(0, 630), 0)) 

    def moveDown(self):
        if self.rect.bottom < 700:
            self.rect.move_ip(0, 10)


class Game:

    def __init__(self):
        self.letters = [] 
        self.window = pygame.display.set_mode((800, 800)) 
        self.clock = Clock()
        self.frame_rate = 15
        self.player_score = 0

        self.ASCII = [] 
        # for i in range(65, 91): self.ASCII.append(i) 
        for i in range(97, 123): self.ASCII.append(i)

        self.ADD_LETTER = pygame.USEREVENT + 1 

        self.letterSpeed = 500
        pygame.time.set_timer(self.ADD_LETTER, self.letterSpeed)
        
    def run(self): 
        running = True 
        while running: 
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    running = False 
            
                elif event.type == pygame.KEYDOWN: 
                    if event.key in self.ASCII: 
                        l = chr(event.key)
                        self.remove(l)

                elif event.type == self.ADD_LETTER: 
                    self.generateLetter()


            self.window.fill((0, 0, 0))
            for letter in self.letters:
                letter.moveDown()
                self.window.blit(letter.surf, letter.rect)

            pygame.display.flip()
            self.clock.tick(self.frame_rate)
        
    def speedUp(self): 
        """
        Increase the speed of the game
        """
    
        self.letterSpeed -= 100
        pygame.time.set_timer(self.ADD_LETTER, self.letterSpeed)

    def generateLetter(self):
        """
        Add a letter to the list of letters
        """
        
        l = chr(self.ASCII[randint(0, len(self.ASCII)-1)])
        self.letters.append(Letter(l))

    def remove(self, l): 
        """
        Removes the letter from the letters array
        """

        i = 0
        while i < len(self.letters): 
            if self.letters[i].letter == l: 
                self.letters.pop(i)
                break 
            i += 1


Game().run()