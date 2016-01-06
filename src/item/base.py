import pygame
from entity.sprites import ScreenSprite, GameSprite

ITEM_FOLDER = "item\\"

# list of items currently dropped on the
# ground that can be picked up by players
dropped_items = []


def item_collide(player):
    """Check each item to see if the player has collided with it, and
    pick up the item if it has.

    :param player:
    :return:
    """
    for item in dropped_items:
        if pygame.sprite.collide_rect(item, player):
            item.pickup(player)


class DroppedItem(GameSprite):
    """GameSprite container for an item dropped in the world.

    Can be dropped from chests and is picked up when a player
    collides with it.
    """

    def __init__(self, item, position):
        """
        :param item: base.Item instance item to show
        :param position: world position to drop the item
        """
        GameSprite.__init__(self, position)
        self.examine = item.examine
        self.item = item
        self.image = item.image
        self.rect.size = self.image.get_rect().size
        dropped_items.append(self)

    def kill(self):
        # may be killed by other means than being picked up
        # i.e. despawn timer, leaving area
        GameSprite.kill(self)
        dropped_items.remove(self)

    def pickup(self, player):
        """Add the item to the player's inventory then destroys the dropped item.

        :param player: player to receive item
        """
        player.add_item(self.item)
        self.kill()


class Item(ScreenSprite):
    """Base item class.

    Contains the amount and basic functions of every item.
    """
    def __init__(self, name, desc, position=(0, 0)):
        ScreenSprite.__init__(self, position)
        self.examine = "{}: {}".format(name.title(), desc)
        self.amount = 0
        self.player_effect = None

    def add_player_effect(self):
        """Add a player effect sprite.
        """
        self.player_effect = GameSprite((0, 0))

    def set_icon(self, file, rect):
        """Set the inventory icon of the item.

        :param file: string file to load from
        :param rect: rect location of image
        """
        self.create_image("{}{}.png".format(ITEM_FOLDER, file), rect)

    def acquire(self):
        """Acquire another item of this type.
        """
        self.visible = True
        self.amount += 1

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
