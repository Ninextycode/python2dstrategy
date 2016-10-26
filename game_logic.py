import numpy as np

import game_data as g_d
import game_objects as g_o
import forest_generator as f_g

def initialise():
    f_g.generate_forest()


def magnitude(vector):
    return np.sqrt(vector[0]^2 + vector[1]^2)


def soldier_the_oject_touches(object):
    for soldier in g_d.soldiers:
        if magnitude(soldier.position - object.position) <= (soldier.radius + object.radius):
            return soldier
    return None
