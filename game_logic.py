import numpy as np
import pygame
import sys


import game_objects as g_o
import game_data as g_d
import drawer
import forest_generator as f_g
import ai


def initialise():
    if g_d.image_mode:
        initialise_pygame()

    initialize_2_teams()

    if g_d.graphs_mode:
        drawer.initialise_matplotlib()

    if g_d.use_ai:
        initialise_ai()


def initialise_test():
    f_g.generate_forest(0.55, 4)

    generate_squad(g_o.Soldier.radius, g_o.Soldier.radius, 3, 10, 0, g_d.size / 2)
    generate_squad(g_d.size[0] / 2, g_d.size[0] / 2, 3, 10, 1, g_d.size / 2 + np.asarray([0, 25]))


def initialize_2_teams():
    f_g.generate_forest(0.0, 4)
    squad_size = np.asarray((16, 2))

    generate_squad((0, 0), squad_size, g_d.teams[0])
    offset = squad_size * g_o.Soldier.radius * 2
    generate_squad(g_d.size - offset, squad_size, g_d.teams[1])


def generate_squad(top, shape, team, target = None):
    soldier_d = g_o.Soldier.radius * 2
    for x_l in range(shape[0]):
        for y_l in range(shape[1]):
            offset = np.asarray([x_l * soldier_d, y_l * soldier_d]) + g_o.Soldier.radius
            s = g_o.Soldier(np.asarray(top) + offset, team)
            if target is not None:
                s.set_target(np.asarray(target) + offset)


def initialise_pygame():
    pygame.init()
    g_d.screen = pygame.display.set_mode(g_d.size)
    pygame.display.set_caption(g_d.title)
    g_d.clock = pygame.time.Clock()


def initialise_ai():
    for team in g_d.teams:
        g_d.AIs.append(ai.AI(team))


def iteration():
    if g_d.image_mode:
        check_events()
    update_objects()
    if g_d.image_mode:
        drawer.draw_game_surface()
    if g_d.graphs_mode:
        drawer.draw_graphs()
    if g_d.use_ai:
        ai.set_targets_from_all_ais()

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





