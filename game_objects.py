import pygame
import numpy as np
from random import random

import game_data as g_d
import collision_detection as c_d

soldier_id = 0
class Soldier:
    radius = 5
    diameter = radius * 2
    field_of_view_radius = 50

    in_forest_speed = 15
    in_forest_evade_chance = 0.70
    default_life_level = 100
    out_forest_speed = 30
    out_forest_evade_chance = 0.05

    colors = [np.asarray((0, 0, 0xff)), np.asarray((0xff, 0, 0))]

    general_reload_time = 0.5

    def __init__(self, position, team):
        global soldier_id
        self.id = soldier_id
        soldier_id += 1

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
        g_d.team_size[self.team] += 1

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
        self.color = Soldier.colors[self.team] // 2

    def out_forest(self):
        self.speed = Soldier.out_forest_speed
        self.evade_chance = Soldier.out_forest_evade_chance
        self.color = Soldier.colors[self.team]

    def try_shoot(self):
        soldier_in_field_view = g_d.closest_reachable_soldiers_map.get(self, None)
        if soldier_in_field_view is not None and self.reloaded():
            soldier_in_field_view.hit(50)

    def reloaded(self):
        return self.time_to_reload <= 0

    def hit(self, damage):
        if self.evade_chance < random():
            self.life -= damage
            if self.life <= 0:
                self.die()

    def die(self):
        if self.life >= 0: # may be killed 2 times in 1 iteration
            g_d.team_size[self.team] -= 1
        g_d.object_to_delete.append(self)

    def is_in_forest(self):
        return c_d.is_position_in_forest(self.position)

    def draw_with_field_view(self, surface):
        self.draw(surface)
        pygame.draw.circle(surface, (0, 0xff, 0), np.round(self.position).astype(int), Soldier.field_of_view_radius, 1)

    def draw(self, surface):
        pygame.draw.circle(surface, (0, 0, 0), np.round(self.position).astype(int), Soldier.radius)
        pygame.draw.circle(surface, self.color, np.round(self.position).astype(int), Soldier.radius-1)

    def __hash__(self):
        return self.id


class Tree:
    radius = 5
    diameter = radius * 2
    color = (0, 0xff, 0)

    def __init__(self, position):
        self.position = np.asarray(position, dtype=float)

        g_d.trees.append(self)

    def draw(self, surface):
        pygame.draw.circle(surface, Tree.color, np.round(self.position).astype(int), Tree.radius)

