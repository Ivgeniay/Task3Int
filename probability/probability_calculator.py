from typing import List
from dice.dice import Dice


class ProbabilityCalculator:

    @staticmethod
    def calculate_win_probability(dice1: Dice, dice2: Dice) -> float:
        return dice1.probability_to_win(dice2)

    @staticmethod
    def calculate_probabilities_matrix(dice_list: List[Dice]) -> List[List[float]]:
        n: int = len(dice_list)
        matrix = []

        for i in range(n):
            row = []
            for j in range(n):
                row.append(dice_list[i].probability_to_win(dice_list[j]))
            matrix.append(row)

        return matrix
