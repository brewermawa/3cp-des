from three_card_poker_des.state import State
from three_card_poker_des.events import deal_cards



def handle_round_started(state, event, now):
    if state.round_state != State.RoundState.READY:
        raise ValueError("ROUND_STARTED is only valid in READY state")
    
    state.round_state = State.RoundState.DEALING

    return [deal_cards(time=now+1)]


def handle_deal_cards(state, event, now):
    if state.round_state != State.RoundState.DEALING:
        raise ValueError("DEAl_CARDS is only valid in DEALING state")
    
    state.round_state = State.RoundState.PLAYER_ACTING


def handle_player_turn(state, event, now):
    pass


def handle_player_bet(state, event, now):
    pass


def handle_player_turn_completed(state, event, now):
    pass


def handle_dealer_turn(state, event, now):
    pass


def handle_dealer_turn_completed(state, event, now):
    pass


def handle_resolve_round(state, event, now):
    pass


def handle_round_finished(state, event, now):
    pass