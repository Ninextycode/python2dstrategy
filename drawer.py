import game_data as g_d


def draw_game_surface():
    g_d.screen.fill((255, 255, 255))
    for soldier in g_d.soldiers:
        soldier.draw(g_d.screen)
    for bullet in g_d.bullets:
        bullet.draw(g_d.screen)
    for bullet in g_d.bullets:
        bullet.draw(g_d.screen)


def draw_graphs():
    pass