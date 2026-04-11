import pytest

from three_card_poker.three_card_poker import ThreeCardPoker
from cards import Hand
from utils.fixed_deck import FixedDeck
from three_card_poker_des.state import State
from three_card_poker_des.events import round_started
from three_card_poker_des.router import handlers
from three_card_poker_des.engine.core import run_simulation


class TestHandleCompleteRound:
    @pytest.fixture
    def default_state(self):
        deck = FixedDeck()
        round = ThreeCardPoker(deck=deck)
        state = State(round=round)
        state.round_state = State.RoundState.READY

        return state
    
    @pytest.fixture
    def stop_condition(self):
        def _stop(state, now, events_processed, metrics):
            return state.round_state == State.RoundState.DONE
        return _stop

    @pytest.mark.parametrize(
        "deck_to_use",
        [
            "deck_for_player_folds_with_dealer_non_qualifying_hand",
            "deck_for_player_folds_with_dealer_qualifying_hand",
        ]
    )
    def test_player_folds(self, default_state, stop_condition, deck_to_use):
        getattr(default_state.round.deck, deck_to_use)()

        simulation_result = run_simulation(
            initial_state=default_state,
            initial_events=[round_started(time=0)],
            handlers=handlers,
            stop_condition=stop_condition,
            observers=None,
            max_events=100
        )

        assert default_state.player_bet is False
        assert default_state.outcomes == State.RoundOutcome.DEALER_WINS
        assert default_state.pair_plus_multiplier == 0
        assert default_state.ante_bonus == 0
        assert default_state.dealer_qualified is False
        assert default_state.dealer_hand_rank is None


    def test_player_bets_dealer_does_not_qualify(self, default_state, stop_condition):
        default_state.round.deck.deck_for_player_bets_with_dealer_non_qualifying_hand()

        simulation_result = run_simulation(
            initial_state=default_state,
            initial_events=[round_started(time=0)],
            handlers=handlers,
            stop_condition=stop_condition,
            observers=None,
            max_events=100
        )

        assert default_state.player_bet is True
        assert default_state.outcomes == State.RoundOutcome.PLAYER_WINS
        assert default_state.pair_plus_multiplier == 0
        assert default_state.ante_bonus == 0
        assert default_state.dealer_qualified is False
        assert default_state.dealer_hand_rank is not None
        assert default_state.player_hand_rank is not None


    def test_player_bets_dealer_qualifies_player_wins(self, default_state, stop_condition):
        default_state.round.deck.deck_for_player_wins()

        simulation_result = run_simulation(
            initial_state=default_state,
            initial_events=[round_started(time=0)],
            handlers=handlers,
            stop_condition=stop_condition,
            observers=None,
            max_events=100
        )

        assert default_state.player_bet is True
        assert default_state.outcomes == State.RoundOutcome.PLAYER_WINS
        assert default_state.pair_plus_multiplier == 0
        assert default_state.ante_bonus == 0
        assert default_state.dealer_qualified is True
        assert default_state.dealer_hand_rank is not None
        assert default_state.player_hand_rank is not None


    def test_player_bets_dealer_qualifies_dealer_wins(self, default_state, stop_condition):
        default_state.round.deck.deck_for_dealer_wins()

        simulation_result = run_simulation(
            initial_state=default_state,
            initial_events=[round_started(time=0)],
            handlers=handlers,
            stop_condition=stop_condition,
            observers=None,
            max_events=100
        )

        assert default_state.player_bet is True
        assert default_state.outcomes == State.RoundOutcome.DEALER_WINS
        assert default_state.dealer_qualified is True
        assert default_state.dealer_hand_rank is not None
        assert default_state.player_hand_rank is not None


    def test_player_bets_dealer_qualifies_push(self, default_state, stop_condition):
        default_state.round.deck.deck_for_push()

        simulation_result = run_simulation(
            initial_state=default_state,
            initial_events=[round_started(time=0)],
            handlers=handlers,
            stop_condition=stop_condition,
            observers=None,
            max_events=100
        )

        assert default_state.player_bet is True
        assert default_state.outcomes == State.RoundOutcome.PUSH
        assert default_state.dealer_qualified is True
        assert default_state.dealer_hand_rank is not None
        assert default_state.player_hand_rank is not None


    @pytest.mark.parametrize(
        "deck_to_use, pair_plus_multiplier",
        [
            ("deck_for_player_pair", 1),
            ("deck_for_player_flush", 3),
            ("deck_for_player_straight", 6),
            ("deck_for_player_trips", 30),
            ("deck_for_player_straight_flush", 40)
        ]
    )
    def test_pair_plus(self, default_state, stop_condition, deck_to_use, pair_plus_multiplier):
        getattr(default_state.round.deck, deck_to_use)()

        simulation_result = run_simulation(
            initial_state=default_state,
            initial_events=[round_started(time=0)],
            handlers=handlers,
            stop_condition=stop_condition,
            observers=None,
            max_events=100
        )
        
        assert default_state.player_bet is True
        assert default_state.pair_plus_multiplier == pair_plus_multiplier


    @pytest.mark.parametrize(
        "deck_to_use, ante_bonus_multiplier",
        [
            ("deck_for_player_pair", 0),
            ("deck_for_player_flush", 0),
            ("deck_for_player_straight", 1),
            ("deck_for_player_trips", 4),
            ("deck_for_player_straight_flush", 6)
        ]
    )
    def test_ante_bonus(self, default_state, stop_condition, deck_to_use, ante_bonus_multiplier):
        getattr(default_state.round.deck, deck_to_use)()

        simulation_result = run_simulation(
            initial_state=default_state,
            initial_events=[round_started(time=0)],
            handlers=handlers,
            stop_condition=stop_condition,
            observers=None,
            max_events=100
        )
        
        assert default_state.player_bet is True
        assert default_state.ante_bonus == ante_bonus_multiplier
