import pygame

import game_data as g_d
import game_logic as g_l
import neural_networking as n_n
import artificial_intelligence as a_i


def compete(ais = None):
    g_d.clear()
    g_l.initialise()
    ais[0].team = 0
    ais[1].team = 1

    for ai in ais:
        g_d.AIs.append(ai)

    print_counter = 0
    while not g_d.done:
        g_l.iteration()

        if g_d.image_mode:
            pygame.display.update()

        g_d.delta_time = 100
        g_d.time_left -= g_d.delta_time

        print_counter += 1
        if print_counter >= 5:
            print_counter = 0
            print(g_d.time_left / 1000, g_d.team_size)

        g_d.done = not (g_d.time_left > 0 and g_d.team_size[0] > 0 and g_d.team_size[1] > 0)

    if g_d.image_mode:
        pygame.quit()

    return -1 if g_d.team_size[0] == g_d.team_size[1] else 0 if g_d.team_size[0] > g_d.team_size[1] else 1


def initialise_random_nets_for_given_ais(ais):
    for ai in ais:
        ai.net.set_random_theta(max_abs_value=0.2)


def start_tournament():
    n_participants = 2
    ais = [a_i.AI() for i in range(n_participants)]
    initialise_random_nets_for_given_ais(ais)
    result = tournament(ais)
    print(result)


def tournament(ais):
    ai_score = [(ai, 0) for ai in ais]
    for i in range(len(ai_score)):
        for j in range(len(ai_score)):
            if i != j:
                result = compete((ai_score[i][0], ai_score[j][0]))
                if result == -1:
                    ai_score[i][1] += 1
                    ai_score[j][1] += 1
                elif result == 0:
                    ai_score[i][1] += 3
                    ai_score[j][1] += 0
                elif result == 1:
                    ai_score[i][1] += 0
                    ai_score[j][1] += 3

    return ai_score

start_tournament()