import random

import pygame
import math

import util
from entity import particle
from entity.sprites import GameSprite, GRAVITY
from map import map

GUN_FOLDER = util.SPRITES_FOLDER + "gun\\"


class Gun(GameSprite):
    def __init__(self, position):
        GameSprite.__init__(self, position)

        self.pieces = ""

        self.stitch_image(self.random_part_image("grip"), self.random_part_image("magazine"),
                          self.random_part_image("barrel"))

        self.rect = pygame.Rect(position, self.image.get_size())

        self.flipped = False

        self.examine = self.pieces

        self.speed = random.randint(1, 12)

        self.examine = self.examine + " - " + str(self.speed)

        self.recoil = 0
        self.recoil_step = self.speed

    def update(self):
        pass

    def generate_stats(self, level):
        pass

    def random_part_image(self, part):
        i = random.randint(1, 8)
        g = random.randint(1, 100)
        if g > 99:
            i = 9
        self.pieces = self.pieces + str(i)

        return util.load_alpha_image("{}\\{}\\{}.png".format(GUN_FOLDER, part, i))

    def stitch_image(self, grip_image, mag_image, barrel_image):
        width = grip_image.get_width() + mag_image.get_width() + barrel_image.get_width()
        height = 12

        self.image = pygame.Surface((width, height)).convert()
        self.image.fill((0, 0, 255))
        self.image.set_colorkey((0, 0, 255), pygame.RLEACCEL)

        self.image.blit(grip_image, (0, 0))
        self.image.blit(mag_image, (grip_image.get_width(), 0))
        self.image.blit(barrel_image, (grip_image.get_width() + mag_image.get_width(), 0))

        self.grip_point = grip_image.get_width()

    def shoot(self):
        if self.flipped:
            Bullet(self, self.rect.midleft, -1, particle.get_texture("bullet"))

        else:
            Bullet(self, self.rect.midright, 1, particle.get_texture("bullet"))

    def recover_recoil(self):
        if self.recoil_step <= 0:
            self.recoil = 0
            self.recoil_step = self.speed
        self.recoil_step -= 1


class Bullet(particle.Particle):
    def __init__(self, gun, position, dir, texture):
        particle.Particle.__init__(self, position, texture)
        self.gun = gun
        self.dir = dir
        self.velocity = util.Vector(self.dir * self.gun.speed, 0)
        self.texture = pygame.transform.scale(texture, (int(math.sqrt(self.gun.speed) * 5), 1))

    def update(self):
        self.velocity.y += GRAVITY / 100.0
        self.rect = self.rect.move(self.velocity.tup)
        return particle.Particle.update(self)

    def collide_map(self):
        if self.dir == 1:
            col = map[1].mask.get_at(self.rect.midright)
        else:
            col = map[1].mask.get_at(self.rect.midleft)
        if col:
            # self.undo_update()
            particle.animated_effect("hit", self.rect.topleft if self.dir == -1 else self.rect.topright)
        return col

    def collide_sprite(self, sprite):
        # cases to quickly return false to speed up collision checking
        if sprite.rect.top > self.rect.top or sprite.rect.bottom < self.rect.bottom:
            return False

        if dir == 1:
            if sprite.rect.left > self.rect.right:
                return False
        elif dir == -1:
            if sprite.rect.right < sprite.rect.left:
                return False

        col = pygame.sprite.collide_rect(self, sprite)
        if col:
            particle.animated_effect("hit", self.rect.topleft if self.dir == -1 else self.rect.topright)
        return col
