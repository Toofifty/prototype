import pygame
from entity.sprites import ScreenSprite, GameSprite
from gui import font

ITEM_FOLDER = "perk\\"

# list of perks currently dropped on the
# ground that can be picked up by players
dropped_perks = []


def perk_collide(player):
    """Check each perk to see if the player has collided with it, and
    pick up the perk if it has.

    :param player:
    :return:
    """
    for perk in dropped_perks:
        if pygame.sprite.collide_rect(perk, player):
            perk.pickup(player)


class DroppedPerk(GameSprite):
    """GameSprite container for an perk dropped in the world.

    Can be dropped from chests and is picked up when a player
    collides with it.
    """

    def __init__(self, perk, position):
        """
        :param item: base.Item instance perk to show
        :param position: world position to drop the perk
        """
        GameSprite.__init__(self, position)
        self.examine = perk.examine
        self.item = perk
        self.image = perk.original_icon
        self.rect.size = self.image.get_rect().size
        dropped_perks.append(self)

    def kill(self):
        # may be killed by other means than being picked up
        # i.e. despawn timer, leaving area
        GameSprite.kill(self)
        dropped_perks.remove(self)

    def pickup(self, player):
        """Add the perk to the player's inventory then destroys the dropped perk.

        :param player: player to receive perk
        """
        if player.add_item(self.item):
            self.kill()


class BasicPerk(ScreenSprite):
    """Base perk class.

    Contains the amount and basic functions of every perk.
    """

    def __init__(self, name, desc, position=(0, 0)):
        ScreenSprite.__init__(self, position)
        self.examine = [name.title(), desc]
        self.amount = 0
        self.player_effect = None
        self.original_icon = None
        self.max_amount = 16

    def set_max_amount(self, amount):
        """Set the maximum amount of this item the player can own
        """
        self.max_amount = amount

    def add_player_effect(self):
        """Add a player effect sprite.
        """
        self.player_effect = GameSprite((0, 0))

    def set_icon(self, file, rect):
        """Set the inventory icon of the perk.

        :param file: string file to load from
        :param rect: rect location of image
        """
        self.create_image("{}{}.png".format(ITEM_FOLDER, file), rect)
        self.original_icon = self.image

    def acquire(self):
        """Acquire another perk of this type.

        :return: true if successful
        """
        if self.amount >= self.max_amount:
            return False

        self.visible = True
        self.amount += 1
        if self.amount > 1:
            am_image = font.mini_num.create_text(str(self.amount))
            new_icon = self.original_icon.copy()
            pos = (new_icon.get_width() - am_image.get_width(), new_icon.get_height() - am_image.get_height())
            print(am_image.get_size())
            print(pos)
            new_icon.blit(am_image, pos)
            self.image = new_icon

        return True

    def draw_on_player(self, player, screen):
        """Draw an image or animation on the player.

        :param player: player to draw on
        :param screen: screen to blit to
        """
        if self.player_effect is not None:
            self.player_effect.rect.center = player.rect.center
            # TODO: allow for animations and syncing of animations to player
            # self.player_effect.set_animation(player.get_animation())
            self.player_effect.set_image(player.get_animation())
            self.player_effect.draw(screen)

    # Hook methods
    # used to change player behaviour without directly altering
    # the player class

    # All pre_ methods have the option of cancelling the
    # player event by returning True

    def pre_jump(self, player):
        return False

    def post_jump(self, player):
        pass

    def pre_shoot(self, player):
        return False

    def post_shoot(self, player):
        pass

    def pre_update(self, player):
        return False

    def post_update(self, player):
        pass
