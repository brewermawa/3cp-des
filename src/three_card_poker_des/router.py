from .handlers import(
    handle_round_started, 
    handle_deal_cards,
    handle_player_turn,
    handle_dealer_turn,
    handle_resolve_round,
    handle_round_finished,
)

handlers = {
    "ROUND_STARTED": handle_round_started,
    "DEAL_CARDS": handle_deal_cards,
    "PLAYER_TURN": handle_player_turn,
    "DEALER_TURN": handle_dealer_turn,
    "RESOLVE_ROUND": handle_resolve_round,
    "ROUND_FINISHED": handle_round_finished
}