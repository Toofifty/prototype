from entity.sprites import Sprite


class Cursor(Sprite):
    def __init__(self, position, text_font):
        Sprite.__init__(self, position)

        self.add_sheet_image("clicked", "other/gui.png", (16, 0, 16, 16))
        self.add_sheet_image("default", "other/gui.png", (0, 0, 16, 16))

        self.rect.topleft = position

        self.clicked = False

        self.hover_text = HoverText(position, text_font)
        self.set_hover_text("")

    def point(self):
        return self.rect.topleft

    def update(self, position, click):
        if click and not self.clicked:
            self.click(position)
        elif not click and self.clicked == True:
            self.set_image("default")
            self.clicked = False

        self.rect.topleft = position
        self.hover_text.update(self.rect.bottomright)

        self.dirty = 1

    def click(self, position):
        self.set_image("clicked")
        self.clicked = True

    def position(self):
        return self.rect.topleft

    def set_hover_text(self, text):
        self.hover_text.set_text(text)


class HoverText(Sprite):
    def __init__(self, position, font):
        Sprite.__init__(self, position)
        self.font = font
        self.image = None

    def set_text(self, text):
        self.image = self.font.create_text(text)

    def update(self, position):
        self.rect.topleft = position
