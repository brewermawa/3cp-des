import os

from dataclasses import dataclass


@dataclass
class SimConfig:
    game_mode: int = 0
    hands: int = 0
    initial_money: int = 0
    bet_size: int = 0
    pair_plus_bet: int = 0


    def player_input(self):
        os.system("clear")

        print("Choose Game Mode")
        print("1) Play a number of hands")
        print("2) Play until money runs out or a number of hands")

        while True:
            game_mode = input("Select game mode (1 or 2): ")
            if game_mode in ["1", "2"]:
                break

        self.game_mode = int(game_mode)

        print()
        while True:
            hands = input("Enter number of hands: ")

            try:
                hands = int(hands)
            except (ValueError, TypeError):
                hands = None

            if hands and hands > 0:
                break

        self.hands = hands

        if self.game_mode == 2:
            print()
            while True:
                initial_money = input("Enter initial money: ")

                try:
                    initial_money = int(initial_money)
                except (ValueError, TypeError):
                    initial_money = None

                if initial_money and initial_money > 0:
                    break

            self.initial_money = initial_money


        print()
        while True:
            bet_size = input("Enter bet size: ")

            try:
                bet_size = int(bet_size)
            except (ValueError, TypeError):
                bet_size = None

            if bet_size and bet_size > 0:
                break

        self.bet_size = bet_size


        print()
        while True:
            pair_plus_bet = input("Enter pair plus bet (0 for no bet): ")

            try:
                pair_plus_bet = int(pair_plus_bet)
            except (ValueError, TypeError):
                pair_plus_bet = None

            if pair_plus_bet is not None and pair_plus_bet >= 0:
                break

        self.pair_plus_bet = pair_plus_bet





