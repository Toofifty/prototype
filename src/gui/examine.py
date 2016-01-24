import camera

screen_objects = []
game_objects = []


def add_screen_object(game_sprite):
    screen_objects.append(game_sprite)


def add_game_object(game_sprite):
    game_objects.append(game_sprite)


def remove_screen_object(game_sprite):
    try:
        screen_objects.remove(game_sprite)
    except ValueError:
        pass


def remove_game_object(game_sprite):
    try:
        game_objects.remove(game_sprite)
    except ValueError:
        pass


def find_examine_text(cursor_pos):
    for obj in screen_objects:
        if obj.rect.collidepoint(cursor_pos):
            return obj.examine

    for obj in game_objects:
        # regular collision
        if camera.apply(obj.rect).collidepoint(cursor_pos):
            return obj.examine

        # pixel perfect collision
        # try:
        #     rel_point = util.sub(cursor_pos, camera.apply(object).topleft)
        #     if object.mask.get_at(rel_point):
        #         return object.examine
        # except (IndexError, AttributeError):
        #     pass
    return ""
