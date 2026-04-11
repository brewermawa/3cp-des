from three_card_poker_des.state import State
from three_card_poker_des.events import(
    deal_cards, player_turn, resolve_round, dealer_turn, round_finished
)
from three_card_poker.three_card_poker_rank import ThreeCardPokerRank
from three_card_poker.three_card_poker_eval import ThreeCardPokerEval



def handle_round_started(state, event, now):
    if state.round_state != State.RoundState.READY:
        raise ValueError("ROUND_STARTED is only valid in READY state")
    
    print()
    print("ROUND STARTED")
    
    state.round_state = State.RoundState.DEALING

    return [deal_cards(time=now+1)]


def handle_deal_cards(state, event, now):
    if state.round_state != State.RoundState.DEALING:
        raise ValueError("DEAL_CARDS is only valid in DEALING state")
    
    print("DEAL CARDS")
    
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

    eval_result = ThreeCardPokerEval.eval(state.round.player_hand)
    state.player_hand_rank = eval_result["rank"]
    
    if state.player_hand_rank == ThreeCardPokerRank.HIGH_CARD:
        player_hand_cards = eval_result["sorted_hand"]
        if player_hand_cards < [12, 6, 4]:
            state.round_state = State.RoundState.RESOLVING
            return [resolve_round(time=now+1)]
        
    state.player_bet = True
    state.round_state = State.RoundState.DEALER_ACTING
    return [dealer_turn(time=now+1)]
    

 
def handle_dealer_turn(state, event, now):
    if state.round_state != State.RoundState.DEALER_ACTING:
        raise ValueError("DEALER_TURN is only valid in DEALER_ACTING state")
    
    eval_result = ThreeCardPokerEval.eval(state.round.dealer_hand)
    state.dealer_hand_rank = eval_result["rank"]


    state.dealer_qualified = (
        (state.dealer_hand_rank == ThreeCardPokerRank.HIGH_CARD and eval_result["sorted_hand"] >= [12, 3, 2])
        or
        (state.dealer_hand_rank in [
            ThreeCardPokerRank.PAIR,
            ThreeCardPokerRank.STRAIGHT,
            ThreeCardPokerRank.FLUSH,
            ThreeCardPokerRank.THREE_OF_A_KIND,
            ThreeCardPokerRank.STRAIGHT_FLUSH
        ])
    )
    
    state.round_state = State.RoundState.RESOLVING
    
    return [resolve_round(time=now+1)]


def handle_resolve_round(state, event, now):
    if state.round_state != State.RoundState.RESOLVING:
        raise ValueError("RESOLVE_ROUND is only valid in RESOLVING state")
    
    if not state.player_bet:
        state.outcomes = State.RoundOutcome.DEALER_WINS
    
    
    state.round_state = State.RoundState.DONE    
    return [round_finished(time=now+1)]

def handle_round_finished(state, event, now):
    pass