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

teams = [0,1]

image_mode = True
graphs_mode = True

done = False