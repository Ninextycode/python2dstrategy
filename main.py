import pygame

import game_data as g_d
import game_logic as g_l


def compete():
    g_l.initialise()

    while not g_d.done:
        g_l.iteration()

        if g_d.image_mode:
            pygame.display.update()

        g_d.delta_time = 100
        g_d.time_left -= g_d.delta_time

        print(g_d.time_left / 1000, g_d.team_size)

        g_d.done = g_d.time_left <= 0 or g_d.team_size[0] <= 0 or  g_d.team_size[1] <=0

    if g_d.image_mode:
        pygame.quit()

    return -1 if g_d.team_size[0] == g_d.team_size[1] else 10 if g_d.team_size[0] > g_d.team_size[1] else 1

compete()