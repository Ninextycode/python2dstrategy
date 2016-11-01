import numpy as np


title = "WAR"

size = np.asarray([400, 300])

n_teams = 2
forest_grid_cell_side = 10


forest_rate = 0.53
match_time_ms = 60 * 3 * 1000

image_mode = True
graphs_mode = False

screen = None
clock = None
delta_time = 0

soldiers = []
bullets = []
trees = []
object_to_delete = []
forest_grid = []
AIs = []
team_size = [0, 0]

done = False
time_left = match_time_ms


def clear():
    global screen, clock, delta_time, soldiers, bullets, trees, object_to_delete, forest_grid, AIs, team_size, done,\
        time_left

    screen = None
    clock = None
    delta_time = 0

    soldiers = []
    bullets = []
    trees = []
    object_to_delete = []
    forest_grid = []
    AIs = []
    team_size = [0, 0]

    done = False
    time_left = match_time_ms
