import numpy as np
import pygame

import game_objects as g_o
import game_data as g_d
import drawer
import forest_generator as f_g


def initialise():
    initialise_pygame()
    f_g.generate_forest(0.55, 5)
    for x in range(len(g_d.forest_grid)):
        for y in range(len(g_d.forest_grid[0])):
            g_o.Tree(
                np.asarray((x*g_d.forest_grid_cell_side, y * g_d.forest_grid_cell_side) + g_d.forest_grid_cell_side/2))


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
        soldier.update()
    for bullet in g_d.bullets:
        bullet.update()


def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            g_d.done = True





