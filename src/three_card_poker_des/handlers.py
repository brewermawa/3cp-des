from three_card_poker_des.state import State
from three_card_poker_des.events import(
    deal_cards, player_turn, resolve_round, dealer_turn, round_finished
)
from three_card_poker.three_card_poker_rank import ThreeCardPokerRank
from three_card_poker.three_card_poker_eval import ThreeCardPokerEval



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
    
    state.dealer_qualified = ThreeCardPokerEval.dealer_qualifies(state.round.dealer_hand)
    eval_result = ThreeCardPokerEval.eval(state.round.dealer_hand)
    state.dealer_hand_rank = eval_result["rank"]
    
    state.round_state = State.RoundState.RESOLVING
    
    return [resolve_round(time=now+1)]


def _compare_hands(state: State) -> State.RoundOutcome:
    rank_values = {
        ThreeCardPokerRank.HIGH_CARD: 1,
        ThreeCardPokerRank.PAIR: 2,
        ThreeCardPokerRank.FLUSH: 3,
        ThreeCardPokerRank.STRAIGHT: 4,
        ThreeCardPokerRank.THREE_OF_A_KIND: 5,
        ThreeCardPokerRank.STRAIGHT_FLUSH: 6
    }

    if rank_values[state.player_hand_rank] > rank_values[state.dealer_hand_rank]:
        return State.RoundOutcome.PLAYER_WINS
    
    if rank_values[state.player_hand_rank] < rank_values[state.dealer_hand_rank]:
        return State.RoundOutcome.DEALER_WINS
    
    if rank_values[state.player_hand_rank] == rank_values[state.dealer_hand_rank]:
        player_sorted_hand = ThreeCardPokerEval.eval(state.round.player_hand)["sorted_hand"]
        dealer_sorted_hand = ThreeCardPokerEval.eval(state.round.dealer_hand)["sorted_hand"]

        if player_sorted_hand > dealer_sorted_hand:
            return State.RoundOutcome.PLAYER_WINS
        
        if player_sorted_hand < dealer_sorted_hand:
            return State.RoundOutcome.DEALER_WINS
        
        return State.RoundOutcome.PUSH


def handle_resolve_round(state, event, now):
    if state.round_state != State.RoundState.RESOLVING:
        raise ValueError("RESOLVE_ROUND is only valid in RESOLVING state")
    
    if not state.player_bet:
        state.outcomes = State.RoundOutcome.DEALER_WINS
        return [round_finished(time=now+1)]

    if not state.dealer_qualified:
        state.outcomes = State.RoundOutcome.PLAYER_WINS
    else:
        state.outcomes = _compare_hands(state)

    state.pair_plus_multiplier = ThreeCardPokerEval.pair_plus(state.round.player_hand)
    state.ante_bonus = ThreeCardPokerEval.ante_bonus(state.round.player_hand)

    
    return [round_finished(time=now+1)]

def handle_round_finished(state, event, now):
    state.round_state = State.RoundState.DONE