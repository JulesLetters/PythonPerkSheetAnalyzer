import itertools
from typing import Set

from multiset import FrozenMultiset


def generate_from(deck: FrozenMultiset) -> Set[FrozenMultiset]:
    result = set()
    for i in range(0, len(deck) + 1):
        for c in itertools.combinations(deck, i):
            result.add(FrozenMultiset(c))
    return result
