import pytest

from three_card_poker.three_card_poker import ThreeCardPoker
from cards import Deck
from three_card_poker_des.state import State
from three_card_poker_des.handlers import handle_deal_cards

class TestRoundStarted:
    @pytest.fixture
    def default_state(self):
        deck = Deck()
        round = ThreeCardPoker(deck=deck)
        state = State(round=round)

        return state

    @pytest.mark.parametrize(
        "round_state",
        [
            State.RoundState.READY,
            State.RoundState.PLAYER_ACTING,
            State.RoundState.DEALER_ACTING,
            State.RoundState.DONE,
            State.RoundState.RESOLVING
        ]
    )
    def test_raises_value_error_if_state_is_not_dealing(self, round_state):
        deck = Deck()
        round = ThreeCardPoker(deck=deck)
        state = State(round=round, round_state=round_state)
        
        with pytest.raises(ValueError):
            handle_deal_cards(state, None, 0)


    def test_leaves_round_in_round_state_player_acting(self, default_state):
        handle_deal_cards(default_state, None, 0)
        assert default_state.round_state == State.RoundState.PLAYER_ACTING


"""
    def test_returns_list_with_correct_event(self, default_state):
        events = handle_deal_cards(default_state, None, 0)

        assert events[0].type == "PLAYER_TURN"

    
    def test_player_and_dealer_hands_have_3_cards_each(self, default_state):
        handle_deal_cards(default_state, None, 0)
        assert len(default_state.round.player_hand.cards()) == 3
        assert len(default_state.round.dealer_hand.cards()) == 3


    def test_cards_remaining_in_deck_is_45

"""