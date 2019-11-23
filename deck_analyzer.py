import operator
from collections import defaultdict
from fractions import Fraction
from functools import reduce

from multiset import FrozenMultiset

import rolling_draw_statistics


class DeckStatistics:
    def __init__(self) -> None:
        self.effect_rates = defaultdict(Fraction)


def calculate_statistics(deck: FrozenMultiset) -> DeckStatistics:
    result = DeckStatistics()

    terminator_freq = defaultdict(Fraction)
    all_effects = set()
    # terminator_count = 0
    rolling_count = 0
    for card in deck:
        if is_rolling(card):
            rolling_count += 1
        if has_effect(card):
            effect = extract_effect(card)
            all_effects.add(effect)
            if not is_rolling(card):
                terminator_freq[effect] += 1

    # Base effect frequency based on terminators.
    # Using the 'empty' draw sequence could eliminate this section.
    rolling_stats = rolling_draw_statistics.generate(deck)
    del rolling_stats[FrozenMultiset({})]
    deck_len = len(deck)
    for effect in terminator_freq:
        result.effect_rates[effect] = Fraction(terminator_freq[effect], deck_len)

    for effect in all_effects:
        # If the effect is present inside the rolling modifier or the terminator, count it.
        # Don't count it twice.
        for draw in rolling_stats:
            print("Draw: {}".format(draw))
            cards_remaining_after_rolling_draw = deck_len - len(draw)
            rolling_draw_freq = rolling_stats[draw]
            rolling_draw_prob = reduce(operator.mul, range(deck_len, cards_remaining_after_rolling_draw, -1), 1)
            true_rolling_draw_prob = Fraction(rolling_draw_freq, rolling_draw_prob)
            if any([has_effect(card) and extract_effect(card) == 'ICE' for card in draw]):
                print(effect)
                non_rolling_non_duplicate_effect_card_count = deck_len - rolling_count - terminator_freq[effect]
                non_duplicate_terminator_prob = Fraction(1, cards_remaining_after_rolling_draw)
                non_duplicate_terminator_prob *= Fraction(non_rolling_non_duplicate_effect_card_count, 1)

                result.effect_rates[effect] += true_rolling_draw_prob * non_duplicate_terminator_prob
                print("First Branch: {} * {}".format(true_rolling_draw_prob, non_duplicate_terminator_prob))

                # Then add the termination & rolling union event:
                print("term_freq/remainder: {}/{}".format(terminator_freq[effect], cards_remaining_after_rolling_draw))
                rate = true_rolling_draw_prob * Fraction(terminator_freq[effect], cards_remaining_after_rolling_draw)
                result.effect_rates[effect] += rate
            else:
                # Our effect isn't in the rolling, but we could still terminate into the effect.
                terminator_prob = Fraction(terminator_freq[effect], cards_remaining_after_rolling_draw)
                result.effect_rates[effect] += true_rolling_draw_prob * terminator_prob
                print("Second Branch: {} * {}".format(true_rolling_draw_prob, terminator_prob))
                pass
            print()

    # print(rolling_stats)
    # for draw in rolling_stats:
    #     cards_remaining_after_rolling_draw = deck_len - len(draw)
    #     rolling_draw_prob = reduce(operator.mul, range(deck_len, cards_remaining_after_rolling_draw, -1), 1)
    #     rolling_draw_freq = rolling_stats[draw]
    #     true_rolling_draw_prob = Fraction(rolling_draw_freq, rolling_draw_prob)
    #     for effect, rate in result.effect_rates.items():
    #         remaining_terminator_prob = Fraction(terminator_freq[effect], cards_remaining_after_rolling_draw)
    #
    #         result.effect_rates[effect] += remaining_terminator_prob * true_rolling_draw_prob
    #
    #     for effect in ['ICE']:
    #         if any([has_effect(card) and extract_effect(card) == 'ICE' for card in draw]):
    #             result.effect_rates[effect] += true_rolling_draw_prob
    #             result.effect_rates[effect] -= true_rolling_draw_prob * Fraction(terminator_freq[effect], cards_remaining_after_rolling_draw)
    return result

# https://oeis.org/A000522

def has_effect(card: str) -> bool:
    return len(card.split()) is 2


def extract_effect(card: str) -> str:
    return card.split()[1]


def is_rolling(card: str) -> bool:
    return card.startswith('R')
