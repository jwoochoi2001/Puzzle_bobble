# game/shooter.py

import math
import arcade

from settings import *


class Shooter:

    def __init__(self):

        self.x = (PLAYFIELD_LEFT + PLAYFIELD_RIGHT) / 2
        self.y = PLAYFIELD_BOTTOM - 42

        self.angle = math.pi / 2

    def rotate_left(self):

        self.angle += math.radians(ANGLE_SPEED)

        if self.angle > POINTER_MAX_ANGLE:
            self.angle = POINTER_MAX_ANGLE

    def rotate_right(self):

        self.angle -= math.radians(ANGLE_SPEED)

        if self.angle < POINTER_MIN_ANGLE:
            self.angle = POINTER_MIN_ANGLE

    def shoot(self, bubble):

        bubble.shoot(self.angle)

    def draw(self):

        gold = (210, 170, 55)
        gold_dark = (150, 110, 30)

        arcade.draw_lrbt_rectangle_filled(
            self.x - 34,
            self.x + 34,
            self.y - 22,
            self.y + 8,
            gold_dark,
        )

        arcade.draw_lrbt_rectangle_filled(
            self.x - 30,
            self.x + 30,
            self.y - 18,
            self.y + 6,
            gold,
        )

        barrel_length = 72
        end_x = self.x + math.cos(self.angle) * barrel_length
        end_y = self.y + math.sin(self.angle) * barrel_length

        arcade.draw_line(
            self.x, self.y, end_x, end_y,
            gold, 10,
        )

        arcade.draw_line(
            self.x, self.y, end_x, end_y,
            arcade.color.WHITE, 2,
        )

        tip_x = end_x + math.cos(self.angle) * 8
        tip_y = end_y + math.sin(self.angle) * 8
        arcade.draw_line(
            end_x, end_y, tip_x, tip_y,
            arcade.color.WHITE, 4,
        )
