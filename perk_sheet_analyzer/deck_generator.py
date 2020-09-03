import itertools
from collections import defaultdict
from typing import List, Callable, Dict, Iterable, NamedTuple

from multiset import FrozenMultiset

import perk_sheet_analyzer.cards as cards

_default_deck = [cards.plus_0] * 6 + [cards.plus_1] * 5 + [cards.minus_1] * 5 + \
                [cards.minus_2, cards.plus_2, cards.times_0, cards.times_2]


def get_default_deck() -> FrozenMultiset:
    return FrozenMultiset(_default_deck)


Perk = Callable[[List[str]], None]


class NamedPerk(NamedTuple):
    name: str
    deck_modification: Perk


def all_decks_and_generations_for(perk_functions: List[Perk]) -> Dict[FrozenMultiset, List[List[NamedPerk]]]:
    named_perks = [NamedPerk(p.__name__, p) for p in perk_functions]

    # Get all unique combinations of perks.
    perk_combinations = []
    for i in range(0, len(named_perks) + 1):
        perk_combinations.extend(itertools.combinations(named_perks, i))
    unique_perk_combinations = frozenset(perk_combinations)

    # Generate all decks, and group the ways to make them.
    decks_and_generation_methods = defaultdict(list)
    for perk_combo in unique_perk_combinations:
        decks_and_generation_methods[generate_deck(perk_combo)].append(perk_combo)

    return decks_and_generation_methods


def generate_deck(perks: Iterable[NamedPerk]) -> FrozenMultiset:
    deck = _default_deck.copy()
    for perk in perks:
        perk.deck_modification(deck)
    return FrozenMultiset(deck)
