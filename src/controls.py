from pygame.locals import *
import pygame

class Controls(object):
    def __init__(self):
        self.up = self.down = self.left = self.right = False
        self.jump = self.shift = self.cam_left = self.cam_right = False
        self.click = self.scroll_up = self.scroll_down = False

    def update_keys(self):
        keys = pygame.key.get_pressed()
        self.jump = keys[K_SPACE]
        self.up = keys[K_w]
        self.down = keys[K_s]
        self.left = keys[K_a]
        self.right = keys[K_d]
        self.shift = keys[KMOD_SHIFT]
        self.cam_left = keys[K_LEFT]
        self.cam_right = keys[K_RIGHT]


    def process_event(self, event):
        """
        Used for single actions, like toggles
        etc. update_keys() should be used for movement
        and continuous key checking

        :param event:
        :return:
        """

        action = None

        # Process all sub events
        for e in event:
            if e.type == QUIT:
                raise SystemExit("QUIT")

            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    # TODO: pause and menu
                    raise SystemExit("ESCAPE-QUIT")

                elif e.key == K_e:
                    action = "change_gun"

                elif e.key == K_r:
                    action = "spawn_item"

                elif e.key == K_RETURN:
                    action = "new_player"

                elif e.key == K_F11:
                    action = "fullscreen"

            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    # TODO: click event
                    self.click = True
                    action = "shoot"

                elif e.button == 5:
                    self.scroll_up = True
                    # self.scroll_down = False

                elif e.button == 4:
                    self.scroll_down = True
                    # self.scroll_up = False

            elif e.type == MOUSEBUTTONUP:
                if e.button == 1:
                    self.click = False

                elif e.button == 5:
                    self.scroll_up = False

                elif e.button == 4:
                    self.scroll_down = False

            return action
