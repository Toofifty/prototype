import pygame

import camera
from entity import particle
from entity.sprites import GameSprite, WALK_SPEED, SPRINT_MULT, JUMP_HEIGHT


class Player(GameSprite):
    def __init__(self, name, position=(0, 0)):
        GameSprite.__init__(self, position)

        self.texture_folder = "player\\{}\\".format(name)

        # Add all animations
        # Last animation loaded will be used
        self.add_animation("jump_armed", (0, 0, 16, 32), frames=4, fpi=6)
        self.add_animation("run_armed", (0, 0, 16, 32), frames=15, fpi=4)
        self.add_animation("idle_armed", (0, 0, 16, 32), frames=2, fpi=30)

        self.add_animation("jump_unarmed", (0, 0, 16, 32), frames=4, fpi=6)
        self.add_animation("run_unarmed", (0, 0, 16, 32), frames=15, fpi=4)
        self.add_animation("idle_unarmed", (0, 0, 16, 32), frames=2, fpi=30)

        self.rect[0] = position[0]
        self.rect[1] = position[1]

        self.flipped = False

        self.examine = name.title()

        self.is_armed = False

        self.primary = None
        self.secondary = None

        self.jumps = 0
        self.is_jumping = False

        self.items = []

    def add_item(self, item):
        if not item in self.items:
            self.items.append(item)
        item.acquire()

    def _jump(self):
        if self.grounded:
            self.velocity.y -= JUMP_HEIGHT
            particle.animated_effect("jump", self.rect.move(-8, 0).topleft)
            self.grounded = False
            self.jumps = 1
            return True
        return False

    def jump(self):
        cancel = False
        for item in self.items:
            if hasattr(item, "pre_jump"):
                cancel = cancel or item.pre_jump(self)

        if not cancel:
            if self._jump(): return

        for item in self.items:
            if hasattr(item, "post_jump"):
                item.post_jump(self)

    def add_weapon(self, weapon):

        if self.primary is not None:
            self.primary.kill()
        self.primary = weapon

        self.is_armed = True
        return
        if self.primary is None:
            self.primary = weapon

        elif self.secondary is None:
            self.secondary = self.primary
            self.primary = weapon

        else:
            pass

    def swap_weapons(self):
        t = self.primary
        self.primary = self.secondary
        self.secondary = t
        self.is_armed = self.primary is not None

    def set_animation(self, animation):
        if self.is_armed:
            GameSprite.set_animation(self, animation + "_armed")
        else:
            GameSprite.set_animation(self, animation + "_unarmed")

    def get_animation(self):
        return self.current_texture.split("_", 1)[0]

    def flip(self, flip):
        self.flipped = flip

    def update(self):

        GameSprite.update(self)

        self.next_frame()

        if self.flipped:
            self.image = pygame.transform.flip(self.image, True, False)

        self.dirty = 1

    def shoot(self):
        if self.primary is not None:
            self.primary.shoot()

    def draw(self, screen):
        screen.blit(self.image, camera.apply(self.rect))

        for item in self.items:
            item.draw_on_player(self)

        if self.primary is not None:
            x_tr = 6
            if self.examine == "Kyle":
                y_tr = -1
            elif self.examine == "Arnold":
                y_tr = -5
            if self.get_animation() == "idle" and self.strips.i == 1:
                y_tr += 1

            elif self.get_animation() == "run" and self.strips.i in [0, 1, 2, 7, 8, 9]:
                y_tr -= 1

            x_tr += self.primary.recoil * (1 if self.flipped else -1)

            if self.primary.flipped is not self.flipped:
                self.primary.flipped = self.flipped
                self.primary.image = pygame.transform.flip(self.primary.image, True, False)

            grip_w = self.primary.grip_point

            if self.primary.flipped:
                self.primary.rect.topright = self.rect.move((-x_tr + grip_w, y_tr)).center

            else:
                self.primary.rect.topleft = self.rect.move((x_tr - grip_w, y_tr)).center

            screen.blit(self.primary.image, camera.apply(self.primary.rect))

            if self.primary.recoil > 0:
                self.primary.recover_recoil()


class LocalPlayer(Player):
    def __init__(self, name, controls):
        Player.__init__(self, name, (500, 900))
        self.controls = controls

    def update(self):

        if self.controls.jump and not self.is_jumping:
            self.jump()
            self.is_jumping = True

        if not self.controls.jump:
            self.is_jumping = False

        if self.controls.left:
            self.velocity.x = -WALK_SPEED * (SPRINT_MULT if self.controls.shift else 1)
            self.set_animation("run")
            if not self.flipped:
                self.flipped = True

        elif self.controls.right:
            self.velocity.x = WALK_SPEED * (SPRINT_MULT if self.controls.shift else 1)
            self.set_animation("run")
            if self.flipped:
                self.flipped = False

        else:
            self.velocity.x = 0
            self.set_animation("idle")

        Player.update(self)
