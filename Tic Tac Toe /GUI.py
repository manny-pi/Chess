import pygame


class TicTacToe:
    def __init__(self):
        # Initialize the pygame module
        pygame.init()

        # Background
        self.__BACKGROUND = pygame.image.load("bg.jpeg")

        # Symbols
        self.__X = pygame.image.load("x.png")
        self.__O = pygame.image.load("o.jpg")

        # Set the game window
        self.__HEIGHT = 300
        self.__WIDTH = 300
        self.__GAME_WINDOW = pygame.display.set_mode((self.__WIDTH, self.__HEIGHT))

        # Determine whether to show "x" or "o" when the user presses the button
        controller = 1

        running = True
        while running:

            for event in pygame.event.get():
                # END GAME
                if event.type == pygame.QUIT:
                    running = False

                # Check if the user clicked the mouse
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # - - draw x or o  - - #
                    mousePos = pygame.mouse.get_pos()
                    

                    # Change the symbol for the next move
                    if controller == 1:
                        controller = 0
                    else:
                        controller = 1


            # Draw the game background
            self.__GAME_WINDOW.blit(self.__BACKGROUND, (0, 0))
            # Update the game window
            pygame.display.flip()


def main():
    game = TicTacToe()


main()
