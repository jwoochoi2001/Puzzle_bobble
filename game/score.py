from settings import *


class ScoreSystem:

    def __init__(self):

        self.score = 0
        self.last_turn_score = 0
        self.last_combo_bonus = 0
        self.last_match_points = 0
        self.last_float_points = 0
        self.combo_streak = 0

    def add_turn_score(self, matched_count, floating_count):

        self.last_turn_score = 0
        self.last_combo_bonus = 0
        self.last_match_points = 0
        self.last_float_points = 0

        if matched_count < MIN_MATCH:
            self.combo_streak = 0
            return 0, 0

        self.combo_streak += 1

        self.last_match_points = matched_count * MATCH_BUBBLE_SCORE
        self.last_float_points = floating_count * FLOATING_BUBBLE_SCORE

        if self.combo_streak >= 2:
            self.last_combo_bonus = (
                (self.combo_streak - 1) * COMBO_BONUS_PER_STEP
            )

        gained = (
            self.last_match_points
            + self.last_float_points
            + self.last_combo_bonus
        )
        self.score += gained
        self.last_turn_score = gained
        self.score = min(self.score, MAX_DISPLAY_SCORE)

        return self.last_combo_bonus, gained

    def reset(self):

        self.score = 0
        self.last_turn_score = 0
        self.last_combo_bonus = 0
        self.last_match_points = 0
        self.last_float_points = 0
        self.combo_streak = 0

    def apply_stage_checkpoint(self, cleared_stage):

        self.score = stage_score_goal(cleared_stage)
        self.last_turn_score = 0
        self.last_combo_bonus = 0
        self.combo_streak = 0
