import operator
from collections import Counter
from functools import reduce

from multiset import FrozenMultiset

import rolling_draw_types
from simple_timer_context import SimpleTimerContext


def generate(deck: FrozenMultiset) -> Counter:
    rolling_cards = []
    for card in deck:
        if card.startswith("R"):
            rolling_cards.append(card)

    # Ideally, something like this would actually return
    # the relative probabilities.
    # That is, the sum of all outputs from this function would be 1.
    # This would allow much easier multiplication.
    # Right now, the problem exists where {+0 ICE} actually is a subset of {+0 ICE, +0 ICE}.
    # ...
    # Though actually, the odds are fairly easy to calculate.
    # Assuming all Draws are starting from the first-drawn card,
    # the only thing necessary to do is multiply every draw by
    # the chance of NOT drawing another rolling modifier.

    with SimpleTimerContext("Generating all rolling card arrangements."):
        result = Counter()
        rolling_cards_multiset = FrozenMultiset(rolling_cards)
        draw_types = rolling_draw_types.generate_from(rolling_cards_multiset)

        for draw_type in draw_types:
            arrangements = factorial(len(draw_type))
            card_types = draw_type.distinct_elements()
            for card_type in card_types:
                arrangements *= ncr(rolling_cards_multiset[card_type], draw_type[card_type])

            result.update({draw_type: arrangements})

    return result


def ncr(n: int, r: int) -> int:
    r = min(r, n - r)
    numerator = reduce(operator.mul, range(n, n - r, -1), 1)
    denominator = reduce(operator.mul, range(1, r + 1), 1)
    return numerator // denominator


def factorial(n: int) -> int:
    return reduce(operator.mul, range(n, 0, -1), 1)
