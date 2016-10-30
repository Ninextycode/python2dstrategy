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
    x_f = np.round(position[0]).astype(int) // g_d.forest_grid_cell_side
    y_f = np.round(position[1]).astype(int) // g_d.forest_grid_cell_side

    return x_f >= 0 and y_f >= 0 and x_f < len(g_d.forest_grid) and y_f < len(g_d.forest_grid[0]) and\
        g_d.forest_grid[x_f][y_f]


def soldier_in_field_view(solder_looking):
    for soldier in g_d.soldiers:
        if soldier is not solder_looking and \
                soldier.team != solder_looking.team and \
                0 < \
                    magnitude(soldier.position - solder_looking.position) <= \
                        (soldier.radius + solder_looking.field_of_view_radius):
            return soldier
    return None


def get_closest_among_given(position, objects):
    closest = objects[0]
    position = np.asarray(position)

    closest_dist = magnitude(position - closest.position)
    for object in objects[1:]:
        local_dist =  magnitude(object.position - position)
        if local_dist < closest_dist:
            closest_dist = local_dist
            closest = object
    return closest
