import matplotlib.pyplot as plt
import sys


import game_data as g_d
import neural_networking as n_n


graphs_figure = None
subplots_teams = []
subplot_forest = None


def initialise_matplotlib():
    plt.ion()

    global graphs_figure, subplot_forest
    graphs_figure = plt.figure()
    subplot_forest = graphs_figure.add_subplot(311)
    subplots_teams.append(graphs_figure.add_subplot(312))
    subplots_teams.append(graphs_figure.add_subplot(313))

    subplot_forest.imshow(n_n.get_forest_matrix(), cmap="Greens", interpolation="nearest")
    subplot_forest.set_xticklabels([])
    subplot_forest.set_yticklabels([])

    for subplot in subplots_teams:
        subplot.set_xticklabels([])
        subplot.set_yticklabels([])

    plt.draw()
    graphs_figure.canvas.mpl_connect('close_event', handle_close)

def draw_game_surface():
    g_d.screen.fill((220, 220, 220))

    for tree in g_d.trees:
        tree.draw(g_d.screen)
    for soldier in g_d.soldiers:
        soldier.draw(g_d.screen)
    for bullet in g_d.bullets:
        bullet.draw(g_d.screen)


team_cmaps = ["Blues", "Reds"]
fitted = False


def draw_graphs():
    global subplots_teams
    teams_mats = n_n.get_teams_matrix()
    for i in range(len(teams_mats)):
        subplots_teams[i].imshow(teams_mats[i], cmap = team_cmaps[i], interpolation = "nearest" )

    graphs_figure.canvas.flush_events()


def handle_close(evt):
    sys.exit()

