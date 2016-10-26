import pygame
import numpy as np
from random import random

import game_logic as g_l
import game_data as g_d
import collision_detection as c_d


class Soldier:
    radius = 5
    field_of_view_radius = 50

    in_forest_speed = 2
    in_forest_evade_chance = 0.6
    default_life_level = 100
    out_forest_speed = 10
    out_forest_evade_chance = 0.1

    colors = [(0, 0, 0xff), (0xff, 0, 0)]

    def __init__(self, position, team):
        g_d.soldiers.append(self)

        self.speed = 0
        self.evade_chance = 0
        self.position = np.asarray(position)
        self.target = self.position

        self.life = Soldier.default_life_level
        self.set_state_by_forest()
        self.team = team
        self.color = Soldier.colors[team]

    def update(self, delta_time):
        direction = self.target - self.position
        direction /= np.sqrt(direction[0]**2 + direction[1]**2)
        velocity = direction * Bullet.speed
        self.dx(velocity[0] * delta_time)
        self.dy(velocity[1] * delta_time)

    def set_target(self, target):
        self.target = target

    def dx(self, dx):
        self.position[0] += dx
        self.check_move()

    def dy(self, dx):
        self.position[0] += dx
        self.check_move()

    def check_move(self):
        self.set_state_by_forest()
        # TODO shooting

    def set_state_by_forest(self):
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

    def hit(self, damage):
        if self.evade_chance < random():
            self.life -= damage
            if self.life <= 0:
                g_d.soldiers.remove(self)

    def is_in_forest(self):
        return c_d.is_position_in_forest(self.position)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, Soldier.radius)


class Bullet:
    speed = 60
    radius = 1

    def __init__(self, position, target):
        g_d.bullets.append(self)

        self.position = np.asarray(position)
        direction = np.asarray(target) - self.position
        direction /= np.sqrt(direction[0]**2 + direction[1]**2)
        self.velocity = direction * Bullet.speed

    def update(self, delta_time):
        self.dx(self.velocity[0]*delta_time)
        self.dy(self.velocity[1]*delta_time)

    def dx(self, dx):
        self.position[0] += dx
        self.check_collision()

    def dy(self, dx):
        self.position[0] += dx
        self.check_collision()

    def check_collision(self):
        hit_soldier = c_d.soldier_the_object_touches(self)
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

