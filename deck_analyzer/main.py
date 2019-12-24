import itertools
import math
import operator
from collections import Counter, defaultdict, namedtuple
from fractions import Fraction
from functools import reduce
from typing import Iterable

from multiset import FrozenMultiset

from deck_analyzer import perk_sheets, deck_generator
from deck_analyzer.cards import Card
from deck_analyzer.simple_timer_context import SimpleTimerContext


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


def card_to_aggregate_line(card: Card) -> AggregateLine:
    return make_aggregate_line_results([card])


class DeckStatistics:
    def __init__(self, generation_methods) -> None:
        self.countable_effect_odds = defaultdict(Fraction)
        self.singular_effect_odds = defaultdict(Fraction)
        self.generation_methods = generation_methods
        self.total_odds = Fraction()

    def add_aggregate(self, aggregate: AggregateLine, odds: Fraction):
        for effect, count in aggregate.countable_effects.items():
            self.countable_effect_odds[(effect, count)] += odds
            self.singular_effect_odds[effect] += odds  # Chance a countable occurred.
        for effect in aggregate.singular_effects:
            self.singular_effect_odds[effect] += odds
        self.total_odds += odds


def analyze_deck(atk, deck, generation_methods):
    normal_statistics = DeckStatistics(generation_methods)
    advantage_statistics = DeckStatistics(generation_methods)

    # Of all possible unique decks, there's still a lot of non-unique rolling and terminator collections.
    # That means an optimization is possible here, caching the result of this loop for given collections.
    # (This isn't done, but should be done at some point)
    deck_length = len(deck)
    rolling_cards = [card for card in deck if card.rolling]
    terminator_cards = [card for card in deck if not card.rolling]

    counted_terminator_cards = Counter(terminator_cards)

    two_card_denominator = Fraction(1, deck_length * (deck_length - 1))

    for terminator_card, count in counted_terminator_cards.items():
        # terminated_line = line.union([terminator_card])
        odds = Fraction(count, deck_length)
        terminated_aggregate = card_to_aggregate_line(terminator_card)

        normal_statistics.add_aggregate(terminated_aggregate, odds)

    advantage_terminators = itertools.combinations(terminator_cards, 2)
    for terminator_pair in advantage_terminators:
        cmp = terminator_pair[0].adv_compare(terminator_pair[1], atk)
        if cmp == -1:
            al = card_to_aggregate_line(terminator_pair[1])
            advantage_statistics.add_aggregate(al, 2 * two_card_denominator)
        elif cmp == 1:
            al = card_to_aggregate_line(terminator_pair[0])
            advantage_statistics.add_aggregate(al, 2 * two_card_denominator)
        else:
            a = card_to_aggregate_line(terminator_pair[0])
            advantage_statistics.add_aggregate(a, two_card_denominator)
            b = card_to_aggregate_line(terminator_pair[1])
            advantage_statistics.add_aggregate(b, two_card_denominator)

    short_rolling_combinations = Counter()
    short_rolling_combinations.update([FrozenMultiset(c) for c in itertools.combinations(rolling_cards, 1)])

    lengthy_rolling_combinations = Counter()
    for i in range(2, len(rolling_cards) + 1):
        lengthy_rolling_combinations.update([FrozenMultiset(c) for c in itertools.combinations(rolling_cards, i)])

    # validate_permutation_count(rolling_cards, unique_rolling_combinations)  # Debug assertion

    for line, line_occurrence_count in short_rolling_combinations.items():
        # line_occurrence_count is the unordered probability numerator.
        # rolling_permutations, below, is the numerator for the probability where order matters.
        rolling_permutations = line_occurrence_count * math.factorial(len(line))
        aggregate_line_results = make_aggregate_line_results(line)

        sequence_length = len(line) + 1
        denominator = reduce(operator.mul, range(deck_length, deck_length - sequence_length, -1), 1)
        for terminator_card, count in counted_terminator_cards.items():
            # terminated_line = line.union([terminator_card])
            odds = Fraction(rolling_permutations * count, denominator)
            terminated_aggregate = add_card_to_aggregate_line_results(terminator_card, aggregate_line_results)

            advantage_statistics.add_aggregate(terminated_aggregate, odds * 2)  # * 2 because either order counts.
            normal_statistics.add_aggregate(terminated_aggregate, odds)

    for line, line_occurrence_count in lengthy_rolling_combinations.items():
        rolling_permutations = line_occurrence_count * math.factorial(len(line))
        aggregate_line_results = make_aggregate_line_results(line)
        sequence_length = len(line) + 1
        denominator = reduce(operator.mul, range(deck_length, deck_length - sequence_length, -1), 1)
        for terminator_card, count in counted_terminator_cards.items():
            # terminated_line = line.union([terminator_card])
            odds = Fraction(rolling_permutations * count, denominator)
            terminated_aggregate = add_card_to_aggregate_line_results(terminator_card, aggregate_line_results)

            normal_statistics.add_aggregate(terminated_aggregate, odds)
            advantage_statistics.add_aggregate(terminated_aggregate, odds)

    return advantage_statistics, normal_statistics


def main():
    decks_and_generation_methods = deck_generator.all_decks_and_generations_for(perk_sheets.three_spears)
    deck_count = len(decks_and_generation_methods)
    print("Decks to analyze: {}".format(deck_count))

    atk = 3
    all_deck_statistics = {}
    n = 0
    for deck, generation_methods in decks_and_generation_methods.items():
        n += 1
        if n % 100 == 0:
            print(".", end="", flush=True)
        advantage_statistics, normal_statistics = analyze_deck(atk, deck, generation_methods)

        all_deck_statistics[deck] = (normal_statistics, advantage_statistics)
        # assert normal_statistics.total_odds == 1  # Debug assertion
        # assert advantage_statistics.total_odds == 1  # Debug assertion
    print("")

    decks_by_odds = defaultdict(list)
    for deck, statistics in all_deck_statistics.items():
        advantage_statistics = statistics[1]
        odds = advantage_statistics.countable_effect_odds[("Refresh_Item", 1)]
        decks_by_odds[odds].append(advantage_statistics.generation_methods)

    level_9_decks = defaultdict(list)
    for odds, generation_methods in decks_by_odds.items():
        for method in generation_methods:
            if len(method[0]) >= 8:
                level_9_decks[odds].append(method)

    top_four_odds = sorted(level_9_decks.keys())[-4:]
    print(top_four_odds)
    for odds in top_four_odds:
        print(odds)
        for gen in level_9_decks[odds]:
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
    with SimpleTimerContext("Calculating all character decks."):
        main()
