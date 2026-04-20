from three_card_poker_des.engine.core import run_simulation
from three_card_poker_des.events import round_started
from three_card_poker.three_card_poker import ThreeCardPoker
from three_card_poker_des.router import handlers
from three_card_poker_des.state import State
from three_card_poker_des.sim_config import SimConfig
from three_card_poker_des.sim_stats import SimStats
from three_card_poker.three_card_poker_rank import ThreeCardPokerRank
from cards import Deck, Hand

def simulation_stop_condition(config: SimConfig, hands_played: int, money: int) -> bool:
    if config.game_mode == 1:
        return hands_played == config.hands
    
    return money > (config.bet_size * 2 + config.pair_plus_bet)

config = SimConfig()
config.player_input()

stats = SimStats()
stats.money = config.initial_money


hands_played = 0
while not simulation_stop_condition(config, hands_played, stats.money):
    deck = Deck()
    deck.shuffle()

    round = ThreeCardPoker(deck=deck)
    state = State(round=round)
    state.round.player_hand = Hand()
    state.round.dealer_hand = Hand()
    state.round_state = State.RoundState.READY

    def stop_condition(state, now, events_processed, metrics):
        return state.round_state == State.RoundState.DONE

    simulation_result = run_simulation(
        initial_state=state,
        initial_events=[round_started(time=0)],
        handlers=handlers,
        stop_condition=stop_condition,
        observers=None,
        max_events=100
    )

    match state.outcomes:
        case State.RoundOutcome.PLAYER_WINS:
            stats.win += 1
            if state.dealer_qualified:
                stats.money += (config.bet_size * 2)
            else:
                stats.money += config.bet_size

        case State.RoundOutcome.DEALER_WINS:
            stats.lost += 1
            if state.player_bet:
                stats.money -= (config.bet_size * 2)
            else:
                stats.money -= config.bet_size

        case State.RoundOutcome.PUSH:
            stats.push += 1


    match state.player_hand_rank:
        case ThreeCardPokerRank.HIGH_CARD:
            stats.high_card += 1
        case ThreeCardPokerRank.PAIR:
            stats.pair += 1
        case ThreeCardPokerRank.FLUSH:
            stats.flush += 1
        case ThreeCardPokerRank.STRAIGHT:
            stats.straight += 1
        case ThreeCardPokerRank.THREE_OF_A_KIND:
            stats.three_of_a_kind += 1
        case ThreeCardPokerRank.STRAIGHT_FLUSH:
            stats.straight_flush += 1

    if state.pair_plus_multiplier == 0:
        stats.pair_plus -= config.pair_plus_bet
        stats.money -= config.pair_plus_bet
    else:
        stats.pair_plus += (config.pair_plus_bet + config.pair_plus_bet * state.pair_plus_multiplier)
        stats.money += (config.pair_plus_bet + config.pair_plus_bet * state.pair_plus_multiplier)

    if state.ante_bonus > 0:
        stats.money += (state.ante_bonus * config.bet_size)

    hands_played += 1


stats.display_stats(config)
