import itertools
from collections import Counter

from multiset import FrozenMultiset

from simple_timer_context import SimpleTimerContext


def generate(deck: FrozenMultiset) -> Counter:
    rolling_cards = []
    for card in deck:
        if card.startswith("R"):
            rolling_cards.append(card)

    with SimpleTimerContext("Generating all rolling card arrangements."):
        result = Counter()
        for i in range(0, len(rolling_cards) + 1):
            print(i)
            rolling_permutations_of_i_length = itertools.permutations(rolling_cards, i)
            for p in rolling_permutations_of_i_length:
                result.update({FrozenMultiset(p)})

    return result
