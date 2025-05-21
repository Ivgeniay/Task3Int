import sys
from typing import List, Tuple
from dice import Dice


class DiceParser:

    @staticmethod
    def parse_args() -> Tuple[List[Dice], str]:
        if len(sys.argv) < 2:
            return [], "No dice configurations provided"

        dice_configs: List[str] = sys.argv[1:]

        if len(dice_configs) < 3:
            return [], "At least 3 dice configurations are required"

        dice_list = []

        for i, config in enumerate(dice_configs):
            try:
                dice: Dice = DiceParser.parse_dice(config)
                dice_list.append(dice)
            except ValueError as e:
                return [], f"Invalid dice configuration at position {i+1}: {str(e)}"

        first_dice_size = dice_list[0].size
        for i, dice in enumerate(dice_list[1:], 1):
            if dice.size != first_dice_size:
                return [], f"All dice must have the same number of faces. Dice {i+1} has {dice.size} faces, but dice 1 has {first_dice_size} faces."

        return dice_list, ""

    @staticmethod
    def parse_dice(config: str) -> Dice:
        try:
            source: List[str] = config.split(',')
            faces: List[int] = [int(face) for face in source]

            if not faces:
                raise ValueError("Empty dice configuration")

            if len(faces) > 6:
                raise ValueError(
                    f"Each dice must have exactly 6 faces, but got {len(faces)}")

            return Dice(faces)
        except ValueError as e:
            if str(e).startswith("invalid literal for int"):
                raise ValueError("Non-integer value in dice configuration")
            raise

    @staticmethod
    def get_usage_example() -> str:
        return ("""Usage: python main.py <dice1> <dice2> <dice3> [...] 
Example: python main.py 2,2,4,4,9,9 6,8,1,1,8,6 7,5,3,7,5,3 
Each dice configuration must consist of less than 6 comma-separated integers.
All dice must have the same number of faces.""")
