from typing import List

import deck_analyzer.cards as cards

Deck = List[cards.Card]


def none(_: Deck) -> None:
    pass


def remo_two_minus_1(deck: Deck) -> None:
    deck.remove(cards.minus_1)
    deck.remove(cards.minus_1)


def remo_four_plus_0(deck: Deck) -> None:
    deck.remove(cards.plus_0)
    deck.remove(cards.plus_0)
    deck.remove(cards.plus_0)
    deck.remove(cards.plus_0)


def repl_one_plus_0_w_one_plus_2(deck: Deck) -> None:
    deck.remove(cards.plus_0)
    deck.append(cards.plus_2)


def repl_one_minus_1_w_one_plus_1(deck: Deck) -> None:
    deck.remove(cards.minus_1)
    deck.append(cards.plus_1)


def add_two_rolling_plus_1(deck: Deck) -> None:
    deck.append(cards.rolling_plus_1)
    deck.append(cards.rolling_plus_1)


def add_three_rolling_muddle(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_muddle)
    deck.append(cards.rolling_plus_0_muddle)
    deck.append(cards.rolling_plus_0_muddle)


def add_three_rolling_push_1(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_push_1)
    deck.append(cards.rolling_plus_0_push_1)
    deck.append(cards.rolling_plus_0_push_1)


def add_two_rolling_pierce_3(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_pierce_3)
    deck.append(cards.rolling_plus_0_pierce_3)


def add_one_rolling_muddle(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_muddle)


def add_one_rolling_stun(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_stun)


def add_one_rolling_disarm(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_disarm)


def add_one_rolling_add_target(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_add_target)


def add_one_plus_0_refresh_item(deck: Deck) -> None:
    deck.append(cards.plus_0_refresh_item)


def add_two_plus_1(deck: Deck) -> None:
    deck.append(cards.plus_1)
    deck.append(cards.plus_1)


def add_one_plus_3(deck: Deck) -> None:
    deck.append(cards.plus_3)


def add_three_plus_0_fire(deck: Deck) -> None:
    deck.append(cards.plus_0_fire)
    deck.append(cards.plus_0_fire)
    deck.append(cards.plus_0_fire)


def add_three_plus_0_ice(deck: Deck) -> None:
    deck.append(cards.plus_0_ice)
    deck.append(cards.plus_0_ice)
    deck.append(cards.plus_0_ice)


def add_three_plus_0_air(deck: Deck) -> None:
    deck.append(cards.plus_0_air)
    deck.append(cards.plus_0_air)
    deck.append(cards.plus_0_air)


def add_three_plus_0_earth(deck: Deck) -> None:
    deck.append(cards.plus_0_earth)
    deck.append(cards.plus_0_earth)
    deck.append(cards.plus_0_earth)


def repl_two_plus_0_w_one_plus_0_fire_and_one_plus_0_earth(deck: Deck) -> None:
    deck.remove(cards.plus_0)
    deck.remove(cards.plus_0)
    deck.append(cards.plus_0_fire)
    deck.append(cards.plus_0_earth)


def repl_two_plus_0_w_one_plus_0_ice_and_one_plus_0_air(deck: Deck) -> None:
    deck.remove(cards.plus_0)
    deck.remove(cards.plus_0)
    deck.append(cards.plus_0_ice)
    deck.append(cards.plus_0_air)


def add_two_plus_1_push_1(deck: Deck) -> None:
    deck.append(cards.plus_1_push_1)
    deck.append(cards.plus_1_push_1)


def add_one_plus_1_wound(deck: Deck) -> None:
    deck.append(cards.plus_1_wound)


def add_one_plus_0_stun(deck: Deck) -> None:
    deck.append(cards.plus_0_stun)


def add_one_plus_0_add_target(deck: Deck) -> None:
    deck.append(cards.plus_0_add_target)


def add_one_plus_1_shield_1_self(deck: Deck) -> None:
    deck.append(cards.plus_1_shield_1_self)
