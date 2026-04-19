import os

from dataclasses import dataclass

from three_card_poker_des.sim_config import SimConfig


@dataclass
class SimStats:
    high_card: int = 0
    pair: int = 0
    flush: int = 0
    straight: int = 0
    three_of_a_kind: int = 0
    straight_flush: int = 0
    player_bets: int = 0
    win: int = 0
    push: int = 0
    lost: int = 0
    pair_plus: int = 0
    money: int = 0
    hands_played: int = 0


    def display_stats(self, config: SimConfig) -> None:
        os.system("clear")
        print(f"Estadísticas de {config.hands} manos de Three Card Poker")
        print()
        print(f"Dinero inicial: {config.initial_money}")
        print(f"Dinero final: {self.money}")
        print()
        print(f"Valor de apuesta por mano: {config.bet_size}")
        print(f"Valor de apuesta en pair plus: {config.pair_plus_bet}")
        print()
        print(f"Cuantas veces apostó el jugador: {self.player_bets}")
        print()
        print(f"Ganadas: {self.win}")
        print(f"Empatadas: {self.push}")
        print(f"Perdidas: {self.lost}")
        print()
        print(f"High card: {self.high_card}")
        print(f"Par: {self.pair}")
        print(f"Color: {self.flush}")
        print(f"Corrida: {self.straight}")
        print(f"Tercia: {self.three_of_a_kind}")
        print(f"Flor corrida: {self.straight_flush}")
        print()
        print(f"Resultados pair plus: {self.pair_plus}")
