import pygame

from entity import particle
from entity.__init__ import NetEntity
from entity.sprites import WALK_SPEED, SPRINT_MULT, JUMP_HEIGHT


class Player(NetEntity):
    """Basic player.

    Contains inventory, animations, jumps and weapon changes.

    Does not contain keyboard control (see LocalPlayer)
    """

    def __init__(self, name, position=(0, 0)):
        """
        :param name: string name of character
        :param position: tuple(2) starting position
        """
        NetEntity.__init__(self, position)

        # set the texture folder
        self.texture_folder = "player\\{}\\".format(name)

        # Add all animations
        # Last animation loaded will be used
        self.add_animation("jump_armed", (0, 0, 16, 32), frames=4, fpi=6)
        # self.add_animation("run_armed", (0, 0, 16, 32), frames=15, fpi=4)
        self.add_animation("idle_armed", (0, 0, 16, 32), frames=4, fpi=30)

        self.add_animation("jump_unarmed", (0, 0, 16, 32), frames=4, fpi=15)
        # self.add_animation("run_unarmed", (0, 0, 16, 32), frames=15, fpi=4)
        self.add_animation("idle_unarmed", (0, 0, 16, 32), frames=4, fpi=30)

        # whether or not the character sprite is
        # facing right (False) or left (True)
        self.flipped = False

        # set the examine to the name of the
        # character.
        # will most likely be changed to player's
        # username, and name replaced with 'skin'
        self.examine = [name.title(), "Lvl 1 scout", "Unarmed"]

        # if the player has at least one gun
        self.is_armed = False

        # player's two guns
        # primary is always the one shown
        # on the character
        self.primary = None
        self.secondary = None

        # amount of jumps performed by player
        self.jumps = 0

        # used to prevent instant double jumps
        # since a keypress may last more than
        # one frame
        self.is_jumping = False

        # inventory of perks
        # amount of perks are stored in the perks
        # themselves
        self.perks = []

    def add_item(self, item):
        """Add an perk to the player's inventory.

        :param item: perk to add
        """
        # do not add the perk if it is already in
        # the list, multiples are handled inside
        # the perk class as perk.amount
        if not item in self.perks:
            self.perks.append(item)

        # tell the perk to increment it's stack
        # and become visible
        item.acquire()

    def _jump(self):
        """Internal jump method.

        Called inside the regular jump method, which may
        be modified by perks.

        :return: True if jump is successful, False if not
        """

        # only jump off the ground, multiple jumps
        # are handled in the external jump() method
        if self.grounded:
            # set the velocity to one upwards
            self.velocity.y = -JUMP_HEIGHT
            # play particle effect
            particle.animated_effect("jump", self.rect.move(-8, 0).topleft)
            self.grounded = False
            self.jumps = 1
            return True
        return False

    def jump(self):
        """External jump method.

        Check perks for pre_ methods, then performs
        the internal method and checks perks for post_
        methods.

        """
        # calls the pre_jump method
        # on all perks
        # if any return True, the internal jump is cancelled
        cancel = any(perk.pre_jump(self) for perk in self.perks)

        if not cancel:
            # if the first jump is successful, we
            # shouldn't be able to jump again straight
            # away (prevents instant double jumps)
            if self._jump():
                return

        # calls the post_jump method
        # on all perks
        [perk.post_jump(self) for perk in self.perks]

    def add_weapon(self, weapon):
        """Add a weapon as primary or secondary, swapping out primary if both are taken.

        :param weapon: weapon to add
        """
        if self.primary is None:
            self.primary = weapon
            self.is_armed = True

        elif self.secondary is None:
            # push primary into secondary slot
            self.secondary = weapon
            self.swap_weapons()

        else:
            self.drop_primary()
            self.primary = weapon
        weapon.being_used = True

    def drop_primary(self):
        if self.primary is not None:
            self.primary.being_used = False
            self.primary = None
            if self.secondary is not None:
                self.primary = self.secondary
                self.secondary = None
            else:
                self.primary = None

    def swap_weapons(self):
        """Swap primary and secondary weapons.
        """
        t = self.primary
        self.primary = self.secondary
        self.secondary = t
        self.is_armed = self.primary is not None

    def set_animation(self, animation):
        """Override method to set the animation with armed/unarmed variants.

        :param animation: string animation name
        """
        if self.is_armed:
            NetEntity.set_animation(self, animation + "_armed")
        else:
            NetEntity.set_animation(self, animation + "_unarmed")

    def get_animation(self):
        """Get the animation name, minus armed/unarmed.

        :return: string animation name
        """
        return self.current_texture.split("_", 1)[0]

    def flip(self, flip):
        """Flip the player to the direction.

        :param flip: bool right=False left=True
        """
        self.flipped = flip

    def shoot(self):
        """Shoot the current gun held, or punch/swing fist/sword.
        """
        if self.primary is not None:
            self.primary.shoot()

    def update(self):
        if self.velocity.x != 0:
            self.set_animation("run")
            self.flipped = self.velocity.x < 0
        else:
            self.set_animation("idle")

        NetEntity.update(self)

    def draw(self, screen):
        """Draw the player to the screen.

        Also draws the primary weapon in a suitable position,
        manually moving to the player's animation.

        Key pixels for weapon positions may be necessary.

        :param screen: pygame.Surface to draw to
        """

        # get next frame
        self.next_frame()

        # flip sprite
        if self.flipped:
            self.image = pygame.transform.flip(self.image, True, False)

        NetEntity.draw(self, screen)

        # overlay perk effects on player
        [item.draw_on_player(self, screen) for item in self.perks]

        if self.primary is not None:
            x_tr = 6
            y_tr = -5
            if self.examine == "Kyle":
                # kyle is short
                y_tr = -1

            # manual tracking of gun onto player animation
            # TODO!!
            if self.get_animation() == "idle" and self.strips.i in [2, 3]:
                y_tr += 1

            elif self.get_animation() == "run" and self.strips.i in [0, 1, 2, 7, 8, 9]:
                y_tr -= 1

            # add recoil to the gun (if it is recoiling)
            # TODO: currently broken
            x_tr += self.primary.recoil * (1 if self.flipped else -1)

            # flip gun to match player
            if self.primary.flipped is not self.flipped:
                self.primary.flipped = self.flipped
                self.primary.image = pygame.transform.flip(self.primary.image, True, False)

            grip_w = self.primary.grip_point

            # move the gun rect left or right depending
            # on which way its facing
            if self.primary.flipped:
                self.primary.rect.topright = self.rect.move((-x_tr + grip_w, y_tr)).center

            else:
                self.primary.rect.topleft = self.rect.move((x_tr - grip_w, y_tr)).center

            self.primary.draw(screen)

            # recover the gun from recoil
            # should be moved
            if self.primary.recoil > 0:
                self.primary.recover_recoil()


class LocalPlayer(Player):
    """Player that the client is controlling.

    Handles controls from the Control class
    """

    def __init__(self, name, controls):
        Player.__init__(self, name, (500, 900))
        self.controls = controls

    def update(self):
        """Apply user controls.
        """

        if self.controls.jump and not self.is_jumping:
            self.jump()
            # is_jumping ensures the player can't jump
            # more than once without lifting the jump button
            self.is_jumping = True

        if not self.controls.jump:
            # player has lifted the jump button, can now
            # jump again
            self.is_jumping = False

        if self.controls.left:
            # set velocity to walk_speed facing left
            self.velocity.x = -WALK_SPEED * (SPRINT_MULT if self.controls.shift else 1)

        elif self.controls.right:
            # set velocity to walk_speed facing right
            self.velocity.x = WALK_SPEED * (SPRINT_MULT if self.controls.shift else 1)

        else:
            # no movement input == idle
            self.velocity.x = 0

        Player.update(self)
