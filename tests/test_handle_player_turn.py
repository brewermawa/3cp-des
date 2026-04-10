import pytest

from three_card_poker.three_card_poker import ThreeCardPoker
from three_card_poker.three_card_poker_rank import ThreeCardPokerRank
from cards import Deck
from utils.fixed_deck import FixedDeck
from three_card_poker_des.state import State
from three_card_poker_des.handlers import handle_deal_cards, handle_player_turn

class TestHandlePlayerTurn:
    @pytest.fixture
    def default_state(self):
        deck = FixedDeck()
        round = ThreeCardPoker(deck=deck)
        state = State(round=round)
        state.round_state = State.RoundState.PLAYER_ACTING

        return state

    @pytest.mark.parametrize(
        "round_state",
        [
            State.RoundState.READY,
            State.RoundState.DEALING,
            State.RoundState.DEALER_ACTING,
            State.RoundState.DONE,
            State.RoundState.RESOLVING
        ]
    )
    def test_raises_value_error_if_state_is_not_player_acting(self, round_state):
        deck = Deck()
        round = ThreeCardPoker(deck=deck)
        state = State(round=round, round_state=round_state)
        
        with pytest.raises(ValueError):
            handle_player_turn(state, None, 0) 

    @pytest.mark.parametrize(
        "deck_to_use",
        [
            "deck_for_player_Q64",
            "deck_for_player_K85",
            "deck_for_player_pair",
            "deck_for_player_straight",
            "deck_for_player_flush",
            "deck_for_player_trips",
            "deck_for_player_straight_flush",
        ]
    )
    def test_leaves_round_in_round_state_player_acting_if_player_bets(self, default_state, deck_to_use):
        getattr(default_state.round.deck, deck_to_use)()
        default_state.round_state = State.RoundState.DEALING
        handle_deal_cards(default_state, None, 0)
        handle_player_turn(default_state, None, 0)

        assert default_state.round_state == State.RoundState.PLAYER_ACTING


    @pytest.mark.parametrize(
        "deck_to_use",
        [
            "deck_for_player_Q63",
            "deck_for_player_862",
        ]
    )
    def test_leaves_round_in_round_state_player_acting_if_player_folds(self, default_state, deck_to_use):
        getattr(default_state.round.deck, deck_to_use)()
        default_state.round_state = State.RoundState.DEALING
        handle_deal_cards(default_state, None, 0)
        handle_player_turn(default_state, None, 0)
        assert default_state.round_state == State.RoundState.RESOLVING


    @pytest.mark.parametrize(
        "deck_to_use",
        [
            "deck_for_player_Q64",
            "deck_for_player_K85",
            "deck_for_player_pair",
            "deck_for_player_straight",
            "deck_for_player_flush",
            "deck_for_player_trips",
            "deck_for_player_straight_flush",
        ]
    )
    def test_returns_list_with_correct_event_if_player_bets(self, default_state, deck_to_use):
        getattr(default_state.round.deck, deck_to_use)()
        default_state.round_state = State.RoundState.DEALING
        handle_deal_cards(default_state, None, 0)
        events = handle_player_turn(default_state, None, 0)

        assert events[0].type == "PLAYER_BET"


    @pytest.mark.parametrize(
        "deck_to_use",
        [
            "deck_for_player_Q63",
            "deck_for_player_862",
        ]
    )
    def test_returns_list_with_correct_event_if_player_folds(self, default_state, deck_to_use):
        getattr(default_state.round.deck, deck_to_use)()
        default_state.round_state = State.RoundState.DEALING
        handle_deal_cards(default_state, None, 0)
        events = handle_player_turn(default_state, None, 0)

        assert events[0].type == "RESOLVE_ROUND"

    @pytest.mark.parametrize(
        "deck_to_use",
        [
            "deck_for_player_Q64",
            "deck_for_player_Q63",
        ]
    )
    def test_handle_player_turn_sets_state_player_hand_rank(self, default_state, deck_to_use):
        getattr(default_state.round.deck, deck_to_use)()
        default_state.round_state = State.RoundState.DEALING
        handle_deal_cards(default_state, None, 0)
        events = handle_player_turn(default_state, None, 0)

        assert isinstance(default_state.player_hand_rank, ThreeCardPokerRank)


    @pytest.mark.parametrize(
        "deck_to_use",
        [
            "deck_for_player_Q64",
            "deck_for_player_K85",
            "deck_for_player_pair",
            "deck_for_player_straight",
            "deck_for_player_flush",
            "deck_for_player_trips",
            "deck_for_player_straight_flush",
        ]
    )
    def test_returns_set_player_bet_to_true_if_player_bets(self, default_state, deck_to_use):
        getattr(default_state.round.deck, deck_to_use)()
        default_state.round_state = State.RoundState.DEALING
        handle_deal_cards(default_state, None, 0)
        events = handle_player_turn(default_state, None, 0)

        assert default_state.player_bet is True


