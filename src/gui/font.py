import os
import pygame
import util

CHARS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
         'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f',
         'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
         'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '"',
         '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<',
         '>', '=', '?', '@', '[', ']', '\\', '^', '_', '{', '|', '}', ' ']


# create a font from a png with 6 rows of 16 characters, in the order of CHARS
def font_from_image(file):
    image = util.load_alpha_image("{0}{1}.png".format(util.SPRITES_FOLDER, file))
    char_h = image.get_height() // 6
    char_w = image.get_width() // 16

    images = []

    for i in range(6):
        x = 0
        y = i * char_h
        while x < image.get_width():
            images.append(image.subsurface((x, y), (char_w, char_h)))
            x += char_w

    return Font(images)


class Font(object):
    def __init__(self, char_images):
        self.chars = {}
        for i, char in enumerate(CHARS):
            self.chars[char] = char_images[i]
        self.char_w = char_images[0].get_width()
        self.char_h = char_images[0].get_height()

    def create_text(self, text):
        """
        Create a sprite using the font with the specified text

        :param text:
        :return:
        """

        # Make an array of only available characters
        chars = [char for char in text if char in self.chars]
        # Create a new surface that can fit the entire text
        image = pygame.Surface(((len(chars)) * self.char_w, self.char_h)).convert()
        image.fill((0, 0, 255))
        image.set_colorkey((0, 0, 255), pygame.RLEACCEL)
        # Add each char one by one to the surface
        for i, char in enumerate(chars):
            image.blit(self.chars[char], (i * self.char_w, 0))
        return image


# all fonts must be in a png with 6 rows of 16 columns
regular = font_from_image("reg_font")
title = font_from_image("title_font")
mini_num = font_from_image("mini_num_font")
