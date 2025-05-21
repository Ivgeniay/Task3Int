from typing import Dict, List, Tuple
from own_random.hmac_calculator import HmacCalculator
from own_random.random_generator import RandomGenerator


class FairRandom:
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value: int = min_value
        self.max_value: int = max_value
        self.computer_number = None
        self.secret_key = None
        self.hmac_value = None

    def initiate_generation(self) -> str:
        self.computer_number: int = RandomGenerator.generate_random_int(
            self.min_value, self.max_value)
        self.secret_key: bytes = RandomGenerator.generate_secret_key()
        self.hmac_value: str = HmacCalculator.calculate(
            self.secret_key, self.computer_number)

        return self.hmac_value

    def calculate_result(self, user_number: int) -> Tuple[int, int, bytes]:
        if self.computer_number is None or self.secret_key is None or self.hmac_value is None:
            raise RuntimeError("Generation not initiated")

        if self.min_value > user_number or user_number > self.max_value:
            raise ValueError(
                f"User number must be between {self.min_value} and {self.max_value}")

        result: int = (self.computer_number +
                       user_number) % (self.max_value - self.min_value + 1)
        return self.computer_number, result, self.secret_key

    def get_options(self) -> List[Dict[str, str]]:
        options = []
        for i in range(self.min_value, self.max_value + 1):
            options.append({"value": str(i), "description": str(i)})
        options.append({"value": "x", "description": "exit"})
        options.append({"value": "h", "description": "help"})
        return options
