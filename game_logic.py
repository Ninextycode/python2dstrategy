import numpy as np
import pygame
import sys


import game_objects as g_o
import game_data as g_d
import drawer
import forest_generator as f_g
import artificial_intelligence as a_i
import collision_detection as c_d


def initialise():
    if g_d.image_mode:
        initialise_pygame()

    initialize_2_teams()

    if g_d.graphs_mode:
        drawer.initialise_matplotlib()


def initialise_test():
    f_g.generate_forest()

    generate_squad(g_o.Soldier.radius, g_o.Soldier.radius, 3, 10, 0, g_d.size / 2)
    generate_squad(g_d.size[0] / 2, g_d.size[0] / 2, 3, 10, 1, g_d.size / 2 + np.asarray([0, 25]))


def initialize_2_teams():
    f_g.generate_forest()
    squad_size = np.asarray((16, 2))

    offset = squad_size * g_o.Soldier.diameter
    generate_squad(g_d.size - offset, squad_size, 1, g_d.size / 2)

    generate_squad((0, 0), squad_size, 0, g_d.size / 2)


def generate_squad(top, shape, team, target=None):
    for x_l in range(shape[0]):
        for y_l in range(shape[1]):
            offset = np.asarray([x_l * g_o.Soldier.diameter, y_l * g_o.Soldier.diameter]) + g_o.Soldier.radius
            s = g_o.Soldier(np.asarray(top) + offset, team)
            if target is not None:
                s.set_target(np.asarray(target) + offset)


def initialise_pygame():
    pygame.init()
    g_d.screen = pygame.display.set_mode(g_d.size)
    pygame.display.set_caption(g_d.title)
    g_d.clock = pygame.time.Clock()


def iteration():
    c_d.set_soldiers_to_closest_enemies()
    if g_d.image_mode:
        check_events()
    update_objects()
    if g_d.image_mode:
        drawer.draw_game_surface()
    if g_d.graphs_mode:
        drawer.draw_graphs()
    a_i.set_targets_from_all_ais()


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
            sys.exit()
