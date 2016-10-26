import numpy as np

import game_data as g_d


def magnitude(vector):
    return np.sqrt(vector[0]**2 + vector[1]**2)


def soldier_the_object_touches(obj):
    for soldier in g_d.soldiers:
        if soldier is not obj and \
                        magnitude(soldier.position - obj.position) <= (soldier.radius + obj.radius):
            return soldier
    return None


def is_position_in_forest(position):
    return g_d.forest_grid[position[0] // g_d.forest_grid_cell_side][position[1] // g_d.forest_grid_cell_side]