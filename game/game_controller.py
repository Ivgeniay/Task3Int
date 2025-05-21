from random import random
from typing import Dict, List, Optional
from dice.dice import Dice
from game.player import Player
from own_random.fair_random import FairRandom
from dice.dice_parser import DiceParser
from own_random.hmac_calculator import HmacCalculator
from own_random.random_generator import RandomGenerator
from probability.table_generator import TableGenerator
from .cli_menu import CliMenu


class GameController:
    def __init__(self, dice_list: List[Dice]) -> None:
        self.dice_list: List[Dice] = dice_list
        self.user_dice = None
        self.computer_dice = None
        self.player_first_move = None

    def determine_first_move(self) -> Player:
        CliMenu.display_message("Let's determine who makes the first move.")

        fair_random = FairRandom(0, 1)
        hmac: str = fair_random.initiate_generation()

        CliMenu.display_message(
            f"I selected a random value in the range 0..1 (HMAC={hmac}).")
        CliMenu.display_message("Try to guess my selection.")

        options: List[Dict[str, str]] = fair_random.get_options()
        user_selection: str = CliMenu.display_menu("", options)

        if user_selection.lower() == "x":
            exit()
        elif user_selection.lower() == "h":
            self.show_help()
            return self.determine_first_move()

        user_number = int(user_selection)
        computer_number, result, key = fair_random.calculate_result(
            user_number)

        CliMenu.display_message(
            f"My selection: {computer_number} (KEY={key.hex().upper()}).")

        if result == 0:
            self.player_first_move = Player.USER
            CliMenu.display_message("You make the first move.")
        else:
            self.player_first_move = Player.COMPUTER
            CliMenu.display_message("I make the first move.")

        return self.player_first_move

    def select_dice(self, player: Player) -> Dice:
        if player == Player.USER:
            available_dice: List[Dice] = [
                dice for dice in self.dice_list if dice != self.computer_dice]
            options = []

            for i, dice in enumerate(available_dice):
                options.append({"value": str(i), "description": str(dice)})

            options.append({"value": "x", "description": "exit"})
            options.append({"value": "h", "description": "help"})
            options.append({"value": "c", "description": "check HMAC"})

            title = "Choose your dice:"
            user_selection: str = CliMenu.display_menu(title, options)

            if user_selection.lower() == "x":
                exit()
            elif user_selection.lower() == "h":
                self.show_help()
                return self.select_dice(player)
            elif user_selection.lower() == "c":
                CliMenu.display_message(
                    "Enter key, message and HMAC separated by spaces:")
                CliMenu.display_message("Format: KEY MESSAGE HMAC")
                CliMenu.display_message(
                    "Example: 9B3C1734EBE66A2862F4CEF1F571192CFAB136AEE28B82982C73409B2A1FAD50 0 ABF90F066F2F84BBBF32DBCBBCE70AF8D36ADC751CAE2AA7377E0BF4BAB435E7")

                check_input: List[str] = input(
                    "Enter verification data: ").strip().split()
                if len(check_input) == 3:
                    key_hex, message, shown_hmac = check_input
                    HmacCalculator.check_hmac(
                        key_hex, message, shown_hmac, True)
                else:
                    CliMenu.display_error(
                        "Invalid input format. Expected: KEY MESSAGE HMAC")

                return self.select_dice(player)

            selected_dice: Dice = available_dice[int(user_selection)]
            self.user_dice: Dice = selected_dice
            CliMenu.display_message(f"You choose the [{selected_dice}] dice.")

            return selected_dice

        if player == Player.COMPUTER:
            available_dice = [
                dice for dice in self.dice_list if dice != self.user_dice]

            if self.user_dice:
                best_dice = None
                best_prob = -1

                for dice in available_dice:
                    prob: float = dice.probability_to_win(self.user_dice)
                    if prob > best_prob:
                        best_prob: float = prob
                        best_dice: Dice = dice

                selected_dice = best_dice
            else:
                selected_dice = available_dice[RandomGenerator.generate_random_int(
                    0, len(available_dice) - 1)]

            self.computer_dice: Dice = selected_dice
            CliMenu.display_message(f"I choose the [{selected_dice}] dice.")

            return selected_dice

    def perform_roll(self, player: Player) -> int:
        dice: Dice = self.user_dice if player == Player.USER else self.computer_dice

        if dice is None:
            raise RuntimeError("Dice not selected")

        CliMenu.display_message(
            f"It's time for {'your' if player == Player.USER else 'my'} roll.")

        fair_random = FairRandom(0, dice.size - 1)
        hmac: str = fair_random.initiate_generation()

        CliMenu.display_message(
            f"I selected a random value in the range 0..{dice.size - 1} (HMAC={hmac}).")
        CliMenu.display_message(f"Add your number modulo {dice.size}.")

        options: List[Dict[str, str]] = fair_random.get_options()
        options.append({"value": "c", "description": "check HMAC"})

        user_selection: str = CliMenu.display_menu("", options)

        if user_selection.lower() == "x":
            exit()
        elif user_selection.lower() == "h":
            self.show_help()
            return self.perform_roll(player)
        elif user_selection.lower() == "c":
            CliMenu.display_message(
                "Enter key, message and HMAC separated by spaces:")
            CliMenu.display_message("Format: KEY MESSAGE HMAC")
            CliMenu.display_message(
                "Example: 9B3C1734EBE66A2862F4CEF1F571192CFAB136AEE28B82982C73409B2A1FAD50 0 ABF90F066F2F84BBBF32DBCBBCE70AF8D36ADC751CAE2AA7377E0BF4BAB435E7")

            check_input = input("Enter verification data: ").strip().split()
            if len(check_input) == 3:
                key_hex, message, shown_hmac = check_input
                HmacCalculator.check_hmac(key_hex, message, shown_hmac, True)
            else:
                CliMenu.display_error(
                    "Invalid input format. Expected: KEY MESSAGE HMAC")

            return self.perform_roll(player)

        user_number = int(user_selection)
        computer_number, result, key = fair_random.calculate_result(
            user_number)

        CliMenu.display_message(
            f"My number is {computer_number} (KEY={key.hex().upper()}).")
        CliMenu.display_message(
            f"The fair number generation result is {computer_number} + {user_number} = {result} (mod {dice.size}).")

        roll_result: int = dice.get_face_by_random_value(result)

        CliMenu.display_message(
            f"{'Your' if player == Player.USER else 'My'} roll result is {roll_result}.")

        return roll_result

    def play_game(self) -> None:
        first_player: Player = self.determine_first_move()

        if first_player == Player.USER:
            self.select_dice(Player.USER)
            self.select_dice(Player.COMPUTER)
        else:
            self.select_dice(Player.COMPUTER)
            self.select_dice(Player.USER)

        user_roll: int = self.perform_roll(Player.USER)
        computer_roll: int = self.perform_roll(Player.COMPUTER)

        user_win: bool = user_roll > computer_roll
        CliMenu.display_result(user_win, user_roll, computer_roll)

    def show_help(self) -> None:
        help_text: str = TableGenerator.generate_probability_table(
            self.dice_list)
        CliMenu.display_help(help_text)
