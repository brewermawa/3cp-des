from cards.deck import Deck
from cards.card import Card

#["♣", "♦", "♠", "♥"]
class FixedDeck(Deck):
    def shuffle(self):
        super()._build_deck()

    def _take_one_by_rank_and_suit(self, rank: str, suit: str) -> Card:
        for c in self._deck:
            if c.rank == rank and c.suit == suit:
                self._deck.remove(c)
                return c
        raise ValueError(f"No card with rank {rank} and suit {suit} found in deck")

    def _program_ranks_top(self, cards_in_draw_order: list[Card]) -> None:
        """
        Arrange the deck so that successive draws (pop from end) return the given
        ranks in this exact order. Supports repeated ranks.
        """
        # Take actual cards (preserves multiplicity correctly)
        taken: list[Card] = [self._take_one_by_rank_and_suit(card.rank, card.suit) for card in cards_in_draw_order]

        # Append in reverse so the last appended is drawn first
        for c in reversed(taken):
            self._deck.append(c)

    #Q-6-4, Q-6-3, K-8-5, 8-6-2, par, straight, flush, tercia, straight flush.
    def deck_for_player_Q63(self): #player does not bet
        self._program_ranks_top([Card("2", "♥"), Card("Q", "♦"), Card("6", "♦"), Card("3", "♠")])

    def deck_for_player_Q64(self): #player bets
        self._program_ranks_top([Card("2", "♥"), Card("Q", "♦"), Card("6", "♦"), Card("4", "♠")])

    def deck_for_player_K85(self): #player bets
        self._program_ranks_top([Card("2", "♥"), Card("K", "♦"), Card("8", "♦"), Card("5", "♠")])

    def deck_for_player_862(self): #player folds
        self._program_ranks_top([Card("2", "♥"), Card("8", "♦"), Card("6", "♦"), Card("2", "♠")])

    def deck_for_player_pair(self): #player bets
        self._program_ranks_top([Card("2", "♥"), Card("2", "♦"), Card("2", "♠"), Card("8", "♦")])

    def deck_for_player_straight(self): #player bets
        self._program_ranks_top([Card("2", "♥"), Card("3", "♦"), Card("4", "♠"), Card("5", "♦")])

    def deck_for_player_flush(self): #player bets
        self._program_ranks_top([Card("2", "♥"), Card("3", "♦"), Card("4", "♦"), Card("6", "♦")])

    def deck_for_player_trips(self): #player bets
        self._program_ranks_top([Card("2", "♥"), Card("3", "♦"), Card("3", "♥"), Card("3", "♠")])

    def deck_for_player_straight_flush(self): #player bets
        self._program_ranks_top([Card("2", "♥"), Card("3", "♦"), Card("4", "♦"), Card("5", "♦")])


    
if __name__ == "__main__":
    deck = FixedDeck()
    deck.deck_for_high_card_A()
    print(deck.draw())
    print(deck.draw())
    print(deck.draw())
        

