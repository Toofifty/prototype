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


def test_edge(*points):
    """Test a list of points for a collision on the map.

    Use a list down one edge of a sprite to test if that side
    collides.

    :param points: list/tuple of points to check
    :return: True if any points collided with the map.
    """
    return any(p for p in points if map[1].mask.get_at(p))


class Sprite(DirtySprite):
    """Base sprite class.

    Handles position, image/animation loading,
    physics and movement of the sprite.

    Base class for everything drawn onto the
    screen.
    """

    def __init__(self, position=(0, 0)):
        DirtySprite.__init__(self)
        self.rect = pygame.Rect(position, (0, 0))

        # determines how the sprite clips
        # clip == 0: sprite does not clip with anything.
        # clip == 1: sprite can be walked past but will also
        #            be hit by projectiles
        # clip == 2: full block
        self.clip = 1

        # image to be drawn each frame
        # change with set_animation and set_image
        self.image = None

        # SheetAnimation instance that controls
        # the current animation
        self.strips = None

        # allows for switching of multiple textures
        self.current_texture = None
        self.animations = {}
        self.images = {}

        self.texture_folder = ""

        # the text shown when hovered by the cursor
        self.examine = ""

        # particles need to check for collisions with
        # all other sprites
        self.is_particle = False

        # turn the drawing of this sprite on or off
        self.visible = True

    def set_pixel_position(self, position):
        """Set the position of the sprite's center

        :param position:
        :return:
        """
        self.rect.center = position

    def next_frame(self):
        """Change the sprite to its next frame if it's animated

        :return:
        """
        if self.strips is not None:
            self.image = self.strips.next()

    def create_animation(self, file, rect, frames=8, loop=True):
        """Create, set and return an animation for the sprite.

        :param file: string file containing the sheet of animation frames
        :param rect: rect of the first sprite
        :param frames: int amount of frames in the animation
        :param loop: bool whether to loop or not
        :return: SheetAnimation object
        """
        try:
            sheet = util.get_sheet(file)
            self.strips = util.SheetAnimation(sheet, rect, frames, loop)
            self.image = self.strips.next()
            self.rect.size = self.image.get_rect().width - 1, self.image.get_rect().height - 1
            return self.strips
        except:
            print("Failed to load animation at {0} in {1}".format(rect, file))
            raise

    def add_animation(self, animation, rect, frames=8, loop=True, fpi=4):
        """Create and add an animation to the dict.

        :param animation: string name of animation
        :param rect: rect of sprite in the sprite sheet
        :param frames: int amount of frames
        :param loop: bool whether to loop or not
        :param fpi: int frames per image in animation (more = slower)
        :return:
        """
        if animation not in self.animations.keys():
            self.animations[animation] = self.create_animation("{0}{1}.png".format(self.texture_folder, animation),
                                                               rect, frames, loop)
            self.animations[animation].set_fpi(fpi)

    def set_animation(self, animation):
        """Set the current animation to one in the dict.

        :param animation: string name of animation to set to
        :return:
        """
        if self.current_texture is not animation and animation in self.animations.keys():
            # set strip to the animation in the dict
            self.strips = self.animations[animation]
            # update the image
            self.image = self.strips.next()
            # save name of current texture
            self.current_texture = animation
            # update size, just in case it was different
            self.rect.size = self.image.get_rect().width - 1, self.image.get_rect().height - 1

    def create_image(self, file, rect):
        """Create, set and return an image for the sprite.

        :param file: string file containing the image
        :param rect: rect of the location in file
        :return: pygame.Image
        """
        self.image = util.get_sheet(file).get_image(rect)
        _, _, self.rect[2], self.rect[3] = pygame.Rect(self.image.get_rect())
        self.rect.size = self.image.get_rect().width - 1, self.image.get_rect().height - 1
        return self.image

    def add_image(self, image, file, rect):
        """Create an add an image to the dict.

        :param image: string name of image
        :param file: string file containing image
        :param rect: rect of location in file
        """
        if image not in self.images.keys():
            self.images[image] = self.create_image(file, rect)

    def set_image(self, image):
        """Set the current image to one in the dict.

        :param image: string name of image
        """
        if self.current_texture is not image:
            self.image = self.images[image]
            self.current_texture = image
            self.rect.size = self.image.get_rect().width - 1, self.image.get_rect().height - 1

    def update(self):
        """Method to update the sprite on each frame.
        """
        pass

    def draw(self, screen):
        """Draw the sprite to the screen provided, as is with no translations.

        Does not draw if self.visible is False

        :param screen: pygame.Surface to draw to
        :return:
        """
        if self.visible:
            screen.blit(self.image, self.rect)

    def kill(self):
        """Set of instructions to execute when
        the sprite needs to be deleted.

        i.e. removal from rendering lists, shop lists,
        examine info lists

        :return:
        """
        pass


class GameSprite(Sprite):
    """Base class for a sprite that is located in the game world.

    It therefore needs to be affected by game physics (gravity)
    and it's drawing needs to be translated by the camera.
    """

    def __init__(self, position):
        Sprite.__init__(self, position)

        # add this sprite to the render and
        # examine lists
        render.add_game_sprites(self)
        examine.add_game_object(self)

        # velocity in x and y directions
        # position is saved in self.rect
        self.velocity = Vector(0, 0)

        # whether or not the sprite is touching
        # the ground and is able to jump
        self.grounded = False

    def draw(self, screen):
        """Draw the sprite translated by the camera's position.

        Does not draw if self.visible is False

        :param screen: pygame.Surface
        """
        if self.visible:
            screen.blit(self.image, camera.apply(self.rect))

    def kill(self):
        render.remove_game_sprites(self)
        examine.remove_game_object(self)

    def gravity_acceleration(self):
        """Method to change the sprite's acceleration downwards
        without needing to edit the update() method.

        :return: float gravity
        """
        return GRAVITY

    def update(self):
        """Apply velocity and check collisions.

        Override to change physics effects.
        """

        if not self.grounded:
            # apply gravity if player is not standing
            # on the ground
            self.velocity.y += self.gravity_acceleration()

            # estimated terminal velocity
            # subject to change
            if self.velocity.y > 60:
                self.velocity.y = 60

        # if the player is moving up or down
        if self.velocity.y != 0:
            self.grounded = False
            # this can be called even if there is no
            # "jump" animation
            self.set_animation("jump")

        self.collide()

    def collide(self):
        """Check if colliding with the map.

        The map is considered pixel perfect, however all other
        sprites are simple rects. This means irregularities in the
        map collide properly.
        """

        # the position the player will be at after
        # applying the x velocity
        next_rect = self.rect.move(self.velocity.x, 0)

        # test the three points on the left edge of the sprite
        # if any collide with the map, the sprite is clipping
        # on this side
        while test_edge(next_rect.topleft, next_rect.midleft, next_rect.bottomleft):
            # move the sprite to the right once, and check if
            # it is still clipping to the left
            next_rect = next_rect.move(1, 0)
            self.velocity.x = 0
            # continue until sprite is no longer clipping

        # same method, on the right edge of the sprite
        while test_edge(next_rect.topright, next_rect.midright, next_rect.bottomright):
            next_rect = next_rect.move(-1, 0)
            self.velocity.x = 0

        # update the rect, then use the same method to
        # test clipping on the top and bottom
        self.rect = next_rect

        # the position the player will be at after
        # applying the y velocity
        next_rect = self.rect.move(0, self.velocity.y)

        # same method, on the bottom edge of the sprite
        while test_edge(next_rect.bottomleft, next_rect.midbottom, next_rect.bottomright):
            next_rect = next_rect.move(0, -1)
            self.velocity.y = 0
            # if it has collided (even if it still needs to
            # move upwards) we know it's hit a floor
            # so grounded can be set to True
            self.grounded = True

        # same method, on the top edge of the sprite
        while test_edge(next_rect.topleft, next_rect.midtop, next_rect.topright):
            next_rect = next_rect.move(0, 1)
            self.velocity.y = 0

        # update the sprite rect
        self.rect = next_rect

        # check if the sprite is still on the floor, or
        # should start falling (from walking off an edge)

        # test the rect that is 1 pixel lower, to see if
        # it is colliding
        # if it isn't, the sprite is falling
        test_rect = self.rect.move(0, 1)
        if not test_edge(test_rect.bottomleft, test_rect.midbottom, test_rect.bottomright):
            self.grounded = False
            # fix jump count for players
            if hasattr(self, "jumps") and self.jumps == 0:
                self.jumps = 1


class ScreenSprite(Sprite):
    """Base class for a sprite that is drawn to the screen rather than the game world.
    """

    def __init__(self, position):
        Sprite.__init__(self, position)
        # add to render and examine lists
        render.add_screen_sprites(self)
        examine.add_screen_object(self)

    def kill(self):
        render.remove_screen_sprites(self)
        examine.remove_screen_object(self)
