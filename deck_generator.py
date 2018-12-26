import itertools
from typing import List, Callable

from multiset import FrozenMultiset

_default_deck = ['+0', '+0', '+0', '+0', '+0', '+0',
                 '+1', '+1', '+1', '+1', '+1',
                 '-1', '-1', '-1', '-1', '-1',
                 '-2', '+2', 'x0', 'x2']


def get_default_deck():
    return FrozenMultiset(_default_deck)


def generate_all_decks_for(perks: List[Callable[[List[str]], None]]):
    result = set()
    perk_combinations = []
    for i in range(0, len(perks) + 1):
        perk_combinations += itertools.combinations(perks, i)

    for perk_combo in perk_combinations:
        deck = _default_deck.copy()
        for func in perk_combo:
            func(deck)
        result.add(FrozenMultiset(deck))

    return result
