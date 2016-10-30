import numpy as np
np.set_printoptions(threshold=np.inf)


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


def get_teams_matrices():
    mats = []
    rows_columns_size = get_field_size_for_soldiers()
    for team in range(g_d.n_teams):
        mat = np.zeros(rows_columns_size)
        mats.append(mat)


    for soldier in g_d.soldiers:
        xypos = tuple((soldier.position // g_o.Soldier.diameter).astype(int))
        rcpos = (xypos[1], xypos[0])
        mats[soldier.team][rcpos] = 1

    return mats


field_size_for_soldiers = None
def get_field_size_for_soldiers():
    global field_size_for_soldiers
    if field_size_for_soldiers is None:
        xysize = np.ceil(g_d.size / g_o.Soldier.diameter).astype(int)
        field_size_for_soldiers = np.asarray((xysize[1], xysize[0]))
    return field_size_for_soldiers


def get_input_length():
    field_size = get_field_size_for_soldiers()
    return field_size[0] * field_size[1] * g_d.n_teams +  len(g_d.forest_grid) *  len(g_d.forest_grid[0])


def get_output_length():
    field_size = get_field_size_for_soldiers()
    return field_size[0] * field_size[1]

class NeuralNet:
    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    def __init__(self, input_length, output_length, hidden_length, n_hidden, theta_row = None):
        self.layers_sizes = [input_length]

        self.layers_sizes.extend([hidden_length for i in range(n_hidden)])
        self.layers_sizes.append(output_length)

        self.thetas = []

        if theta_row is not None:
            self.set_theta(theta_row)

    def set_theta(self, theta_row):
        start = 0
        for i in range(len(self.layers_sizes)-1):
            end = start + (self.layers_sizes[i] + 1) * self.layers_sizes[i + 1]
            self.thetas.append(theta_row[start:end].reshape(self.layers_sizes[i] + 1, self.layers_sizes[i + 1]))
            start = end

    def set_random_theta(self):
        theta = self.generate_random_raw_theta(1)
        self.set_theta(theta)

    def generate_random_raw_theta(self, epsilon):
        length = 0
        for i in range(len(self.layers_sizes) - 1):
            length += (self.layers_sizes[i] + 1) * self.layers_sizes[i + 1]
        return np.random.random(length)* 2 * epsilon - epsilon

    def __call__(self, data):
        i = 0
        for theta in self.thetas:
            i += 1
            data = np.append(data, 0)
            data = data @ theta
            data = NeuralNet.sigmoid(data)
        return data
