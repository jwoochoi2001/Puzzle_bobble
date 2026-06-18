from enum import Enum


class GameState(Enum):

    MENU = 0
    PLAYING = 1
    PAUSED = 2
    STAGE_CLEAR = 3
    GAME_OVER = 4
    VICTORY = 5
    HELP = 6
    DEVELOPER = 7
