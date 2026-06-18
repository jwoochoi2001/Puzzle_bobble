import arcade

from settings import *


class UI:

    def __init__(self):

        self._buttons = {}

    def _store_button(self, name, left, bottom, right, top):

        self._buttons[name] = (left, bottom, right, top)

    def button_hit(self, name, x, y):

        rect = self._buttons.get(name)

        if rect is None:
            return False

        left, bottom, right, top = rect
        return left <= x <= right and bottom <= y <= top

    def _draw_button(self, name, label, base_color, text_size=14):

        left, bottom, right, top = self._buttons[name]

        arcade.draw_lrbt_rectangle_filled(
            left, right, bottom, top, base_color,
        )
        arcade.draw_lrbt_rectangle_outline(
            left, right, bottom, top, arcade.color.WHITE, 2,
        )
        arcade.draw_text(
            label,
            (left + right) / 2,
            (bottom + top) / 2 - text_size * 0.35,
            arcade.color.WHITE,
            text_size,
            anchor_x="center",
            bold=True,
        )

    def layout_pause_button(self):

        left = PLAYFIELD_RIGHT + 18
        right = WIDTH - 18
        bottom = HEIGHT - 86
        top = HEIGHT - 46
        self._store_button("pause", left, bottom, right, top)

    def draw_pause_button(self):

        self.layout_pause_button()
        self._draw_button("pause", "정지", (70, 95, 145), 15)

    def layout_menu_buttons(self):

        cx = WIDTH / 2
        w = 220
        h = 46
        gap = 16

        play_bottom = HEIGHT / 2 - 20
        play_top = play_bottom + h
        self._store_button(
            "menu_start",
            cx - w / 2,
            play_bottom,
            cx + w / 2,
            play_top,
        )

        help_bottom = play_bottom - h - gap
        help_top = help_bottom + h
        self._store_button(
            "menu_help",
            cx - w / 2,
            help_bottom,
            cx + w / 2,
            help_top,
        )

        dev_gap = 24
        dev_h = 38
        dev_w = 180
        dev_top = help_bottom - dev_gap
        dev_bottom = dev_top - dev_h
        self._store_button(
            "menu_dev",
            cx - dev_w / 2,
            dev_bottom,
            cx + dev_w / 2,
            dev_top,
        )

    def layout_help_back_button(self, bottom=None):

        cx = WIDTH / 2
        w = 160
        h = 40
        if bottom is None:
            bottom = HEIGHT / 2 - 200
        top = bottom + h
        self._store_button("help_back", cx - w / 2, bottom, cx + w / 2, top)

    def layout_pause_panel_buttons(self, button_bottom):

        cx = WIDTH / 2
        w = 170
        h = 46
        gap = 20

        self._store_button(
            "resume",
            cx - w - gap / 2,
            button_bottom,
            cx - gap / 2,
            button_bottom + h,
        )
        self._store_button(
            "quit",
            cx + gap / 2,
            button_bottom,
            cx + w + gap / 2,
            button_bottom + h,
        )

    def draw_menu(self):

        self.draw_arcade_frame_bg()
        self._draw_menu_decorations()

        panel_w = 340
        panel_left = WIDTH / 2 - panel_w / 2
        panel_right = WIDTH / 2 + panel_w / 2
        panel_top = HEIGHT / 2 + 210
        panel_bottom = HEIGHT / 2 - 165

        arcade.draw_lrbt_rectangle_filled(
            panel_left,
            panel_right,
            panel_bottom,
            panel_top,
            (24, 32, 58, 210),
        )
        arcade.draw_lrbt_rectangle_outline(
            panel_left,
            panel_right,
            panel_bottom,
            panel_top,
            FRAME_TEAL,
            3,
        )
        arcade.draw_lrbt_rectangle_outline(
            panel_left + 6,
            panel_right - 6,
            panel_bottom + 6,
            panel_top - 6,
            (100, 200, 210, 120),
            2,
        )

        arcade.draw_text(
            "PUZZLE",
            WIDTH / 2 + 2,
            panel_top - 58,
            (0, 0, 0, 140),
            40,
            anchor_x="center",
            bold=True,
        )
        arcade.draw_text(
            "PUZZLE",
            WIDTH / 2,
            panel_top - 56,
            arcade.color.WHITE,
            40,
            anchor_x="center",
            bold=True,
        )
        arcade.draw_text(
            "BOBBLE",
            WIDTH / 2 + 2,
            panel_top - 102,
            (0, 0, 0, 140),
            40,
            anchor_x="center",
            bold=True,
        )
        arcade.draw_text(
            "BOBBLE",
            WIDTH / 2,
            panel_top - 100,
            arcade.color.CYAN,
            40,
            anchor_x="center",
            bold=True,
        )

        arcade.draw_text(
            f"STAGE {MAX_STAGE}  ·  LEVEL {MAX_LEVEL}",
            WIDTH / 2,
            panel_top - 138,
            arcade.color.LIGHT_GRAY,
            14,
            anchor_x="center",
        )

        self.layout_menu_buttons()
        self._draw_button("menu_start", "▶  게임하기", (55, 145, 95), 20)
        self._draw_button("menu_help", "게임 설명", (70, 95, 145), 18)
        self._draw_button("menu_dev", "개발자", (55, 55, 75), 14)

    def layout_dev_back_button(self, bottom=None):

        cx = WIDTH / 2
        w = 160
        h = 40
        if bottom is None:
            bottom = HEIGHT / 2 - 200
        top = bottom + h
        self._store_button("dev_back", cx - w / 2, bottom, cx + w / 2, top)

    def _draw_menu_decorations(self):

        bubbles = [
            (120, 720, RED, 22),
            (210, 780, YELLOW, 18),
            (WIDTH - 130, 760, BLUE, 24),
            (WIDTH - 220, 680, GREEN, 16),
            (WIDTH - 90, 620, PURPLE, 14),
            (95, 580, CYAN, 20),
            (WIDTH / 2 - 180, 640, YELLOW, 12),
            (WIDTH / 2 + 200, 820, RED, 15),
        ]

        for x, y, color, r in bubbles:
            arcade.draw_circle_filled(x + 2, y - 2, r, (0, 0, 0, 60))
            arcade.draw_circle_filled(x, y, r, color)
            arcade.draw_circle_outline(x, y, r, (255, 255, 255, 160), 2)
            hi = max(3, r // 3)
            arcade.draw_circle_filled(
                x - hi * 0.4,
                y + hi * 0.4,
                hi * 0.5,
                (255, 255, 255, 130),
            )

        arcade.draw_lrbt_rectangle_filled(
            PLAYFIELD_LEFT - 8,
            PLAYFIELD_RIGHT + 8,
            PLAYFIELD_BOTTOM - 20,
            PLAYFIELD_TOP + 12,
            (40, 24, 62, 90),
        )
        arcade.draw_lrbt_rectangle_outline(
            PLAYFIELD_LEFT - 8,
            PLAYFIELD_RIGHT + 8,
            PLAYFIELD_BOTTOM - 20,
            PLAYFIELD_TOP + 12,
            FRAME_TEAL_DARK,
            2,
        )

    def draw_help_screen(self):

        self.draw_arcade_frame_bg()

        box_w = 460
        box_h = 310
        left = WIDTH / 2 - box_w / 2
        right = WIDTH / 2 + box_w / 2
        bottom = HEIGHT / 2 - 40
        top = bottom + box_h
        text_x = left + 28

        arcade.draw_lrbt_rectangle_filled(
            left, right, bottom, top, (28, 38, 62),
        )
        arcade.draw_lrbt_rectangle_outline(
            left, right, bottom, top, arcade.color.CYAN, 3,
        )

        arcade.draw_text(
            "게임 설명",
            WIDTH / 2,
            top - 36,
            arcade.color.GOLD,
            26,
            anchor_x="center",
            bold=True,
        )

        sections = [
            (
                "조작",
                [
                    "← →  조준",
                    "SPACE  발사",
                    "P / ESC / 우측 정지 버튼  일시정지",
                    "ENTER  클리어 후 다음 스테이지",
                ],
            ),
            (
                "점수",
                [
                    f"터뜨린 공 1개  +{MATCH_BUBBLE_SCORE}",
                    f"떨어진 공 1개  +{FLOATING_BUBBLE_SCORE}",
                    (
                        f"연속 콤보  +{COMBO_BONUS_PER_STEP} (2연속), "
                        f"+{COMBO_BONUS_PER_STEP * 2} (3연속) ..."
                    ),
                    "목표 점수 달성 또는 공 전부 제거 시 클리어",
                    "스테이지 상승 시 목표 점수 증가",
                ],
            ),
        ]

        y = top - 66
        for title, lines in sections:
            arcade.draw_text(
                title,
                text_x,
                y,
                arcade.color.CYAN,
                16,
                anchor_x="left",
                bold=True,
            )
            y -= 24

            for line in lines:
                arcade.draw_text(
                    line,
                    text_x + 8,
                    y,
                    arcade.color.WHITE,
                    14,
                    anchor_x="left",
                )
                y -= 20

            y -= 8

        self.layout_help_back_button(bottom - 56)
        self._draw_button("help_back", "돌아가기", (90, 70, 130), 17)

    def draw_developer_screen(self):

        self.draw_arcade_frame_bg()

        box_w = 400
        box_h = 260
        left = WIDTH / 2 - box_w / 2
        right = WIDTH / 2 + box_w / 2
        bottom = HEIGHT / 2 + 20
        top = bottom + box_h

        arcade.draw_lrbt_rectangle_filled(
            left, right, bottom, top, (28, 38, 62),
        )
        arcade.draw_lrbt_rectangle_outline(
            left, right, bottom, top, FRAME_TEAL, 3,
        )

        arcade.draw_text(
            "개발자",
            WIDTH / 2,
            top - 40,
            arcade.color.GOLD,
            26,
            anchor_x="center",
            bold=True,
        )

        arcade.draw_text(
            "최정우",
            WIDTH / 2,
            top - 100,
            arcade.color.WHITE,
            32,
            anchor_x="center",
            bold=True,
        )

        lines = [
            "Puzzle Bobble 스타일 퍼즐 게임",
            "Python + Arcade 제작",
            "jwoochoi2001@naver.com",
        ]

        y = top - 148
        for i, line in enumerate(lines):
            color = arcade.color.CYAN if i == len(lines) - 1 else arcade.color.LIGHT_GRAY
            arcade.draw_text(
                line,
                WIDTH / 2,
                y,
                color,
                14,
                anchor_x="center",
            )
            y -= 24

        self.layout_dev_back_button(bottom - 56)
        self._draw_button("dev_back", "돌아가기", (90, 70, 130), 17)

    def draw_pause_panel(
            self,
            level,
            stage,
            score,
            goal_score,
            play_seconds,
            combo_streak,
    ):

        arcade.draw_lrbt_rectangle_filled(
            0, WIDTH, 0, HEIGHT, (0, 0, 0, 185),
        )

        box_w = 500
        box_h = 340
        left = WIDTH / 2 - box_w / 2
        right = WIDTH / 2 + box_w / 2
        bottom = HEIGHT / 2 - 150
        top = HEIGHT / 2 + 190

        arcade.draw_lrbt_rectangle_filled(
            left, right, bottom, top, (30, 42, 68),
        )
        arcade.draw_lrbt_rectangle_outline(
            left, right, bottom, top, arcade.color.WHITE, 3,
        )

        arcade.draw_text(
            "일시정지",
            WIDTH / 2,
            top - 42,
            arcade.color.GOLD,
            30,
            anchor_x="center",
            bold=True,
        )

        remain = max(0, goal_score - score)
        y = top - 82
        score_text = format_score(score)
        goal_text = format_score(goal_score)

        info_lines = [
            f"LEVEL {level}  ·  STAGE {stage:02d} / {MAX_STAGE}",
            f"SCORE  {score_text}  /  GOAL {goal_text}",
            f"남은 점수  {format_score(remain)}",
            f"플레이 시간  {play_seconds:.1f}s",
            f"연속 콤보  {combo_streak}",
        ]

        for line in info_lines:
            arcade.draw_text(
                line,
                WIDTH / 2,
                y,
                arcade.color.WHITE,
                19,
                anchor_x="center",
            )
            y -= 30

        self.layout_pause_panel_buttons(bottom + 18)
        self._draw_button("resume", "계속하기", (55, 130, 90), 18)
        self._draw_button("quit", "그만하기", (150, 70, 70), 18)

    def layout_game_over_buttons(self):

        cx = WIDTH / 2
        w = 170
        h = 46
        gap = 20
        bottom = HEIGHT / 2 - 175

        self._store_button(
            "retry",
            cx - w - gap / 2,
            bottom,
            cx - gap / 2,
            bottom + h,
        )
        self._store_button(
            "go_menu",
            cx + gap / 2,
            bottom,
            cx + w + gap / 2,
            bottom + h,
        )

    def draw_game_over_panel(
            self,
            level,
            stage,
            score,
            goal_score,
            play_seconds,
    ):

        arcade.draw_lrbt_rectangle_filled(
            0, WIDTH, 0, HEIGHT, (0, 0, 0, 185),
        )

        box_w = 520
        left = WIDTH / 2 - box_w / 2
        right = WIDTH / 2 + box_w / 2
        bottom = HEIGHT / 2 - 210
        top = HEIGHT / 2 + 270

        arcade.draw_lrbt_rectangle_filled(
            left, right, bottom, top, (45, 28, 38),
        )
        arcade.draw_lrbt_rectangle_outline(
            left, right, bottom, top, arcade.color.RED, 3,
        )

        arcade.draw_text(
            "GAME OVER",
            WIDTH / 2,
            top - 48,
            arcade.color.RED,
            32,
            anchor_x="center",
            bold=True,
        )

        arcade.draw_text(
            "위험선 아래로 내려왔습니다",
            WIDTH / 2,
            top - 88,
            arcade.color.LIGHT_GRAY,
            18,
            anchor_x="center",
        )

        y = top - 130
        score_text = format_score(score)
        goal_text = format_score(goal_score)
        for line in (
            f"LEVEL {level}  ·  STAGE {stage:02d} / {MAX_STAGE}",
            f"SCORE  {score_text}  /  GOAL {goal_text}",
            f"플레이 시간  {play_seconds:.1f}s",
        ):
            arcade.draw_text(
                line,
                WIDTH / 2,
                y,
                arcade.color.WHITE,
                20,
                anchor_x="center",
            )
            y -= 34

        self.layout_game_over_buttons()
        self._draw_button("retry", "다시하기", (55, 130, 90), 18)
        self._draw_button("go_menu", "처음 화면", (150, 70, 70), 18)

    def draw_arcade_frame_bg(self):

        arcade.draw_lrbt_rectangle_filled(
            0, WIDTH, 0, HEIGHT, (18, 22, 38),
        )

        self._draw_side_panel(0, PLAYFIELD_LEFT)
        self._draw_side_panel(PLAYFIELD_RIGHT, WIDTH)

    def _draw_side_panel(self, left, right):

        arcade.draw_lrbt_rectangle_filled(
            left, right, 0, HEIGHT, PANEL_BLUE,
        )

        vent_w = (right - left) * 0.55
        vent_l = left + (right - left - vent_w) / 2
        vent_b = HEIGHT * 0.28
        vent_t = HEIGHT * 0.72

        arcade.draw_lrbt_rectangle_filled(
            vent_l, vent_l + vent_w, vent_b, vent_t, PANEL_PURPLE,
        )

        cell = 14
        for y in range(int(vent_b), int(vent_t), cell):
            for x in range(int(vent_l), int(vent_l + vent_w), cell):
                c = VENT_GRID if (x // cell + y // cell) % 2 == 0 else PANEL_PURPLE
                arcade.draw_lrbt_rectangle_filled(
                    x, x + cell, y, y + cell, c,
                )

        arcade.draw_lrbt_rectangle_outline(
            vent_l, vent_l + vent_w, vent_b, vent_t,
            FRAME_TEAL, 3,
        )

        for i in range(5):
            ry = 100 + i * 150
            rx = (left + right) / 2
            arcade.draw_circle_filled(rx, ry, 6, FRAME_TEAL_DARK)
            arcade.draw_circle_filled(rx - 1, ry + 1, 3, FRAME_TEAL)

    def draw_playfield_checkered(self):

        size = 22

        for y in range(
            int(PLAYFIELD_BOTTOM),
            int(PLAYFIELD_TOP),
            size,
        ):
            for x in range(
                int(PLAYFIELD_LEFT),
                int(PLAYFIELD_RIGHT),
                size,
            ):
                c = (
                    PLAYFIELD_BG_A
                    if (x // size + y // size) % 2 == 0
                    else PLAYFIELD_BG_B
                )
                arcade.draw_lrbt_rectangle_filled(
                    x, x + size, y, y + size, c,
                )

    def draw_playfield_frame(self):

        fw = 14
        bottom = PLAYFIELD_BOTTOM - 58
        top = PLAYFIELD_TOP + 8

        arcade.draw_lrbt_rectangle_filled(
            PLAYFIELD_LEFT - fw,
            PLAYFIELD_RIGHT + fw,
            top - 18,
            top,
            FRAME_TEAL,
        )

        arcade.draw_lrbt_rectangle_filled(
            PLAYFIELD_LEFT - fw,
            PLAYFIELD_RIGHT + fw,
            bottom,
            PLAYFIELD_BOTTOM - 10,
            FRAME_TEAL,
        )

        for l, r in (
            (PLAYFIELD_LEFT - fw, PLAYFIELD_LEFT),
            (PLAYFIELD_RIGHT, PLAYFIELD_RIGHT + fw),
        ):
            arcade.draw_lrbt_rectangle_filled(
                l, r, bottom, top, FRAME_TEAL,
            )

        arcade.draw_lrbt_rectangle_outline(
            PLAYFIELD_LEFT - fw,
            PLAYFIELD_RIGHT + fw,
            bottom,
            top,
            FRAME_TEAL_DARK,
            3,
        )

        for i in range(7):
            t = top - 30 - i * 115
            for x in (PLAYFIELD_LEFT - 7, PLAYFIELD_RIGHT + 7):
                arcade.draw_circle_filled(x, t, 5, FRAME_TEAL_DARK)
                arcade.draw_circle_filled(x - 1, t + 1, 2, FRAME_TEAL)

        for x in range(
            int(PLAYFIELD_LEFT - fw + 20),
            int(PLAYFIELD_RIGHT + fw - 10),
            55,
        ):
            arcade.draw_circle_filled(
                x, top - 9, 3, FRAME_TEAL_DARK,
            )
            arcade.draw_circle_filled(
                x, bottom + 9, 3, FRAME_TEAL_DARK,
            )

    def draw_ceiling_push_zone(self, bar_bottom, bar_top):

        if bar_top >= PLAYFIELD_TOP:
            return

        arcade.draw_lrbt_rectangle_filled(
            PLAYFIELD_LEFT,
            PLAYFIELD_RIGHT,
            bar_top,
            PLAYFIELD_TOP,
            CEILING_COLOR,
        )

        arcade.draw_lrbt_rectangle_filled(
            PLAYFIELD_LEFT,
            PLAYFIELD_RIGHT,
            PLAYFIELD_TOP - 6,
            PLAYFIELD_TOP,
            CEILING_COLOR_LIGHT,
        )

        for i in range(9):
            gx = PLAYFIELD_LEFT + 25 + i * 52
            arcade.draw_line(
                gx, bar_top, gx + 5, PLAYFIELD_TOP,
                CEILING_COLOR_DARK, 2,
            )

    def draw_ceiling_bar(self, bar_bottom, bar_top):

        arcade.draw_lrbt_rectangle_filled(
            PLAYFIELD_LEFT,
            PLAYFIELD_RIGHT,
            bar_bottom,
            bar_top,
            CEILING_COLOR,
        )

        arcade.draw_lrbt_rectangle_filled(
            PLAYFIELD_LEFT,
            PLAYFIELD_RIGHT,
            bar_top - 5,
            bar_top,
            CEILING_COLOR_LIGHT,
        )

        arcade.draw_lrbt_rectangle_filled(
            PLAYFIELD_LEFT,
            PLAYFIELD_RIGHT,
            bar_bottom,
            bar_bottom + 4,
            CEILING_COLOR_DARK,
        )

        arcade.draw_lrbt_rectangle_outline(
            PLAYFIELD_LEFT,
            PLAYFIELD_RIGHT,
            bar_bottom,
            bar_top,
            CEILING_COLOR_DARK,
            3,
        )

        for i in range(7):
            rx = PLAYFIELD_LEFT + 35 + i * (
                (PLAYFIELD_RIGHT - PLAYFIELD_LEFT - 70) / 6
            )
            ry = (bar_bottom + bar_top) / 2
            arcade.draw_circle_filled(rx, ry, 4, CEILING_COLOR_DARK)
            arcade.draw_circle_filled(rx - 1, ry + 1, 2, CEILING_COLOR_LIGHT)

    def draw_top_hud(self, score, stage, level):

        arcade.draw_text(
            f"LV{level}  S{stage:02d}",
            PLAYFIELD_LEFT + 8,
            PLAYFIELD_TOP + 40,
            arcade.color.CYAN,
            12,
            bold=True,
        )

        arcade.draw_text(
            "1UP",
            PLAYFIELD_LEFT + 8,
            PLAYFIELD_TOP + 20,
            arcade.color.GREEN,
            17,
            bold=True,
        )

        score_text = format_score(score)
        arcade.draw_text(
            score_text,
            PLAYFIELD_LEFT + 52,
            PLAYFIELD_TOP + 17,
            arcade.color.BLACK,
            19,
        )
        arcade.draw_text(
            score_text,
            PLAYFIELD_LEFT + 50,
            PLAYFIELD_TOP + 19,
            arcade.color.WHITE,
            19,
        )

    def draw_ceiling_hud(
            self,
            shots_left,
            time_left,
            fire_count,
            warning,
    ):

        left = 6
        right = PLAYFIELD_LEFT - 22
        bottom = HEIGHT - 112
        top = HEIGHT - 28
        cx = (left + right) / 2

        panel_color = (45, 68, 105) if not warning else (95, 55, 55)
        arcade.draw_lrbt_rectangle_filled(
            left, right, bottom, top, panel_color,
        )
        arcade.draw_lrbt_rectangle_outline(
            left, right, bottom, top, FRAME_TEAL, 2,
        )

        label_color = arcade.color.RED if warning else arcade.color.WHITE
        arcade.draw_text(
            "천장",
            cx,
            top - 16,
            label_color,
            12,
            anchor_x="center",
            bold=True,
        )

        arcade.draw_text(
            f"발{shots_left}/{fire_count}",
            cx,
            top - 38,
            label_color,
            14,
            anchor_x="center",
            bold=True,
        )

        arcade.draw_text(
            f"{max(0, int(time_left + 0.999))}초",
            cx,
            top - 58,
            label_color,
            13,
            anchor_x="center",
            bold=True,
        )

        arcade.draw_line(
            left + 8,
            bottom + 24,
            right - 8,
            bottom + 24,
            (255, 255, 255, 50),
            1,
        )

        if warning:
            arcade.draw_text(
                "WALL!",
                cx,
                bottom + 8,
                arcade.color.YELLOW,
                11,
                anchor_x="center",
                bold=True,
            )

    def draw_bottom_hud(self, level, stage, goal_score, current_score):

        arcade.draw_lrbt_rectangle_filled(
            PLAYFIELD_LEFT + 50,
            PLAYFIELD_RIGHT - 50,
            PLAYFIELD_BOTTOM - 52,
            PLAYFIELD_BOTTOM - 22,
            (18, 18, 32),
        )

        arcade.draw_text(
            f"LV{level}  STAGE {stage:02d}/{MAX_STAGE}",
            (PLAYFIELD_LEFT + PLAYFIELD_RIGHT) / 2,
            PLAYFIELD_BOTTOM - 44,
            arcade.color.WHITE,
            18,
            anchor_x="center",
            bold=True,
        )

        arcade.draw_text(
            "CREDIT 2",
            PLAYFIELD_RIGHT + 42,
            28,
            arcade.color.WHITE,
            14,
            anchor_x="center",
            bold=True,
        )

        remain = max(0, goal_score - current_score)
        arcade.draw_text(
            f"GOAL {format_score(goal_score)}",
            PLAYFIELD_LEFT + 12,
            PLAYFIELD_BOTTOM - 44,
            arcade.color.CYAN,
            12,
            bold=True,
        )
        arcade.draw_text(
            f"남은 {format_score(remain)}",
            PLAYFIELD_LEFT + 12,
            PLAYFIELD_BOTTOM - 58,
            arcade.color.LIGHT_GRAY,
            10,
        )

    def draw_launcher_area(self, shooter_x, shooter_y):

        arcade.draw_lrbt_rectangle_filled(
            shooter_x - 55,
            shooter_x + 55,
            shooter_y - 30,
            shooter_y - 10,
            (140, 100, 40),
        )

        arcade.draw_lrbt_rectangle_filled(
            shooter_x - 48,
            shooter_x + 48,
            shooter_y - 26,
            shooter_y - 14,
            (180, 140, 55),
        )

        self._draw_mini_dino(shooter_x - 70, shooter_y - 38, GREEN)
        self._draw_mini_dino(shooter_x + 58, shooter_y - 42, arcade.color.LIGHT_BLUE)

    def _draw_mini_dino(self, x, y, body_color):

        arcade.draw_ellipse_filled(
            x, y, 28, 22, body_color,
        )
        arcade.draw_ellipse_filled(
            x + 14, y + 6, 16, 14, body_color,
        )
        arcade.draw_circle_filled(x + 20, y + 10, 3, arcade.color.WHITE)
        arcade.draw_circle_filled(x + 21, y + 10, 1, arcade.color.BLACK)

    def draw_next_bubble(self, next_color):

        nx = PLAYFIELD_LEFT + 78
        ny = PLAYFIELD_BOTTOM - 88
        preview_r = BUBBLE_RADIUS + 2

        arcade.draw_lrbt_rectangle_filled(
            nx - 42, nx + 18, ny - 32, ny + 38,
            (95, 58, 32),
        )

        arcade.draw_polygon_filled(
            [
                (nx - 42, ny + 10),
                (nx - 58, ny - 5),
                (nx - 42, ny - 20),
            ],
            (75, 45, 25),
        )

        arcade.draw_text(
            "NEXT",
            nx - 12,
            ny + 24,
            arcade.color.CYAN,
            15,
            anchor_x="center",
            bold=True,
        )

        arcade.draw_circle_filled(nx - 8, ny - 4, preview_r, next_color)
        arcade.draw_circle_outline(
            nx - 8, ny - 4, preview_r, arcade.color.WHITE, 2,
        )

    def draw_danger_line(self, y):

        arcade.draw_line(
            PLAYFIELD_LEFT + 6,
            y,
            PLAYFIELD_RIGHT - 6,
            y,
            DANGER_LINE_COLOR,
            3,
        )

    def draw_session_panel(
            self,
            title,
            level,
            stage,
            score,
            play_seconds,
            subtitle=None,
            hints=None,
    ):

        arcade.draw_lrbt_rectangle_filled(
            0, WIDTH, 0, HEIGHT, (0, 0, 0, 160),
        )

        box_w = 420
        box_h = 320
        left = WIDTH / 2 - box_w / 2
        right = WIDTH / 2 + box_w / 2
        bottom = HEIGHT / 2 - box_h / 2
        top = HEIGHT / 2 + box_h / 2

        arcade.draw_lrbt_rectangle_filled(
            left, right, bottom, top, (35, 38, 58),
        )

        arcade.draw_lrbt_rectangle_outline(
            left, right, bottom, top, arcade.color.WHITE, 3,
        )

        arcade.draw_text(
            title, WIDTH / 2, top - 52,
            arcade.color.WHITE, 30, anchor_x="center",
        )

        if subtitle:
            arcade.draw_text(
                subtitle, WIDTH / 2, top - 88,
                arcade.color.LIGHT_GRAY, 16, anchor_x="center",
            )

        y = HEIGHT / 2 + 10
        for line in (
            f"LEVEL {level}  ·  STAGE {stage:02d} / {MAX_STAGE}",
            f"SCORE  {format_score(score)}",
            f"PLAY   {play_seconds:.1f}s",
        ):
            arcade.draw_text(
                line, WIDTH / 2, y,
                arcade.color.WHITE, 22, anchor_x="center",
            )
            y -= 38

        if hints:
            hy = bottom + 36
            for hint in hints:
                arcade.draw_text(
                    hint, WIDTH / 2, hy,
                    arcade.color.LIGHT_GRAY, 17, anchor_x="center",
                )
                hy += 26

    def draw_stage_clear(
            self,
            level,
            stage,
            clear_seconds,
            goal_score,
            current_score,
            is_final,
            clear_reason="score",
    ):

        arcade.draw_lrbt_rectangle_filled(
            0, WIDTH, 0, HEIGHT, (0, 0, 0, 200),
        )

        box_w = 460
        box_h = 360
        left = WIDTH / 2 - box_w / 2
        right = WIDTH / 2 + box_w / 2
        bottom = HEIGHT / 2 - box_h / 2
        top = HEIGHT / 2 + box_h / 2

        arcade.draw_lrbt_rectangle_filled(
            left, right, bottom, top, (28, 42, 72),
        )
        arcade.draw_lrbt_rectangle_outline(
            left, right, bottom, top, arcade.color.GOLD, 4,
        )

        if is_final:
            title = "ALL CLEAR!"
            sub = f"최종 LV{level} STAGE {stage} 클리어!"
        else:
            title = f"STAGE {stage:02d} 완료!"
            if clear_reason == "board":
                sub = "모든 공 제거!"
            else:
                sub = "목표 점수 달성!"

        arcade.draw_text(
            title,
            WIDTH / 2,
            top - 58,
            arcade.color.GOLD,
            34,
            anchor_x="center",
            bold=True,
        )

        arcade.draw_text(
            sub,
            WIDTH / 2,
            top - 98,
            arcade.color.CYAN,
            20,
            anchor_x="center",
        )

        arcade.draw_text(
            f"LEVEL {level}  ·  STAGE {stage:02d} / {MAX_STAGE}",
            WIDTH / 2,
            HEIGHT / 2 + 62,
            arcade.color.LIGHT_GRAY,
            16,
            anchor_x="center",
        )

        arcade.draw_text(
            f"SCORE  {format_score(current_score)} / {format_score(goal_score)}",
            WIDTH / 2,
            HEIGHT / 2 + 36,
            arcade.color.WHITE,
            22,
            anchor_x="center",
        )

        arcade.draw_text(
            f"클리어 시간  {clear_seconds:.1f}s",
            WIDTH / 2,
            HEIGHT / 2,
            arcade.color.LIGHT_GRAY,
            18,
            anchor_x="center",
        )

        if is_final:
            btn_left = WIDTH / 2 - 110
            btn_right = WIDTH / 2 + 110
            btn_bottom = HEIGHT / 2 - 90
            btn_top = HEIGHT / 2 - 30
            self._store_button(
                "menu",
                btn_left,
                btn_bottom,
                btn_right,
                btn_top,
            )
            self._draw_button("menu", "메뉴로", (90, 70, 130), 18)
            arcade.draw_text(
                "ENTER 키도 가능",
                WIDTH / 2,
                btn_bottom - 24,
                arcade.color.LIGHT_GRAY,
                14,
                anchor_x="center",
            )
        else:
            button_bottom = HEIGHT / 2 - 95
            self.layout_stage_clear_buttons(button_bottom)
            self._draw_button(
                "next_stage",
                f"다음 STAGE {stage + 1:02d}",
                (55, 145, 95),
                17,
            )
            self._draw_button("quit", "그만하기", (150, 70, 70), 17)
            arcade.draw_text(
                "ENTER 키도 가능",
                WIDTH / 2,
                button_bottom - 24,
                arcade.color.LIGHT_GRAY,
                14,
                anchor_x="center",
            )

    def layout_stage_clear_buttons(self, button_bottom):

        cx = WIDTH / 2
        w = 165
        h = 46
        gap = 18

        self._store_button(
            "next_stage",
            cx - w - gap / 2,
            button_bottom,
            cx - gap / 2,
            button_bottom + h,
        )
        self._store_button(
            "quit",
            cx + gap / 2,
            button_bottom,
            cx + w + gap / 2,
            button_bottom + h,
        )

    def next_button_hit(self, x, y):

        return self.button_hit("next_stage", x, y)

    def menu_button_hit(self, x, y):

        return self.button_hit("menu", x, y)

    def pause_button_hit(self, x, y):

        return self.button_hit("pause", x, y)

    def resume_button_hit(self, x, y):

        return self.button_hit("resume", x, y)

    def quit_button_hit(self, x, y):

        return self.button_hit("quit", x, y)

    def menu_start_button_hit(self, x, y):

        return self.button_hit("menu_start", x, y)

    def menu_help_button_hit(self, x, y):

        return self.button_hit("menu_help", x, y)

    def menu_dev_button_hit(self, x, y):

        return self.button_hit("menu_dev", x, y)

    def dev_back_button_hit(self, x, y):

        return self.button_hit("dev_back", x, y)

    def help_back_button_hit(self, x, y):

        return self.button_hit("help_back", x, y)

    def retry_button_hit(self, x, y):

        return self.button_hit("retry", x, y)

    def go_menu_button_hit(self, x, y):

        return self.button_hit("go_menu", x, y)
