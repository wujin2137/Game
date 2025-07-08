import pygame

from game import Game

if __name__ == "__main__":
    game = Game()
    try:
        game.run()
    finally:
        pygame.mixer.quit()