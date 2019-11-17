import itertools
from collections import defaultdict
from typing import List, Callable, Dict, Iterable

from multiset import FrozenMultiset

import deck_analyzer_redux.cards as cards

_default_deck = [cards.plus_zero] * 6 + [cards.plus_one] * 5 + [cards.negative_one] * 5 + \
                [cards.negative_two, cards.plus_two, cards.null_card, cards.times_two]


def get_default_deck() -> FrozenMultiset:
    return FrozenMultiset(_default_deck)


Perk = Callable[[List[str]], None]


def all_decks_and_generations_for(perks: List[Perk]) -> Dict[FrozenMultiset, List[List[Perk]]]:
    # Get all unique combinations of perks.
    perk_combinations = []
    for i in range(0, len(perks) + 1):
        perk_combinations.extend(itertools.combinations(perks, i))
    unique_perk_combinations = frozenset(perk_combinations)

    # Generate all decks, and group the ways to make them.
    decks_and_generation_methods = defaultdict(list)
    for perk_combo in unique_perk_combinations:
        decks_and_generation_methods[generate_deck(perk_combo)].append(perk_combo)

    return decks_and_generation_methods


def generate_deck(perks: Iterable[Perk]) -> FrozenMultiset:
    deck = _default_deck.copy()
    for func in perks:
        func(deck)
    return FrozenMultiset(deck)
