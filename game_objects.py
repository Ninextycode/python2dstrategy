import pygame
import numpy as np
from random import random

import game_data as g_d
import collision_detection as c_d


class Soldier:
    radius = 5
    field_of_view_radius = 80

    in_forest_speed = 15
    in_forest_evade_chance = 0.60
    default_life_level = 100
    out_forest_speed = 50
    out_forest_evade_chance = 0.10

    colors = [(0, 0, 0x77), (0x77, 0, 0)]

    general_reload_time = 0.5

    def __init__(self, position, team):
        self.speed = 0
        self.evade_chance = 0
        self.position = np.asarray(position, dtype=float)
        self.target = self.position
        self.life = Soldier.default_life_level
        self.team = team
        self.color = Soldier.colors[team]

        self.set_state_by_forest()
        self.time_to_reload = 1
        g_d.soldiers.append(self)

    def set_target(self, target):
        self.target = np.asarray(target, dtype=float)

    def update(self, delta_time):
        if not self.reloaded():
            self.continue_reload(delta_time)
        else:
            self.try_shoot()

        direction = self.target - self.position
        length = np.sqrt(direction[0]**2 + direction[1]**2)

        if length < self.radius/2:
            return

        direction = direction / length
        velocity = direction * self.speed * delta_time

        self.dx(velocity[0])
        self.dy(velocity[1])

    def continue_reload(self, delta_time):
        self.time_to_reload -= delta_time

    def dx(self, d):
        self.position[0] += d
        self.check_move()

    def dy(self, d):
        self.position[1] += d
        self.check_move()

    def check_move(self):
        self.set_state_by_forest()

    def set_state_by_forest(self):
        if self.is_in_forest():
            self.in_forest()
        else:
            self.out_forest()

    def in_forest(self):
        self.speed = Soldier.in_forest_speed
        self.evade_chance = Soldier.in_forest_evade_chance
        self.color = self.color = Soldier.colors[self.team]

    def out_forest(self):
        self.speed = Soldier.out_forest_speed
        self.evade_chance = Soldier.out_forest_evade_chance
        (Soldier.colors[self.team][0] * 2, Soldier.colors[self.team][1] * 2, Soldier.colors[self.team][2] * 2)


    def try_shoot(self):
        soldier_in_field_view = c_d.soldier_in_field_view(self)
        if soldier_in_field_view is not None and soldier_in_field_view.team != self.team and self.reloaded():
            self.shoot(soldier_in_field_view.position)

    def reloaded(self):
        return self.time_to_reload <= 0

    def shoot(self, target):
        self.time_to_reload = Soldier.general_reload_time
        direction = target - self.position
        if direction[0] == 0 and direction[1] == 0:
            return

        direction = direction / np.sqrt(direction[0]**2 + direction[1]**2)
        Bullet(self.position + direction * (Bullet.radius + self.radius), target, self.team)

    def hit(self, damage):
        if self.evade_chance < random():
            self.life -= damage
            if self.life <= 0:
                g_d.object_to_delete.append(self)

    def is_in_forest(self):
        return c_d.is_position_in_forest(self.position)

    def draw_with_field_view(self, surface):
        self.draw(surface)
        pygame.draw.circle(surface, (0, 0xff, 0), np.round(self.position).astype(int), Soldier.field_of_view_radius, 1)

    def draw(self, surface):
        pygame.draw.circle(surface, (0,0,0), np.round(self.position).astype(int), Soldier.radius)
        pygame.draw.circle(surface, self.color, np.round(self.position).astype(int), Soldier.radius-1)


class Bullet:
    speed = 60
    radius = 1
    color = (0, 0, 0)
    damage = 50

    def __init__(self, position, target, team):
        self.position = np.asarray(position, dtype=float)
        direction = np.asarray(target, dtype=float) - self.position
        direction = direction / np.sqrt(direction[0]**2 + direction[1]**2)
        self.velocity = direction * Bullet.speed
        self.team = team
        g_d.bullets.append(self)

    def update(self, delta_time):
        self.dx(self.velocity[0]*delta_time)
        self.dy(self.velocity[1]*delta_time)
        self.check_move()

    def dx(self, d):
        self.position[0] += d

    def dy(self, d):
        self.position[1] += d

    def check_move(self):
        self.check_collision()
        self.check_borders()

    def check_collision(self):
        hit_soldier = c_d.soldier_the_object_touches(self)
        if hit_soldier is not None:
            self.delete_self()
            if hit_soldier.team != self.team:
                hit_soldier.hit(self.damage)

    def check_borders(self):
        if self.position[0] < 0 or self.position[1] < 0 or self.position[0] > g_d.size[0] or self.position[1] > g_d.size[1]:
            self.delete_self()

    def draw(self, surface):
        pygame.draw.circle(surface, Bullet.color, np.round(self.position).astype(int), Bullet.radius)

    def delete_self(self):
        g_d.object_to_delete.append(self)


class Tree:
    radius = 5
    color = (0, 0xff, 0)

    def __init__(self, position):
        self.position = np.asarray(position, dtype=float)

        g_d.trees.append(self)

    def draw(self, surface):
        pygame.draw.circle(surface, Tree.color, np.round(self.position).astype(int), Tree.radius)

