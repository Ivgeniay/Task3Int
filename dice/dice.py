from typing import List, Tuple


class Dice:
    def __init__(self, faces: List[int]) -> None:
        self.faces: List[int] = faces
        self.size: int = len(faces)

    def get_face(self, index: int) -> int:
        if 0 <= index < self.size:
            return self.faces[index]
        raise ValueError(
            f"Invalid face index: {index}. Must be between 0 and {self.size-1}")

    def get_all_faces(self) -> List[int]:
        return self.faces.copy()

    def __str__(self) -> str:
        return ','.join(map(str, self.faces))

    def probability_to_win(self, other_dice: 'Dice') -> float:
        if self is other_dice or self.faces == other_dice.faces:
            return 0.5

        wins = 0
        total_outcomes: int = self.size * other_dice.size

        for my_face in self.faces:
            for other_face in other_dice.faces:
                if my_face > other_face:
                    wins += 1

        return wins / total_outcomes

    def get_face_by_random_value(self, random_value: int) -> int:
        if random_value < 0 or random_value >= self.size:
            raise ValueError(
                f"Random value must be between 0 and {self.size-1}")
        return self.faces[random_value]
