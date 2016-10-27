import game_data as g_d


def draw_game_surface():
    g_d.screen.fill((220, 220, 220))

    for tree in g_d.trees:
        tree.draw(g_d.screen)
    for soldier in g_d.soldiers:
        soldier.draw(g_d.screen)
    for bullet in g_d.bullets:
        bullet.draw(g_d.screen)


def draw_graphs():
    pass