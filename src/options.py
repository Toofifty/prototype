options = {
    "view_width": 1280,
    "view_height": 640,
    "fullscreen": 0,
    "scale": 2
}

def fullscreen():
    return options["fullscreen"] == 1


def view_width():
    return options["view_width"]


def view_height():
    return options["view_height"]


def scale():
    return options["scale"]


def dimensions():
    return view_width(), view_height()


def game_dimensions():
    return view_width() // scale(), view_height() // scale()


def centre():
    return view_width() // 2, view_height() // 2