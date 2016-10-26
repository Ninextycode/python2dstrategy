from random import random

import game_data as g_d
import game_objects as g_o


def generate_forest(frequency, n_clean):
    g_d.forest_grid_cell_side = (g_o.Tree.radius * 2)
    width = g_d.size[0] // g_d.forest_grid_cell_side
    height = g_d.size[1] // g_d.forest_grid_cell_side
    g_d.forest_grid = [[False for y in range(height)] for x in range(width)]
    fill_random(frequency)
    for i in range(n_clean):
        clean()


def fill_random(frequency):
    for x in range(len(g_d.forest_grid)):
        for y in range(len(g_d.forest_grid[0])):
            g_d.forest_grid[x][y] = frequency > random()


def clean():
    for x in range(len(g_d.forest_grid)):
        for y in range(len(g_d.forest_grid[0])):
            if calculate_neighbours(x,y) > 5:
                g_d.forest_grid[x][y] = True
            if calculate_neighbours(x, y) < 5:
                g_d.forest_grid[x][y] = False


def calculate_neighbours(x, y):
    n = 0
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if len(g_d.forest_grid) > i and i >= 0 and \
                    len(g_d.forest_grid[i]) > j and j >= 0 and \
                    g_d.forest_grid[i][j]:
                n += 1
    return n
