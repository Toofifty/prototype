import os
import pygame
import util

CHARS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
         'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f',
         'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
         'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '"',
         '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<',
         '>', '=', '?', '@', '[', ']', '\\', '^', '_', '{', '|', '}', ' ']


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
        image = pygame.Surface(((len(chars) + 2) * self.char_w, self.char_h)).convert()
        image.fill((0, 0, 255))
        image.set_colorkey((0, 0, 255), pygame.RLEACCEL)
        # Add each char one by one to the surface
        for i, char in enumerate(chars):
            image.blit(self.chars[char], (i * self.char_w, 0))
        return image

class GameFont(Font):
    def __init__(self):
        num_rows = 6
        char_width = 8

        self.font_image = util.load_alpha_image("{0}reg_font.png".format(util.SPRITES_FOLDER))

        char_images = []
        char_height = self.font_image.get_height() // num_rows

        for i in range(num_rows):
            x = 0
            y = i * char_height
            while x < self.font_image.get_width():
                char_image = self.font_image.subsurface((x, y), (char_width, char_height))
                char_images.append(char_image)
                x += char_width

        Font.__init__(self, char_images)