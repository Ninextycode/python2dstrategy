import pygame

import game_data as g_d
import game_logic as g_l

g_l.initialise()

while not g_d.done:
    g_l.iteration()

    if g_d.image_mode:
        pygame.display.update()

    if g_d.graphs_mode:
        g_d.delta_time = 100
    else:
        g_d.delta_time = g_d.clock.tick(20)

if g_d.image_mode:
    pygame.quit()
