from item.base import Item
from entity.sprites import JUMP_HEIGHT
from entity import particle


class AngelBoots(Item):
    def __init__(self):
        Item.__init__(self, "angel boots", "gain an extra jump")
        self.set_icon("angel_boots", (0, 0, 16, 16))
        self.visible = False

    def post_jump(self, player):
        if not player.grounded and player.jumps <= self.amount:
            player.velocity.y = -JUMP_HEIGHT
            particle.animated_effect("jump", player.rect.move(-8, 0).topleft)
            player.jumps += 1
