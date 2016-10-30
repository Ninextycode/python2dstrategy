import numpy as np
import game_data as g_d
import game_objects as g_o

import neural_networking as n_n
import collision_detection as c_d


class AI:
    n_hidden_layers = 2

    def __init__(self, team, net = None):
        self.last_targeting_data = np.zeros(n_n.get_field_size_for_soldiers())
        self.team = team

        if net is not None:
            self.net = net
        else:
            f_m = n_n.get_forest_matrix()
            s_ms = n_n.get_teams_matrices()

            self.net = n_n.NeuralNet(
                n_n.get_input_length(),
                n_n.get_output_length(),
                (n_n.get_input_length()) // 3 * 4,
                AI.n_hidden_layers)

            self.net.set_random_theta()

    def set_targets_to_soldiers(self):
        targeting_data = self.net(self.get_input())

        self.last_targeting_data = targeting_data.reshape(n_n.get_field_size_for_soldiers())

        my_soldiers = [soldier for soldier in g_d.soldiers if soldier.team == self.team]
        indexes = targeting_data.argsort()[::-1][:len(my_soldiers)]
        field_size = n_n.get_field_size_for_soldiers()
        shift = g_o.Soldier.radius

        for i in range(len(indexes)):
            x = indexes[i] % field_size[1]
            y = indexes[i] // field_size[1]
            target = np.asarray((x, y)) * g_o.Soldier.diameter + shift

            soldier = c_d.get_closest_among_given(target, my_soldiers)
            soldier.set_target(target)
            my_soldiers.remove(soldier)

    def get_input(self):
        forest = n_n.get_forest_matrix()
        teams_matrices = n_n.get_teams_matrices()
        my_team_matrix = teams_matrices[self.team]
        input_to_concat = [forest.reshape(-1), my_team_matrix.reshape(-1)]
        for i in range(len(teams_matrices)):
            if i != self.team:
                input_to_concat.append(teams_matrices[i].reshape(-1))

        return np.concatenate(input_to_concat, axis=0)


def set_targets_from_all_ais():
    for ai in g_d.AIs:
        ai.set_targets_to_soldiers()