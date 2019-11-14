from typing import List


def none(_: List[str]) -> None:
    pass


def remove_two_negative_ones(deck: List[str]) -> None:
    deck.remove('-1')
    deck.remove('-1')


def remove_four_zeroes(deck: List[str]) -> None:
    deck.remove('+0')
    deck.remove('+0')
    deck.remove('+0')
    deck.remove('+0')


def replace_one_plus_zero_with_one_plus_two(deck: List[str]) -> None:
    deck.remove('+0')
    deck.append('+2')


def add_two_rolling_plus_ones(deck: List[str]) -> None:
    deck.append('R+1')
    deck.append('R+1')


def add_three_rolling_muddles(deck: List[str]) -> None:
    deck.append('R+0 MUDDLE')
    deck.append('R+0 MUDDLE')
    deck.append('R+0 MUDDLE')


def add_two_rolling_pierce_3s(deck: List[str]) -> None:
    deck.append('R+0 PIERCE_3')
    deck.append('R+0 PIERCE_3')


def add_one_rolling_stun(deck: List[str]) -> None:
    deck.append('R+0 STUN')


def add_one_rolling_add_target(deck: List[str]) -> None:
    deck.append('R+0 ADD_TARGET')


def add_one_plus_zero_refresh_item(deck: List[str]) -> None:
    deck.append('+0 REFRESH_ITEM')


def add_two_plus_ones(deck: List[str]) -> None:
    deck.append('+1')
    deck.append('+1')


def replace_one_minus_one_with_one_plus_one(deck: List[str]) -> None:
    deck.remove('-1')
    deck.append('+1')


def add_three_plus_zero_fires(deck: List[str]) -> None:
    deck.append('+0 FIRE')
    deck.append('+0 FIRE')
    deck.append('+0 FIRE')


def add_three_plus_zero_ices(deck: List[str]) -> None:
    deck.append('+0 ICE')
    deck.append('+0 ICE')
    deck.append('+0 ICE')


def add_three_plus_zero_airs(deck: List[str]) -> None:
    deck.append('+0 AIR')
    deck.append('+0 AIR')
    deck.append('+0 AIR')


def add_three_plus_zero_earths(deck: List[str]) -> None:
    deck.append('+0 EARTH')
    deck.append('+0 EARTH')
    deck.append('+0 EARTH')


def replace_two_plus_zeros_with_one_plus_zero_fire_and_one_plus_zero_earth(deck: List[str]) -> None:
    deck.remove('+0')
    deck.remove('+0')
    deck.append('+0 FIRE')
    deck.append('+0 EARTH')


def replace_two_plus_zeros_with_one_plus_zero_ice_and_one_plus_zero_air(deck: List[str]) -> None:
    deck.remove('+0')
    deck.remove('+0')
    deck.append('+0 ICE')
    deck.append('+0 AIR')


def add_two_plus_one_push_ones(deck: List[str]) -> None:
    deck.append('+1 PUSH_1')
    deck.append('+1 PUSH_1')


def add_one_plus_one_wound(deck: List[str]) -> None:
    deck.append('+1 WOUND')


def add_one_plus_zero_stun(deck: List[str]) -> None:
    deck.append('+0 STUN')


def add_one_plus_zero_add_target(deck: List[str]) -> None:
    deck.append('+0 ADD_TARGET')
