import numpy as np

import game_data as g_d
import game_objects as g_o

forest_matrix = None



def get_forest_matrix():
    global forest_matrix
    if forest_matrix is None:
        forest_matrix = np.zeros((len(g_d.forest_grid[0]), len(g_d.forest_grid)))
        for x in range(len(g_d.forest_grid)):
            for y in range(len(g_d.forest_grid[0])):
                if g_d.forest_grid[x][y]:
                    forest_matrix[y][x] = 1 # rows - cols instead of x and y

    return  forest_matrix


def get_teams_matrix():
    mats = []
    size = g_d.size // (g_o.Soldier.radius * 2)+ 1
    rcsize = (size[1], size[0])
    for team in g_d.teams:
        mat = np.zeros(rcsize)
        mats.append(mat)

    for soldier in g_d.soldiers:
        xypos = tuple( (soldier.position // (g_o.Soldier.radius * 2)).astype(int))
        rcpos = (xypos[1], xypos[0])
        mats[soldier.team][rcpos] = 1

    return mats