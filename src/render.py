import pygame
import options
from pygame.locals import FULLSCREEN, RESIZABLE
from map import map

screen = None
game_screen = None

# sprites rendered on the screen and not in
# the game world
screen_sprites = []

# sprites rendered in the game world that need
# camera translations
game_sprites = []


def init():
    try:
        flags = 0
        if options.fullscreen():
            flags |= FULLSCREEN
        flags |= RESIZABLE
        global screen
        screen = pygame.display.set_mode(options.dimensions(), flags)

        global game_screen
        game_screen = pygame.Surface(options.game_dimensions())

        pygame.mouse.set_visible(False)
        pygame.display.update()

    except pygame.error as msg:
        raise pygame.error("Failed to initialize render engine {0}".format(str(msg)))


def add_screen_sprites(*sprites):
    for sprite in sprites:
        screen_sprites.append(sprite)


def remove_screen_sprites(*sprites):
    for sprite in sprites:
        screen_sprites.remove(sprite)


def add_game_sprites(*sprites):
    for sprite in sprites:
        game_sprites.append(sprite)


def remove_game_sprites(*sprites):
    for sprite in sprites:
        game_sprites.remove(sprite)


def update_fullscreen():
    pygame.display.set_mode(screen.get_size(), FULLSCREEN if options.fullscreen() else 0)


def draw():
    game_screen.fill((200, 200, 220))

    for map_part in map:
        map_part.draw(game_screen)

    for sprite in game_sprites:
        if sprite.is_particle:
            if hasattr(sprite, "collide"):
                if sprite.collide_map() \
                        or any(sprite.collide(s) for s in game_sprites):
                    remove_game_sprites(sprite)

        if hasattr(sprite, "update"):
            sprite.update()
        sprite.draw(game_screen)

    for sprite in screen_sprites:
        sprite.draw(game_screen)

    screen.blit(pygame.transform.scale(game_screen, options.dimensions()), (0, 0))

    pygame.display.update()