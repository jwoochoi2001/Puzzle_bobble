# game/game.py

import random
import time
import arcade

from settings import *

from game.board import Board
from game.bubble import Bubble
from game.shooter import Shooter
from game.floodfill import FloodFill
from game.score import ScoreSystem
from game.stage import StageManager

from game.states import GameState
from game.ui import UI
from game.ceiling import CeilingManager
from game.pop_effect import PopEffectManager


class Game(arcade.Window):

    def __init__(self):

        super().__init__(WIDTH, HEIGHT, TITLE)

        arcade.set_background_color((18, 22, 38))

        self.board = Board()
        self.shooter = Shooter()
        self.score = ScoreSystem()
        self.stage = StageManager()
        self.ui = UI()
        self.ceiling = CeilingManager(1)
        self.pop_effects = PopEffectManager()

        self.left_pressed = False
        self.right_pressed = False

        self.dead_line_y = DEAD_LINE_Y
        self.state = GameState.MENU
        self.run_start_time = 0.0
        self.frozen_play_seconds = None

        self.shake_time = 0.0
        self.shake_x = 0.0
        self.shake_y = 0.0

        self.current_bubble = None
        self.next_bubble = None
        self._prev_keys = {}
        self.pending_stage_clear = False

    def on_show(self):

        self.activate()

    def play_seconds(self):

        if self.frozen_play_seconds is not None:
            return self.frozen_play_seconds

        if self.run_start_time <= 0:
            return 0.0

        return time.time() - self.run_start_time

    def freeze_play_time(self):

        if self.frozen_play_seconds is None:
            self.frozen_play_seconds = self.play_seconds()

    def unfreeze_play_time(self):

        if self.frozen_play_seconds is not None:
            self.run_start_time = (
                time.time() - self.frozen_play_seconds
            )
            self.frozen_play_seconds = None

    def trigger_game_over(self):

        if self.state == GameState.GAME_OVER:
            return

        self.freeze_play_time()
        self.state = GameState.GAME_OVER
        self.board.turn_all_black()

        if self.current_bubble and self.current_bubble.moving:
            self.current_bubble.stop()

    def start_game(self):

        self.board = Board()
        self.score = ScoreSystem()
        self.pop_effects = PopEffectManager()
        self.stage = StageManager()
        self.stage.new_run()
        self.ceiling = CeilingManager(self.stage.current_stage)
        self.run_start_time = time.time()
        self.frozen_play_seconds = None
        self.shake_time = 0.0

        self.shooter.x = (PLAYFIELD_LEFT + PLAYFIELD_RIGHT) / 2
        self.shooter.y = PLAYFIELD_BOTTOM - 42

        self.stage.load_stage(self.board)

        self.current_bubble = self.create_bubble()
        self.next_bubble = self.create_bubble()

        self.left_pressed = False
        self.right_pressed = False
        self.pending_stage_clear = False

    def go_main_menu(self):

        self.state = GameState.MENU
        self.left_pressed = False
        self.right_pressed = False
        self.frozen_play_seconds = None
        self.shake_time = 0.0
        self.shake_x = 0.0
        self.shake_y = 0.0
        self.pending_stage_clear = False

        if self.current_bubble and self.current_bubble.moving:
            self.current_bubble.stop()

    def toggle_pause(self):

        if self.pending_stage_clear:
            return

        if self.state == GameState.PLAYING:
            self.freeze_play_time()
            self.state = GameState.PAUSED

        elif self.state == GameState.PAUSED:
            self.unfreeze_play_time()
            self.state = GameState.PLAYING

    def try_main_menu(self):

        if self.state in (
            GameState.PLAYING,
            GameState.PAUSED,
            GameState.GAME_OVER,
            GameState.STAGE_CLEAR,
            GameState.VICTORY,
        ):
            self.go_main_menu()

    def _poll_hotkeys(self):

        kb = self.keyboard

        if kb is None:
            return

        pause_keys = (arcade.key.P, arcade.key.ESCAPE)
        menu_keys = (arcade.key.M,)

        for key in pause_keys:
            down = bool(kb[key])
            was = self._prev_keys.get(key, False)

            if down and not was:
                self.toggle_pause()

            self._prev_keys[key] = down

        for key in menu_keys:
            down = bool(kb[key])
            was = self._prev_keys.get(key, False)

            if down and not was:
                self.try_main_menu()

            self._prev_keys[key] = down

    def create_bubble(self):

        colors = list(dict.fromkeys(self.board.get_colors_on_board()))

        if not colors:
            count = stage_color_count(self.stage.current_stage)
            colors = list(COLORS[:count])
            random.shuffle(colors)

        return Bubble(
            self.shooter.x,
            self.shooter.y,
            random.choice(colors),
        )

    def prepare_next_bubble(self):

        self.current_bubble = self.next_bubble
        self.current_bubble.x = self.shooter.x
        self.current_bubble.y = self.shooter.y
        self.current_bubble.stop()

        self.next_bubble = self.create_bubble()

    def apply_ceiling_drop(self):

        self.board.drop_ceiling_one_row()
        self.ceiling.drop()
        self.shake_time = 0.35

        if self.stage.is_game_over(self.board):
            self.trigger_game_over()

    def _finish_shot(self, row, col):

        group = FloodFill.find_color_group(
            self.board,
            row,
            col,
        )

        matched_count = 0
        floating_count = 0

        if len(group) >= MIN_MATCH:
            matched_count = len(group)

            match_positions = []
            for row, col in group:
                bubble = self.board.get(row, col)
                if bubble:
                    match_positions.append((bubble.x, bubble.y))

            self.pop_effects.spawn_match_pops(self.board, group)
            FloodFill.remove_group(self.board, group)

            floating_count = 0

            while True:
                floating_batch = FloodFill.find_floating_cells(
                    self.board,
                )

                if not floating_batch:
                    break

                self.pop_effects.spawn_fall_pops(
                    self.board,
                    floating_batch,
                )
                FloodFill.remove_group(
                    self.board,
                    floating_batch,
                )
                floating_count += len(floating_batch)

            combo_bonus, _ = self.score.add_turn_score(
                matched_count,
                floating_count,
            )

            if combo_bonus > 0 and match_positions:
                cx = sum(p[0] for p in match_positions) / len(
                    match_positions,
                )
                cy = sum(p[1] for p in match_positions) / len(
                    match_positions,
                )
                self.pop_effects.spawn_combo_floater(
                    cx,
                    cy,
                    combo_bonus,
                )
        else:
            self.score.add_turn_score(0, 0)
        self.ceiling.record_shot()

        if self.ceiling.should_drop():
            self.apply_ceiling_drop()

            if self.state != GameState.PLAYING:
                return

        if self.stage.can_clear_stage(self.board, self.score.score):
            self.queue_stage_clear()
            return

        self.prepare_next_bubble()

    def queue_stage_clear(self):

        if self.current_bubble and self.current_bubble.moving:
            self.current_bubble.stop()

        self.left_pressed = False
        self.right_pressed = False
        self.pending_stage_clear = True

    def begin_stage_clear(self):

        self.pending_stage_clear = False

        if self.current_bubble and self.current_bubble.moving:
            self.current_bubble.stop()

        self.stage.last_clear_reason = self.stage.resolve_clear_reason(
            self.board,
            self.score.score,
        )
        self.freeze_play_time()
        self.stage.finish_clear()

        if self.stage.is_final_stage():
            self.state = GameState.VICTORY
        else:
            self.state = GameState.STAGE_CLEAR

    def go_next_stage(self):

        cleared_stage = self.stage.current_stage
        self.score.apply_stage_checkpoint(cleared_stage)
        self.stage.next_stage()
        self.stage.load_stage(self.board)
        self.ceiling = CeilingManager(self.stage.current_stage)
        self.pop_effects.clear()
        self.current_bubble = self.create_bubble()
        self.next_bubble = self.create_bubble()
        self.unfreeze_play_time()
        self.state = GameState.PLAYING

    def on_key_press(self, symbol, modifiers):

        if self.state == GameState.MENU:

            if symbol == arcade.key.ENTER:
                self.start_game()
                self.state = GameState.PLAYING

            return

        if self.state == GameState.HELP:
            return

        if self.state == GameState.DEVELOPER:
            return

        if self.state == GameState.PAUSED:
            return

        if self.state == GameState.GAME_OVER:

            if symbol == arcade.key.ENTER:
                self.start_game()
                self.state = GameState.PLAYING

            return

        if self.state == GameState.VICTORY:

            if symbol == arcade.key.ENTER:
                self.go_main_menu()

            return

        if self.state == GameState.STAGE_CLEAR:

            if symbol == arcade.key.ENTER:
                self.go_next_stage()

            return

        if self.state != GameState.PLAYING:
            return

        if self.pending_stage_clear:
            return

        if symbol == arcade.key.LEFT:
            self.left_pressed = True

        if symbol == arcade.key.RIGHT:
            self.right_pressed = True

        if symbol == arcade.key.SPACE:

            if self.current_bubble and not self.current_bubble.moving:
                self.shooter.shoot(self.current_bubble)

    def on_key_release(self, symbol, modifiers):

        if symbol == arcade.key.LEFT:
            self.left_pressed = False

        if symbol == arcade.key.RIGHT:
            self.right_pressed = False

    def on_mouse_press(self, x, y, button, modifiers):

        if self.state == GameState.MENU:

            if self.ui.menu_start_button_hit(x, y):
                self.start_game()
                self.state = GameState.PLAYING

            elif self.ui.menu_help_button_hit(x, y):
                self.state = GameState.HELP

            elif self.ui.menu_dev_button_hit(x, y):
                self.state = GameState.DEVELOPER

            return

        if self.state == GameState.HELP:

            if self.ui.help_back_button_hit(x, y):
                self.state = GameState.MENU

            return

        if self.state == GameState.DEVELOPER:

            if self.ui.dev_back_button_hit(x, y):
                self.state = GameState.MENU

            return

        if self.state == GameState.PLAYING:

            if self.pending_stage_clear:
                return

            if self.ui.pause_button_hit(x, y):
                self.toggle_pause()

            return

        if self.state == GameState.PAUSED:

            if self.ui.resume_button_hit(x, y):
                self.toggle_pause()

            elif self.ui.quit_button_hit(x, y):
                self.go_main_menu()

            return

        if self.state == GameState.STAGE_CLEAR:

            if self.ui.next_button_hit(x, y):
                self.go_next_stage()

            elif self.ui.quit_button_hit(x, y):
                self.go_main_menu()

            return

        if self.state == GameState.VICTORY:

            if self.ui.menu_button_hit(x, y):
                self.go_main_menu()

            return

        if self.state == GameState.GAME_OVER:

            if self.ui.retry_button_hit(x, y):
                self.start_game()
                self.state = GameState.PLAYING

            elif self.ui.go_menu_button_hit(x, y):
                self.go_main_menu()

    def on_update(self, delta_time):

        self._poll_hotkeys()

        if self.pending_stage_clear:
            self.pop_effects.update(delta_time)

            if not self.pop_effects.has_active_effects():
                self.begin_stage_clear()

            return

        if self.state != GameState.PLAYING:
            return

        self.ceiling.update(delta_time)

        if self.ceiling.should_drop():
            self.apply_ceiling_drop()

            if self.state != GameState.PLAYING:
                return

        self.pop_effects.update(delta_time)

        if self.shake_time > 0:
            self.shake_time -= delta_time
            self.shake_x = random.randint(-5, 5)
            self.shake_y = random.randint(-3, 3)
        else:
            shots_left = self.ceiling.shots_remaining()
            time_left = self.ceiling.seconds_remaining()

            if self.ceiling.is_timer_warning():
                self.shake_x = random.randint(-3, 4)
                self.shake_y = random.randint(-2, 2)
            elif shots_left == 2:
                self.shake_x = random.randint(-1, 1)
                self.shake_y = 0
            elif shots_left == 1:
                self.shake_x = random.randint(-4, 4)
                self.shake_y = random.randint(-2, 2)
            elif time_left <= self.ceiling.warning_seconds + 2:
                self.shake_x = random.randint(-1, 1)
                self.shake_y = 0
            else:
                self.shake_x = 0
                self.shake_y = 0

        if self.left_pressed:
            self.shooter.rotate_left()

        if self.right_pressed:
            self.shooter.rotate_right()

        wall_y = self.board.ceiling_wall_y()
        self.current_bubble.update(wall_y)

        if self.current_bubble.moving:

            attached = self.board.attach_bubble(
                self.current_bubble,
            )

            if attached:
                self._finish_shot(*attached)

        if self.stage.is_game_over(self.board):
            self.trigger_game_over()

    def draw_game_world(self):

        sx = self.shake_x
        sy = self.shake_y

        bar_bottom, bar_top = self.board.ceiling_bar_bounds()

        self.ui.draw_playfield_checkered()
        self.ui.draw_ceiling_push_zone(bar_bottom, bar_top)

        for row in range(GRID_ROWS):
            for col in range(cols_for_row(row)):
                bubble = self.board.get(row, col)

                if bubble:
                    ox, oy = bubble.x, bubble.y
                    bubble.x += sx
                    bubble.y += sy
                    bubble.draw()
                    bubble.x, bubble.y = ox, oy

        self.pop_effects.draw(sx, sy)

        self.ui.draw_ceiling_bar(bar_bottom, bar_top)
        self.ui.draw_danger_line(self.dead_line_y + sy)

        self.ui.draw_launcher_area(
            self.shooter.x + sx,
            self.shooter.y + sy,
        )

        ox, oy = self.shooter.x, self.shooter.y
        self.shooter.x += sx
        self.shooter.y += sy
        self.shooter.draw()
        self.shooter.x, self.shooter.y = ox, oy

        if self.current_bubble and self.state == GameState.PLAYING:
            ox, oy = self.current_bubble.x, self.current_bubble.y
            self.current_bubble.x += sx
            self.current_bubble.y += sy
            self.current_bubble.draw()
            self.current_bubble.x, self.current_bubble.y = ox, oy

    def on_draw(self):

        self.clear()

        if self.state == GameState.MENU:
            self.ui.draw_menu()
            return

        if self.state == GameState.HELP:
            self.ui.draw_help_screen()
            return

        if self.state == GameState.DEVELOPER:
            self.ui.draw_developer_screen()
            return

        self.ui.draw_arcade_frame_bg()
        self.ui.draw_playfield_frame()
        self.draw_game_world()

        shots_left = self.ceiling.shots_remaining()
        time_left = self.ceiling.seconds_remaining()
        warning = self.ceiling.is_warning()

        self.ui.draw_top_hud(
            self.score.score,
            self.stage.current_stage,
            self.stage.current_level(),
        )

        self.ui.draw_ceiling_hud(
            shots_left,
            time_left,
            self.ceiling.fire_count,
            warning,
        )

        self.ui.draw_left_score_hud(
            self.stage.score_goal(),
            self.score.score,
        )

        self.ui.draw_bottom_hud(
            self.stage.current_level(),
            self.stage.current_stage,
        )

        if self.next_bubble:
            self.ui.draw_left_bottom_hud(self.next_bubble.color)

        if self.state == GameState.PLAYING and not self.pending_stage_clear:
            self.ui.draw_pause_button()

        if self.pending_stage_clear:
            return

        if self.state == GameState.PAUSED:
            self.ui.draw_pause_panel(
                self.stage.current_level(),
                self.stage.current_stage,
                self.score.score,
                self.stage.score_goal(),
                self.play_seconds(),
                self.score.combo_streak,
            )

        if self.state == GameState.STAGE_CLEAR:
            self.ui.draw_stage_clear(
                self.stage.current_level(),
                self.stage.current_stage,
                self.stage.last_clear_time,
                self.stage.score_goal(),
                self.score.score,
                False,
                self.stage.last_clear_reason,
            )

        if self.state == GameState.VICTORY:
            self.ui.draw_stage_clear(
                self.stage.current_level(),
                self.stage.current_stage,
                self.stage.last_clear_time,
                self.stage.score_goal(),
                self.score.score,
                True,
                self.stage.last_clear_reason,
            )

        if self.state == GameState.GAME_OVER:
            self.ui.draw_game_over_panel(
                self.stage.current_level(),
                self.stage.current_stage,
                self.score.score,
                self.stage.score_goal(),
                self.play_seconds(),
            )
