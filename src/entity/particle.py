import render
import util
from entity.sprites import GameSprite

PARTICLE_FOLDER = "anim\\"

animated_effects = {}

particle_effects = {}

active_particles = []


def init():
    animated_effects["jump"] = util.SheetAnimation(
            util.get_sheet("{}{}.png".format(PARTICLE_FOLDER, "jump")), (0, 0, 32, 32), 8, False).set_fpi(4)

    animated_effects["hit"] = util.SheetAnimation(
            util.get_sheet("{}{}.png".format(PARTICLE_FOLDER, "hit")), (0, 0, 8, 8), 5, False).set_fpi(4)

    particle_effects["bullet"] = util.load_alpha_image("{}\\gun\\bullet\\1.png".format(util.SPRITES_FOLDER))


def animated_effect(effect_name, position):
    if effect_name in animated_effects.keys():
        render.add_game_sprites(Particle(position, animated_effects[effect_name].copy()))


def particle_effect(effect_name, position):
    if effect_name in particle_effects.keys():
        render.add_game_sprites(Particle(position, particle_effects[effect_name]))


def moving_particle_effect(effect_name, position, func):
    if effect_name in particle_effects.keys():
        render.add_game_sprites(MovingParticle(position, particle_effects[effect_name], func))


def get_texture(effect_name):
    if effect_name in animated_effects.keys():
        return animated_effects[effect_name]
    elif effect_name in particle_effects.keys():
        return particle_effects[effect_name]
    return None


class Particle(GameSprite):
    def __init__(self, position, texture):
        GameSprite.__init__(self, position)
        self.texture = texture
        self.update()
        self.is_particle = True

    def update(self):
        if hasattr(self.texture, "next"):
            self.image = self.texture.next()
            if self.texture.i == len(self.texture.images):
                self.kill()
        else:
            self.image = self.texture


class MovingParticle(Particle):
    def __init__(self, position, texture, func):
        self.func = func
        Particle.__init__(self, position, texture)

    def update(self):
        self.rect.center = self.func(self)
        return Particle.update(self)
