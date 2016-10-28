import numpy as np
import pygame

import game_objects as g_o
import game_data as g_d
import drawer
import forest_generator as f_g


def initialise():
    initialise_pygame()
    initialise_test()

def initialise_test():
    f_g.generate_forest(0.55, 4)

    generate_squad(g_o.Soldier.radius, g_o.Soldier.radius, 3, 10, 0, g_d.size / 2)
    generate_squad(g_d.size[0] / 2, g_d.size[0] / 2, 3, 10, 1, g_d.size / 2 + np.asarray([0, 25]))

def generate_squad(x, y, rows, cols, team, target = None):
    for x_l in range(cols):
        for y_l in range(rows):
            offset = np.asarray([x_l * (g_o.Soldier.radius) * 2, y_l * (g_o.Soldier.radius) * 2])
            s = g_o.Soldier((x + x_l * (g_o.Soldier.radius) * 2, y + y_l * (g_o.Soldier.radius) * 2), team)
            if target is not None:
                s.set_target(np.asarray(target) + offset)

def initialise_pygame():
    pygame.init()
    g_d.screen = pygame.display.set_mode(g_d.size)
    pygame.display.set_caption(g_d.title)
    g_d.clock = pygame.time.Clock()


def iteration():
    check_events()
    update_objects()
    drawer.draw_game_surface()
    drawer.draw_graphs()

def update_objects():
    for soldier in g_d.soldiers:
        soldier.update(g_d.delta_time / 1000)
    for bullet in g_d.bullets:
        bullet.update(g_d.delta_time / 1000)

    for obj in g_d.object_to_delete:
        if obj in g_d.bullets:
            g_d.bullets.remove(obj)
        if obj in g_d.soldiers:
            g_d.soldiers.remove(obj)

    g_d.object_to_delete = []


def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            g_d.done = True





