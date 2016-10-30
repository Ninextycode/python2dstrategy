import numpy as np

title = "WAR"

screen = None

clock = None
delta_time = 0

size = np.asarray([800, 600])

forest_grid = []
forest_grid_cell_side = 0

soldiers = []
bullets = []
trees = []
object_to_delete = []

teams = [0, 1]
team_size = [0 for t in teams]

image_mode = False
graphs_mode = True
use_ai = True
AIs = []

done = False
match_time_ms = 60 * 3 * 1000
time_left = match_time_ms
