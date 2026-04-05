import pytest

from three_card_poker.three_card_poker import ThreeCardPoker
from cards import Deck
from three_card_poker_des.state import State
from three_card_poker_des.handlers import handle_round_started
from three_card_poker_des.engine.core import Event


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
            State.RoundState.DEALING,
            State.RoundState.PLAYER_ACTING,
            State.RoundState.DEALER_ACTING,
            State.RoundState.DONE,
            State.RoundState.RESOLVING
        ]
    )
    def test_raises_value_error_if_state_is_not_ready(self, round_state):
        deck = Deck()
        round = ThreeCardPoker(deck=deck)
        state = State(round=round, round_state=round_state)
        
        with pytest.raises(ValueError):
            handle_round_started(state, None, 0)


    def test_leaves_round_state_in_round_state_dealing(self, default_state):
        handle_round_started(default_state, None, 0)
        assert default_state.round_state == State.RoundState.DEALING


    def test_round_started_returns_list_in_with_correct_event(self, default_state):
        events = handle_round_started(default_state, None, 0)

        assert events[0].type == "DEAL_CARDS"

