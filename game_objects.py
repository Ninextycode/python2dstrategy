import pygame
import numpy as np
from random import random

import game_logic as g_l
import game_data as g_d

class Soldier:

    radius = 5
    in_forest_speed = 2
    in_forest_evade_chance = 0.6
    default_life_level = 100
    out_forest_speed = 10
    out_forest_evade_chance = 0.1

    def __init__(self, position):
        self.speed = 0
        self.evade_chance = 0
        self.position = np.asarray(position)
        self.life = Soldier.default_life_level

        g_d.soldiers.append(self)

        if self.is_in_forest():
            self.in_forest()
        else:
            self.out_forest()

    def in_forest(self):
        self.speed = Soldier.in_forest_speed
        self.evade_chance = Soldier.in_forest_evade_chance

    def out_forest(self):
        self.speed = Soldier.out_forest_speed
        self.evade_chance = Soldier.out_forest_evade_chance

    def is_in_forest(self):
        #TODO
        return False

    def hit(self, damage):
        if self.evade_chance < random():
            self.life -= damage
            if self.life <= 0:
                g_d.soldiers.remove(self)


class Bullet:
    speed = 60
    radius = 1

    def __init__(self, position, target):
        g_d.bullets.append(self)

        self.position = np.asarray(position)
        direction = np.asarray(target) - self.position
        direction /= np.sqrt(direction[0]^2 + direction[1]^2)
        self.velocity = direction * Bullet.speed

    def update(self):
        self.dx(self.velocity[0])
        self.dy(self.velocity[1])

    def dx(self, dx):
        self.position[0] += dx
        self.check_collision()

    def dy(self, dx):
        self.position[0] += dx
        self.check_collision()

    def check_collision(self):
        hit_soldier = g_l.soldier_the_oject_touches(self)
        if hit_soldier is not None:
            g_d.bullets.remove(self)
            hit_soldier.hit()


class Tree:
    radius = 5
    color = (0, 0xff, 0)

    def __init__(self, position):
        g_d.trees.append(self)
        self.position = position

    def draw(self, surface):
        pygame.draw.circle(surface, Tree.color, self.position, Tree.radius)

