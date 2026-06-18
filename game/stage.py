# game/stage.py

import random
import time

from settings import *
from game.bubble import Bubble
from game.stage_patterns import (
    TUTORIAL_MAPS,
    STAGE_PATTERNS,
    LEVEL_PATTERN_IDS,
)


class StageManager:

    def __init__(self):

        self.current_stage = 1
        self.stage_start_time = 0.0
        self.last_clear_time = 0.0
        self.last_clear_reason = "score"
        self.run_nonce = random.randint(1, 999_999_999)

    def new_run(self):

        self.run_nonce = random.randint(1, 999_999_999)

    def load_stage(self, board):

        self.clear_board(board)
        board.reset_ceiling()

        if self.current_stage in TUTORIAL_MAPS:
            self._load_tutorial_map(board, TUTORIAL_MAPS[self.current_stage])
        else:
            self._load_pattern_map(board)

        board.sync_positions()
        self.stage_start_time = time.time()

    def _color_pool(self):

        count = stage_color_count(self.current_stage)
        pool = list(COLORS[:count])
        random.shuffle(pool)
        return pool

    def _pick_color(self, pool):

        return random.choice(pool)

    def _load_tutorial_map(self, board, rows):

        pool = self._color_pool()

        for row_idx, row_str in enumerate(rows):

            if row_idx >= GRID_ROWS:
                break

            limit = cols_for_row(row_idx)

            for col_idx, ch in enumerate(row_str[:limit]):

                if ch in (".", "/"):
                    continue

                x, y = board.cell_to_pixel(row_idx, col_idx)
                board.set(
                    row_idx,
                    col_idx,
                    Bubble(x, y, self._pick_color(pool)),
                )

    def _mirror_pattern(self, pattern):

        mirrored = []

        for row, col in pattern:
            max_col = cols_for_row(row) - 1
            mirrored.append((row, max_col - col))

        return mirrored

    def _normalize_pattern(self, pattern):

        if not pattern:
            return []

        min_row = min(row for row, col in pattern)
        shifted = [
            (row - min_row, col)
            for row, col in pattern
        ]

        return shifted

    def _resolve_pattern(self):

        level = stage_to_level(self.current_stage)

        if self.current_stage in STAGE_PATTERNS:
            pattern = list(STAGE_PATTERNS[self.current_stage])
        else:
            pool_ids = LEVEL_PATTERN_IDS.get(
                level,
                LEVEL_PATTERN_IDS[MAX_LEVEL],
            )
            pattern_id = random.choice(pool_ids)
            pattern = list(STAGE_PATTERNS[pattern_id])

        if random.random() < 0.45:
            pattern = self._mirror_pattern(pattern)

        pattern = self._normalize_pattern(pattern)
        pattern = self._thicken_pattern(pattern, level)

        return pattern

    def _thicken_pattern(self, pattern, level):

        """레벨이 높을수록 같은 뼈대에 공을 조금 더 추가."""

        cells = set(pattern)
        target_extra = (level - 1) * 2 + (self.current_stage % 3)
        added = 0
        tries = 0

        while added < target_extra and tries < 80:
            tries += 1
            seed = random.choice(list(cells))
            row, col = seed

            for nr, nc in self._neighbor_coords(row, col):
                if (nr, nc) in cells:
                    continue
                if nr >= GRID_ROWS - 2:
                    continue
                cells.add((nr, nc))
                added += 1
                break

        return list(cells)

    def _neighbor_coords(self, row, col):

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

            if 0 <= nr < GRID_ROWS and 0 <= nc < cols_for_row(nr):
                result.append((nr, nc))

        return result

    def _load_pattern_map(self, board):

        pattern = self._resolve_pattern()
        pool = self._color_pool()

        for row, col in pattern:

            if not board.is_valid_cell(row, col):
                continue

            x, y = board.cell_to_pixel(row, col)

            board.set(
                row,
                col,
                Bubble(x, y, self._pick_color(pool)),
            )

    def elapsed_seconds(self):

        return time.time() - self.stage_start_time

    def finish_clear(self):

        self.last_clear_time = self.elapsed_seconds()

    def next_stage(self):

        if self.current_stage < MAX_STAGE:
            self.current_stage += 1

    def is_final_stage(self):

        return self.current_stage >= MAX_STAGE

    def is_score_goal_met(self, total_score):

        return total_score >= stage_score_goal(self.current_stage)

    def is_board_cleared(self, board):

        return board.is_empty()

    def can_clear_stage(self, board, total_score):

        return (
            self.is_score_goal_met(total_score)
            or self.is_board_cleared(board)
        )

    def resolve_clear_reason(self, board, total_score):

        if self.is_board_cleared(board):
            return "board"

        return "score"

    def current_level(self):

        return stage_to_level(self.current_stage)

    def score_goal(self):

        return stage_score_goal(self.current_stage)

    def clear_board(self, board):

        for row in range(GRID_ROWS):
            for col in range(cols_for_row(row)):
                board.remove(row, col)

    def is_game_over(self, board):

        lowest = board.lowest_bubble_y()

        if lowest is None:
            return False

        return lowest <= DEAD_LINE_Y
