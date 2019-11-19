import itertools
import math
import operator
from collections import Counter, defaultdict, namedtuple
from fractions import Fraction
from functools import reduce
from typing import Iterable

from multiset import FrozenMultiset

from deck_analyzer_redux import perk_sheets, deck_generator
from deck_analyzer_redux.cards import Card


def unique_ordered_combinations(string_counts, length):
    return set(["".join(sorted(c)) for c in itertools.combinations(string_counts, length)])


AggregateLine = namedtuple("AggregateLine", "atk_calculation countable_effects singular_effects")


def make_aggregate_line_results(line: Iterable[Card]) -> AggregateLine:
    atk_calculation = []
    countable_effects = Counter()
    singular_effects = {}
    for card in line:
        # Another optimization is to intelligently combine the functions.
        atk_calculation.append(card.bonus)
        if card.countable_effect:
            countable_effects[card.countable_effect] += 1
        if card.singular_effect:
            singular_effects[card.singular_effect] = True

    return AggregateLine(atk_calculation, countable_effects, singular_effects)


def add_card_to_aggregate_line_results(card: Card, aggregate: AggregateLine) -> AggregateLine:
    atk_calculation = aggregate.atk_calculation + [card.bonus]

    if card.countable_effect:
        countable_effects = aggregate.countable_effects.copy()
        countable_effects[card.countable_effect] += 1
    else:
        countable_effects = aggregate.countable_effects

    if card.singular_effect:
        singular_effects = aggregate.singular_effects.copy()
        singular_effects[card.singular_effect] = True
    else:
        singular_effects = aggregate.singular_effects

    return AggregateLine(atk_calculation, countable_effects, singular_effects)


class DeckStatistics:
    def __init__(self, generation_methods) -> None:
        self.countable_effect_odds = defaultdict(Fraction)
        self.singular_effect_odds = defaultdict(Fraction)
        self.generation_methods = generation_methods

    def add_aggregate(self, aggregate: AggregateLine, odds: Fraction):
        for effect, count in aggregate.countable_effects.items():
            self.countable_effect_odds[(effect, count)] += odds
            self.singular_effect_odds[effect] += odds  # Chance a countable occurred.
        for effect in aggregate.singular_effects:
            self.singular_effect_odds[effect] += odds


def main():
    decks_and_generation_methods = deck_generator.all_decks_and_generations_for(perk_sheets.three_spears)
    deck_count = len(decks_and_generation_methods)
    print("Decks to analyze: {}".format(deck_count))

    deck_statistics = {}
    for deck, generation_methods in decks_and_generation_methods.items():

        # Of all possible unique decks, there's still a lot of non-unique rolling and terminator collections.
        # That means an optimization is possible here, caching the result of this loop for given collections.
        # (This isn't done, but should be done at some point)
        rolling_cards = [card for card in deck if card.rolling]
        terminator_cards = [card for card in deck if not card.rolling]

        unique_rolling_combinations = Counter()
        # Change 0 to 1 to handle things for Advantage, when we need two terminal-only cards.
        for i in range(0, len(rolling_cards) + 1):
            unique_rolling_combinations.update([FrozenMultiset(c) for c in itertools.combinations(rolling_cards, i)])

        # validate_permutation_count(rolling_cards, unique_rolling_combinations)

        counted_terminator_cards = Counter(terminator_cards)
        deck_length = len(deck)
        for line, line_occurrence_count in unique_rolling_combinations.items():
            # line_occurrence_count is the unordered probability numerator.
            # rolling_permutations, below, is the numerator for the probability where order matters.
            rolling_permutations = line_occurrence_count * math.factorial(len(line))
            aggregate_line_results = make_aggregate_line_results(line)

            sequence_length = len(line) + 1
            denominator = reduce(operator.mul, range(deck_length, deck_length - sequence_length, -1), 1)
            for terminator_card, count in counted_terminator_cards.items():
                # terminated_line = line.union([terminator_card])
                odds = Fraction(rolling_permutations * count, denominator)  # non-advantage.
                terminated_aggregate = add_card_to_aggregate_line_results(terminator_card, aggregate_line_results)

                normal_statistics.add_aggregate(terminated_aggregate, odds)

                # For advantage, we actually have to pick between two outcomes (terminals)
        deck_statistics[deck] = normal_statistics

        # Then, depending on advantage:
        # 0 rolling: 2 terminators. Rolling isn't used. Analyze and pick better.
        # 1 rolling: 1 terminator is used. Aggregate rolls and terminators. Cartesian join.
        # 2 rolling: 1 terminator is used. Aggregate rolls and terminators. Cartesian join.
    print("")
    decks_by_odds = defaultdict(list)
    for deck, statistics in deck_statistics.items():
        odds = statistics.countable_effect_odds[("Refresh_Item", 1)]
        decks_by_odds[odds].append(statistics.generation_methods)
    best_odds = max(decks_by_odds.keys())
    print(best_odds)
    for gen in decks_by_odds[best_odds]:
        print(gen)

    print('Done!')


def validate_permutation_count(rolling_cards, rolling_combination_counts):
    # For debugging. Tests that the expected and actual number of arrangements for rolling cards are the same.
    s = defaultdict(int)
    for line, combination_occurrences in rolling_combination_counts.items():
        permutations = combination_occurrences * math.factorial(len(line))
        s[len(line)] += permutations
    for line_length, actual_permutations in s.items():
        rc_count = len(rolling_cards)
        expected_permutations = math.factorial(rc_count) // math.factorial(rc_count - line_length)
        print(line_length, actual_permutations, expected_permutations)
        assert actual_permutations == expected_permutations


if __name__ == '__main__':
    main()
