# game/board.py

import math

from settings import *
from game.bubble import Bubble


class Board:

    def __init__(self):

        self.grid = [
            [None for _ in range(GRID_COLS)]
            for _ in range(GRID_ROWS)
        ]
        self.ceiling_offset = 0.0

    # -------------------------

    def reset_ceiling(self):

        self.ceiling_offset = 0.0

    def cell_to_pixel(self, row, col):

        x = GRID_ORIGIN_X + col * BUBBLE_DIAMETER

        if row % 2 == 1:
            x += BUBBLE_RADIUS

        y = (
            GRID_TOP_Y
            - row * ROW_HEIGHT
            - self.ceiling_offset
        )

        return x, y

    # -------------------------

    def pixel_to_cell(self, x, y):

        row = round(
            (GRID_TOP_Y - self.ceiling_offset - y) / ROW_HEIGHT,
        )

        cx = x
        if row % 2 == 1:
            cx -= BUBBLE_RADIUS

        col = round((cx - GRID_ORIGIN_X) / BUBBLE_DIAMETER)

        row = max(0, min(GRID_ROWS - 1, row))
        col = max(0, min(cols_for_row(row) - 1, col))

        return row, col

    # -------------------------

    def is_valid_cell(self, row, col):

        if row < 0 or row >= GRID_ROWS:
            return False

        return 0 <= col < cols_for_row(row)

    def inside(self, row, col):

        return self.is_valid_cell(row, col)

    # -------------------------

    def get(self, row, col):

        if not self.inside(row, col):
            return None

        return self.grid[row][col]

    # -------------------------

    def set(self, row, col, bubble):

        if self.inside(row, col):
            self.grid[row][col] = bubble

    # -------------------------

    def remove(self, row, col):

        if self.inside(row, col):
            self.grid[row][col] = None

    # -------------------------

    def neighbors(self, row, col):

        if row % 2 == 0:
            dirs = [
                (-1, -1), (-1, 0),
                (0, -1), (0, 1),
                (1, -1), (1, 0),
            ]
        else:
            dirs = [
                (-1, 0), (-1, 1),
                (0, -1), (0, 1),
                (1, 0), (1, 1),
            ]

        result = []

        for dr, dc in dirs:
            nr = row + dr
            nc = col + dc

            if self.inside(nr, nc):
                result.append((nr, nc))

        return result

    # -------------------------

    def _dist_sq(self, x1, y1, x2, y2):

        dx = x1 - x2
        dy = y1 - y2
        return dx * dx + dy * dy

    # -------------------------

    def find_collision(self, moving):

        best = None
        best_dist = float("inf")

        for row in range(GRID_ROWS):
            for col in range(cols_for_row(row)):
                bubble = self.grid[row][col]

                if bubble is None:
                    continue

                if moving.collides_with(bubble):
                    d = self._dist_sq(
                        moving.x,
                        moving.y,
                        bubble.x,
                        bubble.y,
                    )
                    if d < best_dist:
                        best_dist = d
                        best = (row, col)

        return best

    # -------------------------

    def find_attach_cell(self, moving, hit_row, hit_col):

        """충돌한 공 주변 빈 칸 중, 실제 맞은 방향(접촉 벡터)과 가장 잘 맞는 칸."""

        hit_x, hit_y = self.cell_to_pixel(hit_row, hit_col)

        cx = moving.x - hit_x
        cy = moving.y - hit_y
        clen = math.hypot(cx, cy)

        if clen < 1e-6:
            cx = -moving.dx
            cy = -moving.dy
            clen = math.hypot(cx, cy)

        if clen > 1e-6:
            cx /= clen
            cy /= clen
        else:
            cx, cy = 0.0, -1.0

        candidates = []

        for nr, nc in self.neighbors(hit_row, hit_col):
            if self.grid[nr][nc] is None:
                candidates.append((nr, nc))

        if not candidates:
            return None

        def attach_score(rc):

            px, py = self.cell_to_pixel(*rc)
            nx = px - hit_x
            ny = py - hit_y
            nlen = math.hypot(nx, ny)

            if nlen < 1e-6:
                return (float("inf"), float("inf"))

            dot = (nx / nlen) * cx + (ny / nlen) * cy
            dist = self._dist_sq(moving.x, moving.y, px, py)

            return (-dot, dist)

        return min(candidates, key=attach_score)

    # -------------------------

    def find_ceiling_attach_cell(self, moving):

        row, col = self.pixel_to_cell(moving.x, moving.y)

        if (
            self.inside(row, col)
            and self.grid[row][col] is None
        ):
            return row, col

        top = self.top_occupied_row()

        if top is None:
            search_to = 2
        else:
            search_to = min(top + 1, GRID_ROWS - 1)

        return self.find_nearest_empty_cell(
            moving.x,
            moving.y,
            max_row=search_to,
        )

    def find_nearest_empty_cell(self, x, y, max_row=3):

        best = None
        best_dist = float("inf")

        for row in range(min(max_row + 1, GRID_ROWS)):
            for col in range(cols_for_row(row)):
                if self.grid[row][col] is not None:
                    continue

                px, py = self.cell_to_pixel(row, col)
                d = self._dist_sq(x, y, px, py)

                if d < best_dist:
                    best_dist = d
                    best = (row, col)

        return best

    def top_occupied_row(self):

        for row in range(GRID_ROWS):
            for col in range(cols_for_row(row)):
                if self.grid[row][col] is not None:
                    return row

        return None

    def is_empty(self):

        return self.top_occupied_row() is None

    # -------------------------

    def attach_bubble(self, moving):

        wall_y = self.ceiling_wall_y()

        if moving.hit_ceiling(wall_y):
            pos = self.find_ceiling_attach_cell(moving)

            if pos is None:
                return None

            row, col = pos

            if self.grid[row][col] is not None:
                return None

            x, y = self.cell_to_pixel(row, col)
            moving.x = x
            moving.y = y
            moving.stop()
            self.set(row, col, moving)
            return row, col

        hit = self.find_collision(moving)

        if hit is None:
            return None

        row, col = hit

        pos = self.find_attach_cell(
            moving,
            row,
            col,
        )

        if pos is None:
            return None

        nr, nc = pos

        if self.grid[nr][nc] is not None:
            return None

        x, y = self.cell_to_pixel(nr, nc)
        moving.x = x
        moving.y = y
        moving.stop()
        self.set(nr, nc, moving)
        return nr, nc

    # -------------------------

    def sync_positions(self):

        for row in range(GRID_ROWS):
            for col in range(cols_for_row(row)):
                bubble = self.grid[row][col]

                if bubble:
                    bubble.x, bubble.y = self.cell_to_pixel(
                        row,
                        col,
                    )

    # -------------------------

    def drop_ceiling_one_row(self):

        """나도코딩 wall_height 방식 — 격자는 유지, 전체를 한 줄 아래로."""

        self.ceiling_offset += ROW_HEIGHT
        self.sync_positions()
        return False

    def lowest_bubble_y(self):

        lowest = None

        for row in range(GRID_ROWS):
            for col in range(cols_for_row(row)):
                bubble = self.grid[row][col]

                if bubble is None:
                    continue

                if lowest is None or bubble.y < lowest:
                    lowest = bubble.y

        return lowest

    def count_bubbles(self):

        n = 0

        for row in range(GRID_ROWS):
            for col in range(cols_for_row(row)):
                if self.grid[row][col] is not None:
                    n += 1

        return n

    def is_empty(self):

        return self.count_bubbles() == 0

    def get_colors_on_board(self):

        colors = []

        for row in range(GRID_ROWS):
            for col in range(cols_for_row(row)):
                bubble = self.grid[row][col]

                if bubble is None:
                    continue

                if bubble.color not in colors:
                    colors.append(bubble.color)

        return colors

    def turn_all_black(self):

        for row in range(GRID_ROWS):
            for col in range(cols_for_row(row)):
                bubble = self.grid[row][col]

                if bubble:
                    bubble.color = BLACK

    def ceiling_bar_bounds(self):

        bar_top = CEILING_BAR_TOP - self.ceiling_offset
        bar_bottom = bar_top - CEILING_BAR_THICKNESS

        return bar_bottom, bar_top

    def ceiling_wall_y(self):

        return CEILING_WALL_Y - self.ceiling_offset

    # -------------------------

    def draw(self):

        for row in range(GRID_ROWS):
            for col in range(cols_for_row(row)):
                bubble = self.grid[row][col]

                if bubble:
                    bubble.draw()
