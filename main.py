import pygame

import game_data as g_d
import game_logic as g_l

g_l.initialise()

while not g_d.done:
    g_l.iteration()

    pygame.display.update()
    g_d.delta_time = g_d.clock.tick(20)

# close the window and quit
pygame.quit()
