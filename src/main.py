"""
Main driver class for Prototype

Handles UI/Menu states and initialises
the game.
"""

import game


def main():
    # options = Options(save_file)
    game.init()
    game.run()


if __name__ == "__main__":
    main()
