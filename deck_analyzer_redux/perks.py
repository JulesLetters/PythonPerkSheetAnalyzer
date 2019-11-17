from typing import List

import deck_analyzer_redux.cards as cards


Deck = List[cards.Card]


def none(_: Deck) -> None:
    pass


def remove_two_negative_ones(deck: Deck) -> None:
    deck.remove(cards.negative_one)
    deck.remove(cards.negative_one)


def remove_four_zeroes(deck: Deck) -> None:
    deck.remove(cards.plus_zero)
    deck.remove(cards.plus_zero)
    deck.remove(cards.plus_zero)
    deck.remove(cards.plus_zero)


def replace_one_plus_zero_with_one_plus_two(deck: Deck) -> None:
    deck.remove(cards.plus_zero)
    deck.append(cards.plus_two)


def add_two_rolling_plus_ones(deck: Deck) -> None:
    deck.append(cards.rolling_plus_one)
    deck.append(cards.rolling_plus_one)


def add_three_rolling_muddles(deck: Deck) -> None:
    deck.append(cards.rolling_plus_zero_muddle)
    deck.append(cards.rolling_plus_zero_muddle)
    deck.append(cards.rolling_plus_zero_muddle)


def add_two_rolling_pierce_3s(deck: Deck) -> None:
    deck.append(cards.rolling_plus_zero_pierce_3)
    deck.append(cards.rolling_plus_zero_muddle)


def add_one_rolling_stun(deck: Deck) -> None:
    deck.append(cards.rolling_plus_zero_stun)


def add_one_rolling_add_target(deck: Deck) -> None:
    deck.append(cards.rolling_plus_zero_add_target)


def add_one_plus_zero_refresh_item(deck: Deck) -> None:
    deck.append(cards.rolling_plus_one_refresh_item)


def add_two_plus_ones(deck: Deck) -> None:
    deck.append(cards.plus_one)
    deck.append(cards.plus_one)


def replace_one_minus_one_with_one_plus_one(deck: Deck) -> None:
    deck.remove(cards.negative_one)
    deck.append(cards.plus_one)


def add_three_plus_zero_fires(deck: Deck) -> None:
    deck.append(cards.plus_zero_fire)
    deck.append(cards.plus_zero_fire)
    deck.append(cards.plus_zero_fire)


def add_three_plus_zero_ices(deck: Deck) -> None:
    deck.append(cards.plus_zero_ice)
    deck.append(cards.plus_zero_ice)
    deck.append(cards.plus_zero_ice)


def add_three_plus_zero_airs(deck: Deck) -> None:
    deck.append(cards.plus_zero_air)
    deck.append(cards.plus_zero_air)
    deck.append(cards.plus_zero_air)


def add_three_plus_zero_earths(deck: Deck) -> None:
    deck.append(cards.plus_zero_earth)
    deck.append(cards.plus_zero_earth)
    deck.append(cards.plus_zero_earth)


def replace_two_plus_zeros_with_one_plus_zero_fire_and_one_plus_zero_earth(deck: Deck) -> None:
    deck.remove(cards.plus_zero)
    deck.remove(cards.plus_zero)
    deck.append(cards.plus_zero_fire)
    deck.append(cards.plus_zero_earth)


def replace_two_plus_zeros_with_one_plus_zero_ice_and_one_plus_zero_air(deck: Deck) -> None:
    deck.remove(cards.plus_zero)
    deck.remove(cards.plus_zero)
    deck.append(cards.plus_zero_ice)
    deck.append(cards.plus_zero_air)


def add_two_plus_one_push_ones(deck: Deck) -> None:
    deck.append(cards.plus_one_push_one)
    deck.append(cards.plus_one_push_one)


def add_one_plus_one_wound(deck: Deck) -> None:
    deck.append(cards.plus_one_wound)


def add_one_plus_zero_stun(deck: Deck) -> None:
    deck.append(cards.plus_zero_stun)


def add_one_plus_zero_add_target(deck: Deck) -> None:
    deck.append(cards.plus_zero_add_target)
