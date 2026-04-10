from three_card_poker_des.engine.core import Event

def round_started(*, time: int) -> Event:
    return Event(
        time=time,
        type="ROUND_STARTED",
        data={}
    )

def deal_cards(*, time: int) -> Event:
    return Event(
        time=time,
        type="DEAL_CARDS",
        data={}
    )


def player_turn(*, time: int) -> Event:
    return Event(
        time=time,
        type="PLAYER_TURN",
        data={}
    )


def dealer_turn(*, time: int) -> Event:
    return Event(
        time=time,
        type="DEALER_TURN",
        data={}
    )


def resolve_round(*, time: int) -> Event:
    return Event(
        time=time,
        type="RESOLVE_ROUND",
        data={}
    )


def round_finished(*, time: int) -> Event:
    return Event(
        time=time,
        type="ROUND_FINISHED",
        data={}
    )



