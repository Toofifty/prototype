import pygame

import util
import options
from entity.sprites import Sprite



class Cursor(Sprite):
    def __init__(self, position, text_font):
        Sprite.__init__(self, position)

        self.add_image("clicked", "other/gui.png", (16, 0, 16, 16))
        self.add_image("default", "other/gui.png", (0, 0, 16, 16))

        self.rect.topleft = position

        self.clicked = False

        self.hover_text = HoverText(position, text_font)
        self.set_hover_text("")

    def point(self):
        return self.rect.topleft

    def move(self, position, click):
        if click and not self.clicked:
            self.click(position)
        elif not click and self.clicked == True:
            self.set_image("default")
            self.clicked = False

        self.rect.topleft = position
        self.hover_text.move(self.rect.bottomright)

        self.dirty = 1

    def click(self, position):
        self.set_image("clicked")
        self.clicked = True

    def position(self):
        return self.rect.topleft

    def set_hover_text(self, text_list):
        self.hover_text.set_examine(text_list)


class HoverText(Sprite):
    def __init__(self, position, font):
        Sprite.__init__(self, position)
        self.font = font
        template = util.get_sheet("other/gui.png").get_image((32, 0, 12, 12))
        self.background = util.GUIBackground(template)
        self.image = None

    def set_text(self, text):
        self.image = self.font.create_text(text)

    def set_examine(self, lines):
        if len(lines) > 0:
            max_len = max(len(l) for l in lines)
            image = pygame.Surface((max_len * self.font.char_w + 8, len(lines) * self.font.char_h + 8)).convert()
            image.fill((0, 0, 255))
            image.set_colorkey((0, 0, 255), pygame.RLEACCEL)
            self.background.draw_on(image)
            for i, line in enumerate(lines):
                image.blit(self.font.create_text(line), (4, 4 + i * self.font.char_h))
            self.image = image
            self.rect.size = self.image.get_rect().size
        else:
            self.set_text("")

    def move(self, position):
        self.rect.topleft = position
        if self.rect.bottom > options.game_height():
            self.rect.bottom = options.game_height()
        if self.rect.right > options.game_width():
            self.rect.right = options.game_width()
