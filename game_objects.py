import pygame
import numpy as np
from random import random

import game_data as g_d
import collision_detection as c_d


class Soldier:
    radius = 10
    field_of_view_radius = 50

    in_forest_speed = 15
    in_forest_evade_chance = 0.6
    default_life_level = 100
    out_forest_speed = 50
    out_forest_evade_chance = 0.1

    colors = [(0, 0, 0x77), (0x77, 0, 0)]

    def __init__(self, position, team):
        self.speed = 0
        self.evade_chance = 0
        self.position = np.asarray(position, dtype=float)
        self.target = self.position

        self.life = Soldier.default_life_level
        self.team = team
        self.color = Soldier.colors[team]

        self.set_state_by_forest()

        g_d.soldiers.append(self)

    def set_target(self, target):
        self.target = np.asarray(target, dtype=float)

    def update(self, delta_time):
        direction = self.target - self.position
        length = np.sqrt(direction[0]**2 + direction[1]**2)

        if length < self.radius/2:
            return

        direction = direction / length
        velocity = direction * self.speed * delta_time
        print(self.position)
        print(velocity)

        self.dx(velocity[0])
        self.dy(velocity[1])
        print(self.position)

    def dx(self, d):
        self.position[0] += d
        self.check_move()

    def dy(self, d):
        self.position[1] += d
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
        self.color = (Soldier.colors[self.team][0]*2, Soldier.colors[self.team][1]*2, Soldier.colors[self.team][2]*2)

    def out_forest(self):
        self.speed = Soldier.out_forest_speed
        self.evade_chance = Soldier.out_forest_evade_chance
        self.color = Soldier.colors[self.team]

    def hit(self, damage):
        if self.evade_chance < random():
            self.life -= damage
            if self.life <= 0:
                g_d.soldiers.remove(self)

    def is_in_forest(self):
        return c_d.is_position_in_forest(self.position)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, np.round(self.position).astype(int), Soldier.radius)


class Bullet:
    speed = 60
    radius = 1
    color = (0, 0, 0)

    def __init__(self, position, target):
        self.position = np.asarray(position, dtype=float)
        direction = np.asarray(target, dtype=float) - self.position
        direction = direction / np.sqrt(direction[0]**2 + direction[1]**2)
        self.velocity = direction * Bullet.speed

        g_d.bullets.append(self)

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

    def draw(self, surface):
        pygame.draw.circle(surface, Bullet.color, np.round(self.position).astype(int), Bullet.radius)


class Tree:
    radius = 8
    color = (0, 0xff, 0)

    def __init__(self, position):
        self.position = np.asarray(position, dtype=float)

        g_d.trees.append(self)

    def draw(self, surface):
        pygame.draw.circle(surface, Tree.color, np.round(self.position).astype(int), Tree.radius)

