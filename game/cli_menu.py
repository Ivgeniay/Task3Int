from typing import Dict, List


class CliMenu:

    @staticmethod
    def display_menu(title: str, options: List[Dict[str, str]]) -> str:
        print(title)
        for option in options:
            print(f"{option['value']} - {option['description']}")

        while True:
            user_input: str = input("Your selection: ").strip().lower()
            for option in options:
                if user_input == option['value'].lower():
                    return option['value']

            print("Invalid option, please try again")

    @staticmethod
    def display_message(message: str) -> None:
        print(message)

    @staticmethod
    def display_error(error_message: str) -> None:
        print(f"Error: {error_message}")

    @staticmethod
    def display_result(win: bool, user_roll: int, computer_roll: int) -> None:
        if win:
            print(f"You win ({user_roll} > {computer_roll})!")
        else:
            print(f"Computer wins ({computer_roll} > {user_roll})!")

    @staticmethod
    def display_help(help_text: str) -> None:
        print("\nHelp:")
        print(help_text)
        print()
