from three_card_poker_des.engine.core import run_simulation
from three_card_poker_des.events import round_started
from three_card_poker.three_card_poker import ThreeCardPoker
from three_card_poker_des.router import handlers
from three_card_poker_des.state import State
from cards import Deck, Hand

deck = Deck()
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

print()
print()
print(simulation_result)
