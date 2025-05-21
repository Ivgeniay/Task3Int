from typing import List
from dice.dice import Dice
from dice.dice_parser import DiceParser
from game.cli_menu import CliMenu
from game.game_controller import GameController


def main() -> int:
    dice_list, error = DiceParser.parse_args()
    if error:
        CliMenu.display_error(error)
        CliMenu.display_help(DiceParser.get_usage_example())
        return 1

    try:
        game = GameController(dice_list)
        game.play_game()
    except Exception as e:
        CliMenu.display_error(str(e))
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
