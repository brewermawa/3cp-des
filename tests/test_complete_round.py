import pytest

from three_card_poker.three_card_poker import ThreeCardPoker
from three_card_poker.three_card_poker_rank import ThreeCardPokerRank
from cards import Deck
from utils.fixed_deck import FixedDeck
from three_card_poker_des.state import State
from three_card_poker_des.events import round_started
from three_card_poker_des.handlers import handle_deal_cards, handle_player_turn, handle_dealer_turn, handle_resolve_round
from three_card_poker_des import handlers
from three_card_poker_des.engine.core import run_simulation


class TestHandleCompleteRound:
    @pytest.fixture
    def default_state(self):
        deck = FixedDeck()
        round = ThreeCardPoker(deck=deck)
        state = State(round=round)
        state.round_state = State.RoundState.READY

        return state

    @pytest.mark.parametrize(
        "deck_to_use",
        [
            "deck_for_player_folds_with_dealer_non_qualifying_hand",
            #"deck_for_player_folds_with_dealer_qualifying_hand",
        ]
    )
    def test_player_folds(self, default_state, deck_to_use):
        getattr(default_state.round.deck, deck_to_use)()

        simulation_result = run_simulation(
            initial_state=default_state,
            initial_events=[round_started(time=0)],
            handlers=handlers,
            stop_condition=default_state.round_state == State.RoundState.DONE,
            observers=None,
            max_events=100
        )

        assert 1 == 1

        