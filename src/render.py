import pygame
import options
from pygame.locals import FULLSCREEN
from map import map

# screen to render on the window directly
screen = None

# game_screen to render ONTO screen with
# scaling set in options
game_screen = None

# sprites rendered on the screen and not in
# the game world
screen_sprites = []

# sprites rendered in the game world that need
# camera translations
game_sprites = []


def init():
    """Initialise the screen and game screen, and set default options.
    """
    try:
        flags = 0
        if options.fullscreen():
            flags |= FULLSCREEN
        # flags |= RESIZABLE

        # initialise the screen
        global screen
        screen = pygame.display.set_mode(options.dimensions(), flags)

        # initialise the game_screen
        global game_screen
        game_screen = pygame.Surface(options.game_dimensions())

        pygame.mouse.set_visible(False)
        pygame.display.update()

    except pygame.error as msg:
        raise pygame.error("Failed to initialize render engine {0}".format(str(msg)))


def add_screen_sprites(*sprites):
    """Add 1 or more sprites to the screen sprites list.

    :param sprites: 1 or more screen sprites
    """
    for sprite in sprites:
        screen_sprites.append(sprite)


def remove_screen_sprites(*sprites):
    """Remove 1 or more sprites to the screen sprites list.

    :param sprites: 1 or more screen sprites
    """
    for sprite in sprites:
        screen_sprites.remove(sprite)


def add_game_sprites(*sprites):
    """Add 1 or more sprites to the game sprites list.

    :param sprites: 1 or more game sprites
    """
    for sprite in sprites:
        game_sprites.append(sprite)


def remove_game_sprites(*sprites):
    """Remove 1 or more sprites to the game sprites list.

    :param sprites: 1 or more game sprites
    """
    for sprite in sprites:
        game_sprites.remove(sprite)


def update_fullscreen():
    """Update the fullscreen flag to align with the options.
    """
    pygame.display.set_mode(screen.get_size(), FULLSCREEN if options.fullscreen() else 0)


def draw():
    """Frame drawing function.

    Wipes the screen, blits all game sprites then screen sprites
    (and calling update on them), then scales the screen and updates
    the main display.
    """

    # wipe game screen
    # to be replaced with background drawing
    game_screen.fill((0, 0, 0))

    # draw each map layer
    for map_layer in map:
        map_layer.draw(game_screen)

    # update and draw each game sprite
    for sprite in game_sprites:
        if sprite.is_particle:
            # check collision on only certain particles
            # i.e. projectiles
            if hasattr(sprite, "collide_sprite"):
                if sprite.collide_map() \
                        or any(sprite.collide_sprite(s) for s in game_sprites):
                    # the particle will then be removed and freed
                    remove_game_sprites(sprite)

        # update all sprites, then draw
        sprite.update()
        sprite.draw(game_screen)

    # update and draw each screen sprite
    # these are rendered after all game sprites because
    # they need to always show over other sprites.
    for sprite in screen_sprites:
        sprite.update()
        sprite.draw(game_screen)

    # blit the low-res screen onto the main screen and scale it
    screen.blit(pygame.transform.scale(game_screen, options.dimensions()), (0, 0))

    # update the display
    pygame.display.update()
