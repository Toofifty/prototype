"""
Handles the game loop and all game logic

"""

from enum import Enum

import pygame

import camera
import options
import render
import map
from controls import Controls
from entity import particle
from entity.player import LocalPlayer
from gui import examine
from gui.cursor import Cursor
from gui.font import GameFont
from weapon.gun import Gun
from item.base import DroppedItem, item_collide
from item.angelboots import AngelBoots

EXIT = 0
RUNNING = 1

controls = Controls()
player1 = None
player2 = None

cursor = None
state = 1

ab = None

def init():
    pygame.init()
    render.init()
    particle.init()

    global player1
    player1 = LocalPlayer("kyle", controls)

    global cursor
    cursor = Cursor(options.centre(), GameFont())

    render.add_screen_sprites(cursor, cursor.hover_text)

    map.load_map("2")

    global ab
    ab = AngelBoots()

    camera.init(map.width(), map.height())

def run():
    play_time = 0
    clock = pygame.time.Clock()

    while state == RUNNING:
        ms = clock.tick(60)
        play_time += ms / 1000.0

        # handle player inputs
        action = controls.process_event(pygame.event.get())
        controls.update_keys()

        if action == "shoot":
            player1.shoot()
        elif action == "spawn_item":
            DroppedItem(ab, player1.rect.move(30, 0).center)

        # update cursor
        cursor_pos_x, cursor_pos_y = pygame.mouse.get_pos()
        cursor.update((cursor_pos_x / options.scale(), cursor_pos_y / options.scale()),
                           controls.click)

        # update cursor text
        cursor.set_hover_text(examine.find_examine_text(cursor.point()))

        # update window title to show frame rate
        pygame.display.set_caption("FPS: {0:.2f}".format(clock.get_fps()))

        # flip player to face cursor
        player1.flip(cursor.point()[0] < camera.apply(player1.rect).centerx)

        item_collide(player1)

        # render screen
        render.draw()

        # debug help
        if action == "change_gun":
            player1.add_weapon(Gun((0, 0)))