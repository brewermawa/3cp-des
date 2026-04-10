import pytest

from three_card_poker.three_card_poker import ThreeCardPoker
from three_card_poker.three_card_poker_rank import ThreeCardPokerRank
from cards import Deck
from utils.fixed_deck import FixedDeck
from three_card_poker_des.state import State
from three_card_poker_des.handlers import handle_deal_cards, handle_player_turn, handle_dealer_turn

class TestHandleDealerTurn:
    @pytest.fixture
    def default_state(self):
        deck = FixedDeck()
        round = ThreeCardPoker(deck=deck)
        state = State(round=round)
        state.round_state = State.RoundState.DEALER_ACTING

        return state

    @pytest.mark.parametrize(
        "round_state",
        [
            State.RoundState.READY,
            State.RoundState.DEALING,
            State.RoundState.PLAYER_ACTING,
            State.RoundState.DONE,
            State.RoundState.RESOLVING
        ]
    )
    def test_raises_value_error_if_state_is_not_dealer_acting(self, round_state):
        deck = Deck()
        round = ThreeCardPoker(deck=deck)
        state = State(round=round, round_state=round_state)
        
        with pytest.raises(ValueError):
            handle_dealer_turn(state, None, 0) 


    def test_leaves_round_in_round_state_resolving(self, default_state):
        default_state.round_state = State.RoundState.DEALING
        handle_deal_cards(default_state, None, 0)
        default_state.round_state = State.RoundState.DEALER_ACTING
        handle_dealer_turn(default_state, None, 0)

        assert default_state.round_state == State.RoundState.RESOLVING


    def test_returns_list_with_correct_event_resolve_round(self, default_state):
        default_state.round_state = State.RoundState.DEALING
        handle_deal_cards(default_state, None, 0)
        default_state.round_state = State.RoundState.DEALER_ACTING
        events = handle_dealer_turn(default_state, None, 0)

        assert events[0].type == "RESOLVE_ROUND"


    @pytest.mark.parametrize(
        "deck_to_use",
        [
            "deck_for_dealer_Q23",
            "deck_for_dealer_226",
        ]
    )
    def test_returns_sets_state_dealer_qualfied_to_true_if_dealer_qualifies(self, default_state, deck_to_use):
        getattr(default_state.round.deck, deck_to_use)()
        default_state.round_state = State.RoundState.DEALING
        handle_deal_cards(default_state, None, 0)
        default_state.round_state = State.RoundState.DEALER_ACTING
        events = handle_dealer_turn(default_state, None, 0)

        assert default_state.dealer_qualified is True


    @pytest.mark.parametrize(
        "deck_to_use",
        [
            "deck_for_dealer_246",
            "deck_for_dealer_JT8",
        ]
    )
    def test_returns_leaves_state_dealer_qualified_false_if_dealer_does_not_qualify(self, default_state, deck_to_use):
        getattr(default_state.round.deck, deck_to_use)()
        default_state.round_state = State.RoundState.DEALING
        handle_deal_cards(default_state, None, 0)
        default_state.round_state = State.RoundState.DEALER_ACTING
        events = handle_dealer_turn(default_state, None, 0)

        assert default_state.dealer_qualified is False


    @pytest.mark.parametrize(
        "deck_to_use",
        [
            "deck_for_player_Q64",
            "deck_for_player_Q63",
        ]
    )
    def test_handle_dealer_turn_sets_state_dealer_hand_rank(self, default_state, deck_to_use):
        getattr(default_state.round.deck, deck_to_use)()
        default_state.round_state = State.RoundState.DEALING
        handle_deal_cards(default_state, None, 0)
        default_state.round_state = State.RoundState.DEALER_ACTING
        events = handle_dealer_turn(default_state, None, 0)

        assert isinstance(default_state.dealer_hand_rank, ThreeCardPokerRank)
