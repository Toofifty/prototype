from perk import BasicPerk
from entity.sprites import JUMP_HEIGHT
from entity import particle


class AngelBoots(BasicPerk):
    def __init__(self):
        BasicPerk.__init__(self, "angel boots", "+1 jump")
        self.set_icon("angel_boots", (0, 0, 16, 16))
        self.set_max_amount(4)
        self.visible = False

    def post_jump(self, player):
        if not player.grounded and player.jumps <= self.amount:
            player.velocity.y = -JUMP_HEIGHT
            particle.animated_effect("jump", player.rect.move(-8, 0).topleft)
            player.jumps += 1
