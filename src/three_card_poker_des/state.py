from enum import Enum
from dataclasses import dataclass
from typing import List, Optional

from three_card_poker.three_card_poker import ThreeCardPoker
from three_card_poker.three_card_poker_rank import ThreeCardPokerRank


@dataclass
class State:
    class RoundOutcome(Enum):
        PLAYER_WINS = 1
        DEALER_WINS = 2
        PUSH = 3

    class RoundState(Enum):
        READY = 1
        DEALING = 2
        PLAYER_ACTING = 3
        DEALER_ACTING = 4
        RESOLVING = 5
        DONE = 6

    round: ThreeCardPoker
    round_state: RoundState = RoundState.READY
    outcomes: Optional[RoundOutcome] = None
    player_bet: bool = False
    pair_plus_multiplier: int = 0
    ante_bonus: int = 0
    player_hand_rank: Optional[ThreeCardPokerRank] = None
    dealer_hand_rank: Optional[ThreeCardPokerRank] = None
    dealer_qualified: bool = False
    