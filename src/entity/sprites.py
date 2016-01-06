import pygame
from pygame.sprite import DirtySprite

import camera
import render
import util
from gui import examine
from map import map
from util import Vector

WALK_SPEED = 2
SPRINT_MULT = 1.5
JUMP_HEIGHT = 6
GRAVITY = 0.4


class Sprite(DirtySprite):
    """
    Base sprite class
    """

    def __init__(self, pixel_position=(0, 0)):
        DirtySprite.__init__(self)
        self.x = pixel_position[0]
        self.y = pixel_position[1]
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.rect.center = pixel_position
        self.clip = 1

        self.animated = False
        self.image = None
        self.current_texture = None
        self.animations = {}
        self.images = {}

        self.texture_folder = ""

        self.examine = ""

        self.is_particle = False

        self.visible = True

    def set_pixel_position(self, position):
        """
        Set the position of the sprite's center

        :param position:
        :return:
        """
        self.rect.center = position

    def next_frame(self):
        """
        Change the sprite to it's next frame if it's animated

        :return:
        """
        if self.animated:
            self.image = self.strips.next()

    def create_animation(self, sheet_file, position, frames=8, loop=True):
        """
        Set the animation information about the sprite

        :param sheet_file:
        :param position:
        :param frames:
        :param loop:
        :return:
        """
        try:
            sheet = util.get_sheet(sheet_file)
            self.strips = util.SheetAnimation(sheet, position, frames, loop)
            self.image = self.strips.next()
            self.rect.size = self.image.get_rect().width - 1, self.image.get_rect().height - 1
            self.animated = True
            return self.strips
        except:
            print("Failed to load animation at {0} in {1}".format(position, sheet_file))
            raise

    def add_animation(self, animation, position, frames=8, loop=True, fpi=4):
        if not animation in self.animations.keys():
            self.animations[animation] = self.create_animation("{0}{1}.png".format(self.texture_folder, animation),
                                                               position, frames, loop)
            self.animations[animation].set_fpi(fpi)

    def set_animation(self, animation):
        if self.current_texture is not animation and animation in self.animations.keys():
            self.strips = self.animations[animation]
            self.image = self.strips.next()
            self.current_texture = animation
            self.rect.size = self.image.get_rect().width - 1, self.image.get_rect().height - 1

    # def set_unique(self, path):
    #     self.image = util.load_alpha_image(path)
    #     self.rect = pygame.Rect(self.image.get_rect())
    #     self.src_image = self.image

    def create_sheet_image(self, sheet_file, pos):
        """
        Set the sprite image to one from a sprite sheet

        :param sheet_file:
        :param pos:
        :return:
        """
        self.image = util.get_sheet(sheet_file).get_image(pos)
        _, _, self.rect[2], self.rect[3] = pygame.Rect(self.image.get_rect())
        self.src_image = self.image
        self.rect.size = self.image.get_rect().width - 1, self.image.get_rect().height - 1
        return self.image

    def add_sheet_image(self, image, sheet_file, position):
        if not image in self.images.keys():
            self.images[image] = self.create_sheet_image(sheet_file, position)

    def set_image(self, image):
        if self.current_texture is not image:
            self.image = self.images[image]
            self.current_texture = image
            self.rect.size = self.image.get_rect().width - 1, self.image.get_rect().height - 1

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, self.rect)

    def kill(self):
        pass


class GameSprite(Sprite):
    def __init__(self, position):
        Sprite.__init__(self, position)
        render.add_game_sprites(self)
        examine.add_game_object(self)

        self.velocity = Vector(0, 0)
        self.grounded = False

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, camera.apply(self.rect))

    def kill(self):
        render.remove_game_sprites(self)
        examine.remove_game_object(self)

    def gravity_acceleration(self):
        return GRAVITY

    def update(self):
        if not self.grounded:
            self.velocity.y += self.gravity_acceleration()
            if self.velocity.y > 100:
                self.velocity.y = 100

        if self.velocity.y != 0:
            self.grounded = False
            self.set_animation("jump")

        self.collideX()
        self.collideY()

    def collideX(self):
        next_rect = self.rect.move(self.velocity.x, 0)

        while self.test_edge(next_rect.topleft, next_rect.midleft, next_rect.bottomleft):
            next_rect = next_rect.move(1, 0)
            self.velocity.x = 0

        while self.test_edge(next_rect.topright, next_rect.midright, next_rect.bottomright):
            next_rect = next_rect.move(-1, 0)
            self.velocity.x = 0

        self.rect = next_rect

    def collideY(self):
        next_rect = self.rect.move(0, self.velocity.y)

        while self.test_edge(next_rect.bottomleft, next_rect.midbottom, next_rect.bottomright):
            # bottom points collided. try to move up
            next_rect = next_rect.move(0, -1)
            self.velocity.y = 0
            self.grounded = True

        while self.test_edge(next_rect.topleft, next_rect.midtop, next_rect.topright):
            next_rect = next_rect.move(0, 1)
            self.velocity.y = 0

        self.rect = next_rect

        # check for floor
        test_rect = self.rect.move(0, 1)
        if not self.test_edge(test_rect.bottomleft, test_rect.midbottom, test_rect.bottomright):
            self.grounded = False
            if hasattr(self, "jumps") and self.jumps == 0:
                self.jumps = 1

    def test_edge(self, *points):
        return any(p for p in points if map[1].mask.get_at(p))


class ScreenSprite(Sprite):
    def __init__(self, position):
        Sprite.__init__(self, position)
        render.add_screen_sprites(self)
        examine.add_screen_object(self)

    def kill(self):
        render.remove_screen_sprites(self)
        examine.remove_screen_object(self)
