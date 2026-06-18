# game/pop_effect.py

import random
import math
import arcade

from settings import *


class ScoreFloater:

    def __init__(self, x, y, points, kind="match"):

        self.x = float(x)
        self.y = float(y)
        self.points = points
        self.kind = kind
        self.age = 0.0
        self.duration = SCORE_FLOAT_DURATION

        if kind == "combo":
            self.text = f"COMBO +{points}"
            self.color = arcade.color.GOLD
            self.size = 20
        elif kind == "fall":
            self.text = f"+{points}"
            self.color = arcade.color.LIGHT_BLUE
            self.size = 17
        else:
            self.text = f"+{points}"
            self.color = arcade.color.WHITE
            self.size = 16

    def update(self, delta_time):

        self.age += delta_time
        self.y += delta_time * 52
        return self.age >= self.duration

    def draw(self):

        t = min(1.0, self.age / self.duration)
        fade = 1.0 - t
        alpha = int(255 * fade)

        arcade.draw_text(
            self.text,
            self.x,
            self.y,
            (*self.color[:3], alpha),
            self.size,
            anchor_x="center",
            bold=True,
        )


class PopEffect:

    POP = "pop"
    FALL = "fall"

    def __init__(self, x, y, color, kind=POP):

        self.x = float(x)
        self.y = float(y)
        self.start_y = float(y)
        self.color = color
        self.kind = kind
        self.age = 0.0

        if kind == self.FALL:
            self.squished = False
            self.splat_age = 0.0
            self.floor_y = PLAYFIELD_BOTTOM + 28
            fall_distance = max(0.0, self.start_y - self.floor_y)
            self.duration = min(
                2.2,
                0.55 + fall_distance / 380.0,
            )
            self.vx = random.uniform(-70, 70)
            self.vy = random.uniform(25, 95)
        else:
            self.duration = POP_EFFECT_DURATION

    def update(self, delta_time):

        self.age += delta_time

        if self.kind == self.FALL and not self.squished:
            self.vy -= FALL_GRAVITY * delta_time
            self.x += self.vx * delta_time
            self.y += self.vy * delta_time

            if self.y <= self.floor_y:
                self.y = self.floor_y
                self.squished = True
                self.splat_age = 0.0
                self.vx *= 0.25

        elif self.kind == self.FALL and self.squished:
            self.splat_age += delta_time

        return self.age >= self.duration

    def _alpha_color(self, alpha):

        r, g, b = self.color[:3]
        return (r, g, b, max(0, min(255, int(alpha))))

    def draw(self):

        t = min(1.0, self.age / self.duration)

        if self.kind == self.POP:
            self._draw_pop(t)
        else:
            self._draw_fall(t)

    def _draw_pop(self, t):

        r = BUBBLE_RADIUS
        fade = max(0.0, 1.0 - t * 1.15)

        if t < 0.12:
            flash = 1.0 - t / 0.12
            arcade.draw_circle_filled(
                self.x,
                self.y,
                r * (1.2 + flash * 0.8),
                (255, 255, 255, int(200 * flash)),
            )

        arcade.draw_circle_filled(
            self.x,
            self.y,
            r * max(0.1, 1.0 - t * 0.9),
            self._alpha_color(230 * fade),
        )

        arcade.draw_circle_outline(
            self.x,
            self.y,
            r * (1.0 + t * 1.8),
            self._alpha_color(255 * fade),
            4,
        )

        arcade.draw_circle_outline(
            self.x,
            self.y,
            r * (0.5 + t * 1.1),
            self._alpha_color(200 * fade),
            2,
        )

        for i in range(8):
            ang = i * math.pi / 4.0 + t * 4.5
            dist = r * (0.5 + t * 1.6)
            px = self.x + math.cos(ang) * dist
            py = self.y + math.sin(ang) * dist
            arcade.draw_circle_filled(
                px,
                py,
                max(2.0, r * 0.2 * fade),
                self._alpha_color(255 * fade),
            )

    def _draw_fall(self, t):

        r = BUBBLE_RADIUS

        if not self.squished:
            if self.age < 0.1:
                burst = 1.0 - self.age / 0.1
                arcade.draw_circle_filled(
                    self.x,
                    self.y,
                    r * (1.1 + burst * 0.6),
                    (255, 255, 255, int(190 * burst)),
                )
                arcade.draw_circle_outline(
                    self.x,
                    self.y,
                    r * (1.0 + (1.0 - burst) * 1.2),
                    self._alpha_color(255 * burst),
                    3,
                )

            wobble = math.sin(self.age * 18) * 2
            stretch = 1.0 + abs(self.vy) * 0.0015
            arcade.draw_ellipse_filled(
                self.x + wobble,
                self.y,
                r * 1.85 * stretch,
                r * 1.75 / stretch,
                self._alpha_color(220),
            )
            arcade.draw_ellipse_outline(
                self.x + wobble,
                self.y,
                r * 1.9 * stretch,
                r * 1.8 / stretch,
                self._alpha_color(160),
                2,
            )
            hi = r * 0.25
            arcade.draw_circle_filled(
                self.x + wobble - hi,
                self.y + hi * 0.5,
                hi * 0.55,
                self._alpha_color(180),
            )
            return

        splat_t = min(1.0, self.splat_age / 0.35)
        fade = max(0.0, 1.0 - splat_t)
        spread = r * (1.0 + splat_t * 1.4)
        squish = r * (0.35 + (1.0 - splat_t) * 0.2)

        arcade.draw_ellipse_filled(
            self.x,
            self.floor_y,
            spread * 2,
            squish,
            self._alpha_color(180 * fade),
        )

        for i in range(5):
            ang = -math.pi / 2 + (i - 2) * 0.35
            dist = spread * (0.6 + splat_t * 0.5)
            px = self.x + math.cos(ang) * dist
            py = self.floor_y + abs(math.sin(ang)) * squish * 0.4
            arcade.draw_circle_filled(
                px,
                py,
                max(2.0, r * 0.12 * fade),
                self._alpha_color(220 * fade),
            )


class PopEffectManager:

    def __init__(self):

        self.effects = []
        self.floaters = []

    def clear(self):

        self.effects = []
        self.floaters = []

    def _bubble_positions(self, board, cells):

        positions = []

        for row, col in cells:
            bubble = board.get(row, col)

            if bubble is None:
                continue

            positions.append((bubble.x, bubble.y, bubble.color))

        return positions

    def spawn_match_pops(self, board, cells):

        for x, y, color in self._bubble_positions(board, cells):
            self.effects.append(PopEffect(x, y, color, PopEffect.FALL))
            self.floaters.append(
                ScoreFloater(x, y, MATCH_BUBBLE_SCORE, "match"),
            )

    def spawn_fall_pops(self, board, cells):

        for x, y, color in self._bubble_positions(board, cells):
            self.effects.append(PopEffect(x, y, color, PopEffect.FALL))
            self.floaters.append(
                ScoreFloater(x, y, FLOATING_BUBBLE_SCORE, "fall"),
            )

    def spawn_combo_floater(self, x, y, bonus):

        if bonus <= 0:
            return

        self.floaters.append(
            ScoreFloater(x, y + 24, bonus, "combo"),
        )

    def has_active_effects(self):

        return bool(self.effects or self.floaters)

    def update(self, delta_time):

        self.effects = [
            effect
            for effect in self.effects
            if not effect.update(delta_time)
        ]
        self.floaters = [
            floater
            for floater in self.floaters
            if not floater.update(delta_time)
        ]

    def draw(self, offset_x=0.0, offset_y=0.0):

        for effect in self.effects:
            ox, oy = effect.x, effect.y
            effect.x += offset_x
            effect.y += offset_y

            if effect.kind == PopEffect.FALL:
                effect.floor_y += offset_y

            effect.draw()
            effect.x, effect.y = ox, oy

            if effect.kind == PopEffect.FALL:
                effect.floor_y -= offset_y

        for floater in self.floaters:
            ox, oy = floater.x, floater.y
            floater.x += offset_x
            floater.y += offset_y
            floater.draw()
            floater.x, floater.y = ox, oy
