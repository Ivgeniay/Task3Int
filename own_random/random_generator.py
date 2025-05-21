import secrets


class RandomGenerator:
    @staticmethod
    def generate_secret_key(length: int = 32) -> bytes:
        return secrets.token_bytes(length)

    @staticmethod
    def generate_random_int(min_value: int, max_value: int) -> int:
        if min_value > max_value:
            raise ValueError(
                "Minimum value cannot be greater than maximum value")

        if min_value == max_value:
            return min_value

        # min_value = 3 & max_value = 6
        # max_value - min_value + 1 = 6 - 3 + 1 = 4
        # secrets.randbelow(4) = 0, 1, 2, 3
        # 3 + [0,1,2,3] <= max_value
        return min_value + secrets.randbelow(max_value - min_value + 1)
