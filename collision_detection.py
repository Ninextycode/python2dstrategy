import numpy as np

import game_data as g_d


def magnitude(vector):
    return np.sqrt(vector[0]**2 + vector[1]**2)


def soldiers_the_object_touches(obj):
    soldiers = []
    for soldier in g_d.soldiers:
        if soldier is not obj and \
                        magnitude(soldier.position - obj.position) <= (soldier.radius + obj.radius):
            soldiers.append(soldier)
    return soldiers


def is_position_in_forest(position):
    x_f = np.round(position[0]).astype(int) // g_d.forest_grid_cell_side
    y_f = np.round(position[1]).astype(int) // g_d.forest_grid_cell_side

    return x_f >= 0 and y_f >= 0 and x_f < len(g_d.forest_grid) and y_f < len(g_d.forest_grid[0]) and\
        g_d.forest_grid[x_f][y_f]


def soldier_in_field_view(solder_looking):
    objects_in_view_field = []
    for soldier in g_d.soldiers:
        if soldier is not solder_looking and \
                soldier.team != solder_looking.team and \
                    magnitude(soldier.position - solder_looking.position) < \
                        (soldier.radius + solder_looking.field_of_view_radius):
            objects_in_view_field.append(soldier)

    return get_closest_among_given(solder_looking.position, objects_in_view_field)


def set_soldiers_to_closest_enemies():
    g_d.closest_reachable_soldiers_map = {}
    for soldier in g_d.soldiers:
        enemy = get_closest_reachable_enemy(soldier)
        g_d.closest_reachable_soldiers_map[soldier] = enemy
        if g_d.closest_reachable_soldiers_map.get(enemy, None) is None:
            g_d.closest_reachable_soldiers_map[enemy] = soldier
            #   Assign closest enemy to recieved soldier as initial soldier,
            #   if nothing was assigned to enemy before.
            #  Should fix one bug


def get_closest_reachable_enemy(given_soldier):
    closest_enemy = None
    closest_distance = None
    for soldier in g_d.soldiers:
        if soldier.team != given_soldier.team:
            local_distance = magnitude(soldier.position - given_soldier.position)
            if local_distance < (soldier.radius + soldier.field_of_view_radius) and\
                    (closest_distance is None or closest_distance < local_distance):
                closest_distance = local_distance
                closest_enemy = soldier

    return closest_enemy


def get_closest_among_given(position, objects):
    if len(objects) == 0:
        return None
    closest = objects[0]
    position = np.asarray(position)

    closest_dist = magnitude(position - closest.position)
    for object in objects[1:]:
        local_dist =  magnitude(object.position - position)
        if local_dist < closest_dist:
            closest_dist = local_dist
            closest = object

    return closest
