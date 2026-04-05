from three_card_poker_des.state import State
from three_card_poker_des.events import(
    deal_cards, player_turn,
)



def handle_round_started(state, event, now):
    if state.round_state != State.RoundState.READY:
        raise ValueError("ROUND_STARTED is only valid in READY state")
    
    state.round_state = State.RoundState.DEALING

    return [deal_cards(time=now+1)]


def handle_deal_cards(state, event, now):
    if state.round_state != State.RoundState.DEALING:
        raise ValueError("DEAL_CARDS is only valid in DEALING state")
    
    state.round.deck.burn()
    
    for card in state.round.deck.draw(3):
        state.round.player_hand.add_card(card)

    for card in state.round.deck.draw(3):
        state.round.dealer_hand.add_card(card)

    state.round_state = State.RoundState.PLAYER_ACTING

    return [player_turn(time=now+1)]


def handle_player_turn(state, event, now):
    if state.round_state != State.RoundState.PLAYER_ACTING:
        raise ValueError("PLAYER_TURN is only valid in PLAYER_ACTING state")

 
def handle_player_bet(state, event, now):
    pass


def handle_dealer_turn(state, event, now):
    pass


def handle_resolve_round(state, event, now):
    pass


def handle_round_finished(state, event, now):
    pass