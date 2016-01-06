"""
Main driver class for Prototype

Handles UI/Menu states and initialises
the game.
"""

import pygame
import render


def main():
    # initialise pygame here so all modules
    # have instant access to pygame functions
    pygame.init()
    render.init()

    import game
    game.init()
    game.run()


if __name__ == "__main__":
    main()
