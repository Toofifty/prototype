import pygame
from entity.sprites import ScreenSprite, GameSprite

ITEM_FOLDER = "item\\"

dropped_items = []


def item_collide(player):
    for item in dropped_items:
        item.collide(player)


class DroppedItem(GameSprite):
    def __init__(self, item, position):
        GameSprite.__init__(self, position)
        self.examine = item.examine
        self.item = item
        self.image = item.image
        self.rect.size = self.image.get_rect().size
        dropped_items.append(self)

    def collide_player(self, player):
        if pygame.sprite.collide_rect(self, player):
            self.pickup(player)

    def pickup(self, player):
        player.add_item(self.item)
        self.kill()
        dropped_items.remove(self)


class Item(ScreenSprite):
    def __init__(self, name, desc, position=(0, 0)):
        ScreenSprite.__init__(self, position)
        self.examine = "{}: {}".format(name.title(), desc)
        self.amount = 0

    def set_icon(self, sheet, position):
        self.create_image("{}{}.png".format(ITEM_FOLDER, sheet), position)

    def acquire(self):
        self.visible = True
        self.amount += 1

    def draw_on_player(self, player):
        pass
