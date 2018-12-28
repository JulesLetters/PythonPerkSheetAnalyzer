from collections import defaultdict
from fractions import Fraction

from multiset import FrozenMultiset


class DeckStatistics:
    def __init__(self) -> None:
        self.effect_rates = defaultdict(Fraction)


def calculate_statistics(deck: FrozenMultiset) -> DeckStatistics:
    result = DeckStatistics()

    non_rolling_count = 0
    for card in deck:
        if not card.startswith('R'):
            non_rolling_count += 1

    for card in deck:
        if has_effect(card):
            result.effect_rates[extract_effect(card)] += Fraction(1, non_rolling_count)

    return result


def has_effect(card: str) -> bool:
    return len(card.split()) is 2


def extract_effect(card: str) -> str:
    return card.split()[1]
