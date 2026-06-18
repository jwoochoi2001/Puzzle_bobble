import sys
import traceback

import arcade

from game.game import Game


def main():

    try:
        window = Game()
        arcade.run()

    except Exception:
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
