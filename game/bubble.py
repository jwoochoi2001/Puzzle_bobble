# game/bubble.py

import math
import arcade

from settings import *


class Bubble:

    def __init__(self, x, y, color):

        self.x = float(x)
        self.y = float(y)
        self.color = color

        self.dx = 0
        self.dy = 0
        self.moving = False

    def shoot(self, angle):

        self.dx = math.cos(angle) * SHOOT_SPEED
        self.dy = math.sin(angle) * SHOOT_SPEED
        self.moving = True

    def stop(self):

        self.dx = 0
        self.dy = 0
        self.moving = False

    def update(self, ceiling_wall_y=None):

        if not self.moving:
            return

        wall = (
            ceiling_wall_y
            if ceiling_wall_y is not None
            else CEILING_WALL_Y
        )

        self.x += self.dx
        self.y += self.dy

        if self.x <= WALL_INNER_LEFT:
            self.x = WALL_INNER_LEFT
            self.dx *= -1

        elif self.x >= WALL_INNER_RIGHT:
            self.x = WALL_INNER_RIGHT
            self.dx *= -1

        if self.y >= wall:
            self.y = wall
            self.dy = 0
            self.dx = 0

    def draw(self):

        r = BUBBLE_RADIUS

        arcade.draw_circle_filled(
            self.x + 2,
            self.y - 2,
            r,
            (0, 0, 0, 80),
        )

        arcade.draw_circle_filled(
            self.x,
            self.y,
            r,
            self.color,
        )

        arcade.draw_circle_outline(
            self.x,
            self.y,
            r,
            (255, 255, 255, 200),
            2,
        )

        hi = max(4, r // 3)
        arcade.draw_circle_filled(
            self.x - hi,
            self.y + hi,
            hi,
            (255, 255, 255, 150),
        )

        arcade.draw_circle_filled(
            self.x - hi // 2,
            self.y + hi // 2,
            hi // 2,
            (255, 255, 255, 220),
        )

    def distance_to(self, other):

        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)

    def collides_with(self, other):

        return self.distance_to(other) <= BUBBLE_DIAMETER - 1

    def hit_ceiling(self, ceiling_wall_y=None):

        wall = (
            ceiling_wall_y
            if ceiling_wall_y is not None
            else CEILING_WALL_Y
        )

        return self.y >= wall
