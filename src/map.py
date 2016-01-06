import re

import pygame

import util
import render
import camera

DEF_PATTERN = re.compile(r"^!def (\^?)(\S): ([a-z_-]+)\((\d+), ?(\d+)\)$")
TYPE_PATTERN = re.compile(r"^type: ([a-z]+)")

TILE_SIZE = 16

map = []

def load_map(name):
    file = util.read("{}{}_info.txt".format(util.MAPS_FOLDER, name))
    tiles = {}
    for line in file:

        if line.startswith("#"):
            continue

        # Define keyword
        # Defines a map char to a tile coordinate on the sprite sheet,
        # and determines whether to collide or not
        def_match = re.match(DEF_PATTERN, line)

        if def_match:
            clip = def_match.group(1) != "^"
            char = def_match.group(2)
            sheet = def_match.group(3)
            sheet_x = int(def_match.group(4))
            sheet_y = int(def_match.group(5))

            rect = pygame.Rect(sheet_x * TILE_SIZE, sheet_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            tiles[char] = util.get_sheet("tile\\{}.png".format(sheet)).get_image(rect)

    for i in range(3):
        text_map = util.read("{}{}_map_layer{}.txt".format(util.MAPS_FOLDER, name, i))
        map_surface = pygame.Surface((len(text_map[0]) * TILE_SIZE, len(text_map) * TILE_SIZE))
        map_surface.fill((0, 0, 255))
        map_surface.set_colorkey((0, 0, 255), pygame.RLEACCEL)

        x = y = 0
        for line in text_map:
            for char in line:
                if char != " ":
                    map_surface.blit(tiles[char], (x, y))
                x += TILE_SIZE
            y += TILE_SIZE
            x = 0
        map.append(Map(i == 1, map_surface))

def width():
    return map[0].rect.width

def height():
    return map[0].rect.height



class Map(pygame.sprite.DirtySprite):
    def __init__(self, clip, surface):
        pygame.sprite.DirtySprite.__init__(self)
        self.clip = clip
        self.image = surface
        self.mask = pygame.mask.from_surface(surface)
        self.rect = pygame.Rect(0, 0, surface.get_width(), surface.get_height())

    def draw(self, screen):
        screen.blit(self.image, camera.apply(self.rect))
