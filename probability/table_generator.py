from typing import List, LiteralString
from dice.dice import Dice
from probability.probability_calculator import ProbabilityCalculator


class TableGenerator:

    @staticmethod
    def generate_probability_table(dice_list: List[Dice]) -> str:
        matrix: List[List[float]] = ProbabilityCalculator.calculate_probabilities_matrix(
            dice_list)

        dice_str_list: List[str] = [str(dice) for dice in dice_list]
        max_dice_len: int = max(len(s) for s in dice_str_list)
        max_dice_len = max(max_dice_len, len("User dice v"))

        result: List[str] = ["Probability of the win for the user:"]

        header = f"+{'-' * (max_dice_len + 2)}+"
        for dice_str in dice_str_list:
            header += f"{'-' * (max(len(dice_str), 8) + 2)}+"
        result.append(header)

        header_row: LiteralString = f"| {'User dice v'.ljust(max_dice_len)} |"
        for dice_str in dice_str_list:
            header_row += f" {dice_str.ljust(max(len(dice_str), 8))} |"
        result.append(header_row)

        separator: LiteralString = f"+{'-' * (max_dice_len + 2)}+"
        for dice_str in dice_str_list:
            separator += f"{'-' * (max(len(dice_str), 8) + 2)}+"
        result.append(separator)

        for i, dice in enumerate(dice_list):
            row: str = f"| {str(dice).ljust(max_dice_len)} |"
            for j, prob in enumerate(matrix[i]):
                value: str = f"{prob:.4f}"
                if i == j:
                    value = f"- ({value})"
                row += f" {value.ljust(max(len(dice_str_list[j]), 8))} |"
            result.append(row)
            result.append(separator)

        return "\n".join(result)
