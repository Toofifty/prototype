"""
Handles the game loop and all game logic

"""

import pygame
import select
from threading import Thread

import camera
import options
import render
import map
import util
from gui import font
from controls import Controls
from entity import particle, __init__
from entity.player import LocalPlayer, Player
from gui import examine
from gui.cursor import Cursor
from net import client, host, common

# debug imports
from weapon.gun import Gun
from perk import DroppedPerk, perk_collide
from perk.angelboots import AngelBoots

EXIT = 0
RUNNING = 1

controls = Controls()
player1 = LocalPlayer("arnold", controls)
player2 = None

cursor = Cursor(options.centre(), font.regular)
state = 1

ab = AngelBoots()

is_host = False


def init():
    particle.init()

    render.add_screen_sprites(cursor, cursor.hover_text)

    map.load_map("2")

    camera.init(map.width(), map.height())


def init_host():
    global is_host
    is_host = True

    host.init(1)

    t = Thread(target=host_loop)
    t.daemon = True
    t.start()

    init_net()


def init_net():
    if not is_host:
        client.init("localhost", 43244)
        __init__.set_player_to(1)

    t = Thread(target=net_loop)
    t.daemon = True
    t.start()


def run():
    play_time = 0
    clock = pygame.time.Clock()

    while state == RUNNING:
        ms = clock.tick(60)
        play_time += ms / 1000.0

        # handle player inputs
        action = controls.process_events()
        controls.update_keys()

        # debug actions
        if action == "shoot":
            player1.shoot()
        elif action == "spawn_item":
            DroppedPerk(ab, player1.rect.move(30, 0).center)
        elif action == "spawn_gun":
            player1.add_weapon(Gun((0, 0)))
        elif action == "swap_gun":
            player1.swap_weapons()
        elif action == "host":
            if not is_host:
                init_host()
        elif action == "connect":
            if not is_host:
                init_net()
        elif action == "test_sock":
            client.send("hello")

        # update cursor
        cursor_pos_x, cursor_pos_y = pygame.mouse.get_pos()
        cursor.move((cursor_pos_x / options.scale(), cursor_pos_y / options.scale()),
                    controls.click)

        # update cursor text
        cursor.set_hover_text(examine.find_examine_text(cursor.point()))

        # update window title to show frame rate
        pygame.display.set_caption("FPS: {0:.2f}".format(clock.get_fps()))

        # flip player to face cursor
        player1.flip(cursor.point()[0] < camera.apply(player1.rect).centerx)

        perk_collide(player1)

        # render screen
        render.draw()

        # update the camera to the player's position
        camera.follow(player1.rect)


def host_loop():
    clock = pygame.time.Clock()

    tick_count = 0

    while is_host:
        clock.tick(60)
        tick_count += 1

        # update velocities
        __init__.sync_velocities()

        if tick_count % 20 == 0:
            # update positions
            __init__.sync_positions()


def net_loop():
    while True:
        if is_host:
            read_sockets, _, _ = select.select(host.clients, [], [])
        else:
            read_sockets = client.client_socket,

        for sock in read_sockets:
            data = sock.recv(4096).decode()
            print(data)
            net_update(common.parse_packet_string(data))


def net_update(data):
    if data["op"] == common.OP_ENTITY_MOVE:
        if not is_host:
            ent = __init__.entity_from_id(data["eid"])
            if ent is None:
                print("added net player 0")
                __init__.add_net_entity(data["eid"], Player("arnold", (data["x"], data["y"])))
            else:
                print("updated player")
                ent.rect.topleft = data["x"], data["y"]
    elif data["op"] == common.OP_ENTITY_VEL:
        if not is_host:
            __init__.entity_from_id(data["eid"]).velocity = util.Vector(data["vx"], data["vy"])
