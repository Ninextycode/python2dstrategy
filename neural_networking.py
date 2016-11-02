import numpy as np
np.set_printoptions(threshold=np.inf)
import numpy.random as rand

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

field_size_for_forest = None
def get_field_size_for_forest():
    global field_size_for_forest
    if field_size_for_forest is None:
        xysize = np.ceil(g_d.size / g_o.Tree.diameter).astype(int)
        field_size_for_soldiers = np.asarray((xysize[1], xysize[0]))
    return field_size_for_soldiers


def get_input_length():
    field_size = get_field_size_for_soldiers()
    forest_size = get_field_size_for_forest()
    return field_size[0] * field_size[1] * g_d.n_teams +  forest_size[0] *  forest_size[1]


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
        self.thetas = []
        start = 0
        for i in range(len(self.layers_sizes)-1):
            end = start + (self.layers_sizes[i] + 1) * self.layers_sizes[i + 1]
            self.thetas.append(theta_row[start:end].reshape(self.layers_sizes[i] + 1, self.layers_sizes[i + 1]))
            start = end

    def set_random_theta(self, max_abs_value = 1):
        theta = self.generate_random_raw_theta(max_abs_value)
        self.set_theta(theta)

    def generate_random_raw_theta(self, epsilon):
        length = 0
        for i in range(len(self.layers_sizes) - 1):
            length += (self.layers_sizes[i] + 1) * self.layers_sizes[i + 1]
        return np.random.random(length)* 2 * epsilon - epsilon

    def __call__(self, data):
        for theta in self.thetas:
            data = np.append(data, 0)
            data = data @ theta
            data = NeuralNet.sigmoid(data)
        return data

    def get_theta(self):
        return np.concatenate([theta.reshape(-1) for theta in self.thetas])

def mutate(theta, rate, max_change):
    for i in range(len(theta)):
        if rate > rand.random():
            theta[i] += rand.random() * max_change * 2 - max_change


def cross(theat_1, theta_2, rate):
    for i in range(len(theat_1)):
        if rate > rand.random():
            theat_1[i], theta_2[i] = theta_2[i], theat_1[i]