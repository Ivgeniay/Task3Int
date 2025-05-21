from operator import le


# TODO: float validation
# TODO: more than 2 arguments
# TODO: equal edge all dice
class Validator:
    def __init__(self) -> None:
        pass

    def validate_args(self, data) -> bool:
        if len(data) < 2:
            print("Error: insufficient arguments")
            return False

        first_arg_l = len(data[0])

        for i in range(1, len(data)):
            if (len(data[i]) != first_arg_l):
                print(f"Error: arguments are not the same length")
                return False

        return True
