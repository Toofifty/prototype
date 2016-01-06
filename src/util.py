import pygame
import os

# directory management
# constants here should always be used
# where appropriate
DIR = os.path.dirname(__file__).replace("src", "", 1)
ASSETS_FOLDER = DIR + "assets\\"
SPRITES_FOLDER = ASSETS_FOLDER + "sprites\\"
MAPS_FOLDER = ASSETS_FOLDER + "maps\\"

# list of loaded sheets to prevent
# reloading sheets when used multiple
# times
loaded_sheets = []


def load_alpha_image(src):
    """Load and return an image.

    :param src: string source file
    :return: pygame.Image
    """
    return pygame.image.load(src).convert_alpha()


def get_sheet(file):
    """Get the sheet object at file, creates one if it doesn't exist.

    :param file: string file location
    :return: SpriteSheet object
    """
    for sheet in loaded_sheets:
        if sheet.file == file:
            return sheet
    return SpriteSheet(file)


def read(file):
    """Read lines from a file and return a list of strings.

    :param file: string file location
    :return: list of strings
    """
    with open(file, "r") as file:
        return [line.rstrip() for line in file]


class Vector(object):
    """Easy 2D or 3D vector access.
    """
    def __init__(self, x, y, z=None):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "({0}, {1}, {2})".format(self.x, self.y, self.z) if self.z else "({0}, {1})".format(self.x, self.y)

    @property
    def tup(self):
        """Get x,y as a tuple.
        :return: tuple (x, y)
        """
        return self.x, self.y

    @property
    def tup3(self):
        """Get x,y,z as a tuple.
        :return: tuple (x, y, z)
        """
        return self.x, self.y, self.z


class SpriteSheet(object):
    """Contains the image of a sprite sheet and methods to extract sprites from it.
    """

    def __init__(self, file):
        self.sheet = load_alpha_image(SPRITES_FOLDER + file)
        self.file = file
        loaded_sheets.append(self)

    def get_image(self, rect):
        """Grab a single image at rect from the sprite sheet

        :param rect: rect location of image
        :return image: pygame.Image
        """
        return self.sheet.subsurface(rect)

    def get_images(self, rect_list):
        """Get a list of images from a list of rect positions.

        :param rect_list: list of rect locations
        :return list of images:
        """
        return [self.get_image(rect) for rect in rect_list]

    def get_strip(self, rect, frames):
        """Get a strip of sprites along the x axis, to use as an animation.

        :param rect: rect of first image
        :param frames: int amount of frames
        :return list of images:
        """
        sprites = [
            (rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
            for x in range(frames)
            ]
        return self.get_images(sprites)


class SheetAnimation(object):
    """Single animation controller
    """

    def __init__(self, sheet, rect, frames, loop=True):
        self.sheet = sheet
        self.images = self.sheet.get_strip(rect, frames)
        self.rect = rect

        # Iterator containing current frame id
        self.i = 0
        # Frames per image (allows for slower anims)
        self.fpi = 2
        self.loop = loop

        # Current image frame (controls frames per image drawing)
        self.cif = 2

    def copy(self):
        """Return a copy of this animation with the same attributes.

        Useful for particles, since playing the same animation instance
        twice will have it update twice as fast and display the same
        frame in both places.

        :return: SheetAnimation
        """
        return SheetAnimation(self.sheet, self.rect, len(self.images), self.loop).set_fpi(self.fpi)

    def set_fpi(self, fpi):
        """Set the frames per image rate.

        i.e. 2 fpi means the next sprite frame will be after
        2 game frames

        :param fpi: int frames per image
        :return: SheetAnimation self, for ease of use
        """
        self.fpi = fpi
        return self

    def next(self):
        """Get the next image in the animation sequence.

        :return: pygame.Image next image
        """
        if self.i >= len(self.images):
            if self.loop:
                self.i = 0
            else:
                self.i -= 1
        image = self.images[self.i]
        self.cif -= 1
        if self.cif == 0:
            self.i += 1
            self.cif = self.fpi

        return image
