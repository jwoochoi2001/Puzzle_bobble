# settings.py

import math

WIDTH = 900
HEIGHT = 920

FPS = 60
TITLE = "Puzzle Bobble"

SIDE_PANEL_WIDTH = 155
PLAYFIELD_LEFT = SIDE_PANEL_WIDTH
PLAYFIELD_RIGHT = WIDTH - SIDE_PANEL_WIDTH
PLAYFIELD_BOTTOM = 165
PLAYFIELD_TOP = HEIGHT - 95

PLAYFIELD_WIDTH = PLAYFIELD_RIGHT - PLAYFIELD_LEFT

# 나도코딩: MAP_ROW_COUNT = 11
GRID_ROWS = 11
GRID_COLS = 8
ODD_ROW_COLS = GRID_COLS - 1

BUBBLE_DIAMETER = PLAYFIELD_WIDTH // GRID_COLS
BUBBLE_RADIUS = BUBBLE_DIAMETER // 2
ROW_HEIGHT = BUBBLE_RADIUS * math.sqrt(3)

GRID_ORIGIN_X = PLAYFIELD_LEFT + BUBBLE_RADIUS

CEILING_BAR_THICKNESS = 26
CEILING_BAR_GAP = 5
CEILING_COLOR = (55, 145, 155)
CEILING_COLOR_DARK = (30, 95, 110)
CEILING_COLOR_LIGHT = (100, 200, 210)

FRAME_TEAL = (65, 155, 165)
FRAME_TEAL_DARK = (35, 105, 120)
PANEL_BLUE = (45, 95, 145)
PANEL_PURPLE = (72, 38, 105)
VENT_GRID = (95, 55, 130)
PLAYFIELD_BG_A = (58, 32, 88)
PLAYFIELD_BG_B = (42, 22, 68)
DANGER_LINE_COLOR = (220, 185, 60)

GRID_TOP_Y = (
    PLAYFIELD_TOP
    - CEILING_BAR_THICKNESS
    - CEILING_BAR_GAP
    - BUBBLE_RADIUS
)

CEILING_WALL_Y = GRID_TOP_Y + BUBBLE_RADIUS
CEILING_BAR_BOTTOM = PLAYFIELD_TOP - CEILING_BAR_THICKNESS
CEILING_BAR_TOP = PLAYFIELD_TOP

WALL_INNER_LEFT = PLAYFIELD_LEFT + BUBBLE_RADIUS
WALL_INNER_RIGHT = PLAYFIELD_RIGHT - BUBBLE_RADIUS

# 나도코딩 6_pointer_fire: radius = 18
SHOOT_SPEED = 18
ANGLE_SPEED = 1.5
POINTER_MIN_ANGLE = math.radians(10)
POINTER_MAX_ANGLE = math.radians(170)

DEAD_LINE_Y = PLAYFIELD_BOTTOM + 100

MIN_MATCH = 3
MAX_STAGE = 30
MAX_LEVEL = 6
MAX_DISPLAY_SCORE = 99999

# 레벨별 스테이지 구간 (같은 레벨 = 같은 천장 속도)
# 레벨1: 1~3, 레벨2: 4~9, 레벨3: 10~15, 레벨4: 16~21, 레벨5: 22~27, 레벨6: 28~30
LEVEL_STAGE_END = {
    1: 3,
    2: 9,
    3: 15,
    4: 21,
    5: 27,
    6: 30,
}

# 단계별 클리어 목표 점수 (누적 총점, 5자리 이내)
STAGE_SCORE_GOALS = {
    1: 350,
    2: 750,
    3: 1200,
    4: 1750,
    5: 2400,
    6: 3150,
    7: 4000,
    8: 4950,
    9: 6000,
    10: 7200,
    11: 8500,
    12: 9900,
    13: 11400,
    14: 13100,
    15: 14900,
    16: 16800,
    17: 18800,
    18: 20900,
    19: 23100,
    20: 25400,
    21: 27800,
    22: 30300,
    23: 32900,
    24: 35600,
    25: 38400,
    26: 41300,
    27: 44300,
    28: 47400,
    29: 50600,
    30: 53900,
}

# 매칭 터뜨린 공 1개당 / 떨어진 공 1개당
MATCH_BUBBLE_SCORE = 10
FLOATING_BUBBLE_SCORE = 20

# 연속 턴 매칭 시 추가 보너스 (2연속 +15, 3연속 +30 ...)
COMBO_BONUS_PER_STEP = 15

# 천장 하강 기본값 (단계가 올라갈수록 stage_ceiling_settings에서 감소)
FIRE_COUNT = 7
MIN_FIRE_COUNT = 4
DROP_WARNING_SHOTS = 2

CEILING_DROP_SECONDS = 28
MIN_CEILING_DROP_SECONDS = 14
DROP_WARNING_SECONDS = 6
MIN_DROP_WARNING_SECONDS = 3

# 공 터짐·낙하 연출
POP_EFFECT_DURATION = 0.38
FALL_EFFECT_DURATION = 1.35
FALL_GRAVITY = 1100
SCORE_FLOAT_DURATION = 0.85

WHITE = (255, 255, 255)
BLACK = (30, 30, 30)

RED = (255, 80, 80)
GREEN = (80, 220, 80)
BLUE = (80, 120, 255)
YELLOW = (255, 220, 50)
PURPLE = (180, 80, 255)
CYAN = (50, 220, 255)

COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE, CYAN]

CHAR_TO_COLOR = {
    "R": RED,
    "Y": YELLOW,
    "B": BLUE,
    "G": GREEN,
    "P": PURPLE,
}


def cols_for_row(row):

    if row % 2 == 0:
        return GRID_COLS
    return ODD_ROW_COLS


def format_score(score):

    clamped = max(0, min(int(score), MAX_DISPLAY_SCORE))
    return f"{clamped:05d}"


def stage_to_level(stage):

    stage = min(max(stage, 1), MAX_STAGE)

    if stage <= LEVEL_STAGE_END[1]:
        return 1
    if stage <= LEVEL_STAGE_END[2]:
        return 2
    if stage <= LEVEL_STAGE_END[3]:
        return 3
    if stage <= LEVEL_STAGE_END[4]:
        return 4
    if stage <= LEVEL_STAGE_END[5]:
        return 5

    return 6


def stage_score_goal(stage):

    stage = min(max(stage, 1), MAX_STAGE)
    return min(STAGE_SCORE_GOALS[stage], MAX_DISPLAY_SCORE)


def stage_color_count(stage):

    level = stage_to_level(stage)
    return min(2 + level, 6)


def level_ceiling_settings(level):

    """레벨별 천장 하강 속도 (같은 레벨은 동일)."""

    level = min(max(level, 1), MAX_LEVEL)

    if MAX_LEVEL <= 1:
        t = 0.0
    else:
        t = (level - 1) / (MAX_LEVEL - 1)

    fire_count = round(
        FIRE_COUNT - t * (FIRE_COUNT - MIN_FIRE_COUNT),
    )
    drop_seconds = (
        CEILING_DROP_SECONDS
        - t * (CEILING_DROP_SECONDS - MIN_CEILING_DROP_SECONDS)
    )
    warning_seconds = (
        DROP_WARNING_SECONDS
        - t * (DROP_WARNING_SECONDS - MIN_DROP_WARNING_SECONDS)
    )

    return {
        "fire_count": max(MIN_FIRE_COUNT, fire_count),
        "drop_seconds": max(MIN_CEILING_DROP_SECONDS, drop_seconds),
        "warning_shots": DROP_WARNING_SHOTS,
        "warning_seconds": max(
            MIN_DROP_WARNING_SECONDS,
            warning_seconds,
        ),
    }


def stage_ceiling_settings(stage):

    return level_ceiling_settings(stage_to_level(stage))
