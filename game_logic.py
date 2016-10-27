import numpy as np
import pygame

import game_objects as g_o
import game_data as g_d
import drawer
import forest_generator as f_g


def initialise():
    initialise_pygame()
    f_g.generate_forest(0.55, 4)

    s0 = g_o.Soldier((g_d.size[0]//2,g_d.size[1]//2), 0)
    s1 = g_o.Soldier((g_d.size[0]//2,g_d.size[1]//2), 1)

    s0.set_target(g_d.size)
    s1.set_target((0,0))


def initialise_pygame():
    pygame.init()
    g_d.screen = pygame.display.set_mode(g_d.size)
    pygame.display.set_caption(g_d.title)
    g_d.clock = pygame.time.Clock()


def iteration():
    check_events()
    update_objects()
    drawer.draw_game_surface()


def update_objects():
    for soldier in g_d.soldiers:
        soldier.update(g_d.delta_time / 1000)
    for bullet in g_d.bullets:
        bullet.update(g_d.delta_time / 1000)


def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            g_d.done = True





