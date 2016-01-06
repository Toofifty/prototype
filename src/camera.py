from pygame.locals import Rect

import options

camera = None


def init(map_width, map_height):
    """Set the camera's boundaries to the map size

    :param map_width:
    :param map_height:
    """
    global camera
    camera = Rect(0, 0, map_width, map_height)


def apply(target):
    """Apply the camera's translation to a rect

    :param target: rect to translate
    :return: new rect translated by the camera
    """
    return target.move(camera.topleft)


def follow(target):
    """Follow and centre on the target rect

    :param target: rect to follow
    """
    width = options.view_width() // options.scale()
    height = options.view_height() // options.scale()

    l, t, _, _ = target
    _, _, w, h = camera
    l, t = width // 2 - l, height // 2 - t

    l = min(0, l)
    l = max(width - camera.width, l)
    t = max(height - camera.height, t)
    t = min(0, t)

    global camera
    camera = Rect(l, t, w, h)
