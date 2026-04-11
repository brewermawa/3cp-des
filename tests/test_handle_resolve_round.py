import pytest

from three_card_poker.three_card_poker import ThreeCardPoker
from three_card_poker.three_card_poker_rank import ThreeCardPokerRank
from cards import Deck
from utils.fixed_deck import FixedDeck
from three_card_poker_des.state import State
from three_card_poker_des.handlers import handle_deal_cards, handle_player_turn, handle_dealer_turn, handle_resolve_round

class TestHandleResolveRound:
    @pytest.fixture
    def default_state(self):
        deck = FixedDeck()
        round = ThreeCardPoker(deck=deck)
        state = State(round=round)
        state.round_state = State.RoundState.RESOLVING

        return state
    
    @pytest.mark.parametrize(
        "round_state",
        [
            State.RoundState.READY,
            State.RoundState.DEALING,
            State.RoundState.PLAYER_ACTING,
            State.RoundState.DONE,
            State.RoundState.DEALER_ACTING
        ]
    )
    def test_raises_value_error_if_state_is_not_resolving(self, round_state):
        deck = Deck()
        round = ThreeCardPoker(deck=deck)
        state = State(round=round, round_state=round_state)
        
        with pytest.raises(ValueError):
            handle_resolve_round(state, None, 0)


    def test_leaves_round_in_round_state_done(self, default_state):
        default_state.round_state = State.RoundState.DEALING
        handle_deal_cards(default_state, None, 0)
        default_state.round_state = State.RoundState.RESOLVING
        handle_resolve_round(default_state, None, 0)

        assert default_state.round_state == State.RoundState.RESOLVING


    def test_returns_list_with_correct_event_round_finished(self, default_state):
        default_state.round_state = State.RoundState.DEALING
        handle_deal_cards(default_state, None, 0)
        default_state.round_state = State.RoundState.RESOLVING
        events = handle_resolve_round(default_state, None, 0)

        assert events[0].type == "ROUND_FINISHED"

    
    @pytest.mark.parametrize(
        "deck_to_use",
        [
            "deck_for_player_folds_with_dealer_non_qualifying_hand",
            "deck_for_player_folds_with_dealer_qualifying_hand",
        ]
    )
    def test_player_folds_leaves_player_bet_false(self, default_state, deck_to_use):
        getattr(default_state.round.deck, deck_to_use)()
        default_state.round_state = State.RoundState.DEALING
        handle_deal_cards(default_state, None, 0)
        default_state.round_state = State.RoundState.RESOLVING
        events = handle_resolve_round(default_state, None, 0)

        assert default_state.player_bet is False


    @pytest.mark.parametrize(
        "deck_to_use",
        [
            "deck_for_player_folds_with_dealer_non_qualifying_hand",
            "deck_for_player_folds_with_dealer_qualifying_hand",
        ]
    )
    def test_player_folds_sets_outcome_dealer_wins(self, default_state, deck_to_use):
        getattr(default_state.round.deck, deck_to_use)()
        default_state.round_state = State.RoundState.DEALING
        handle_deal_cards(default_state, None, 0)
        default_state.round_state = State.RoundState.RESOLVING
        events = handle_resolve_round(default_state, None, 0)

        assert default_state.outcomes == State.RoundOutcome.DEALER_WINS
