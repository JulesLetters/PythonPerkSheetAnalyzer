import itertools
import math
import operator
from collections import namedtuple, Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
from functools import reduce
from typing import Dict, List

from multiset import FrozenMultiset

from perk_sheet_analyzer.aggregated_line import AggregatedLine
from perk_sheet_analyzer.draw_scheme_statistics import DrawSchemeStatistics

EITHER_ORDER = 2
AggregatedLineWithOdds = namedtuple("AggregatedLineWithOdds", "aggregated_line odds")


@dataclass
class DeckStatistics:
    normal: DrawSchemeStatistics
    advantage: DrawSchemeStatistics


def derive_statistics(deck: FrozenMultiset, atk_range: range) -> Dict[int, DeckStatistics]:
    statistics = DeckStatistics(DrawSchemeStatistics(), DrawSchemeStatistics())

    # Possible optimization: Pre-calculate denominators involving deck_length and sequence_length.

    # Of all possible unique decks, there's still a lot of non-unique rolling and terminator collections.
    # That means an optimization is possible here, caching the result of this loop for given collections.
    # (This isn't done, but should be done at some point)
    deck_length = len(deck)
    rolling_cards = [card for card in deck if card.rolling]
    terminator_cards = [card for card in deck if not card.rolling]

    counted_terminator_cards = Counter(terminator_cards)

    for terminator_card, count in counted_terminator_cards.items():
        odds = Fraction(count, deck_length)
        terminated_aggregate = AggregatedLine.from_card(terminator_card)
        statistics.normal.add_aggregated_line(terminated_aggregate, odds)

    short_rolling_combinations = Counter()
    short_rolling_combinations.update([FrozenMultiset(c) for c in itertools.combinations(rolling_cards, 1)])

    lengthy_rolling_combinations = Counter()
    for length in range(2, len(rolling_cards) + 1):
        lengthy_rolling_combinations.update([FrozenMultiset(c) for c in itertools.combinations(rolling_cards, length)])

    # unique_rolling_combinations = short_rolling_combinations + lengthy_rolling_combinations
    # validate_permutation_count(rolling_cards, unique_rolling_combinations)  # Debug assertion

    short_rolling = terminate_rolling_combos(counted_terminator_cards, deck_length, short_rolling_combinations)
    for terminated_line in short_rolling:
        # Advantage gets odds times two because either order can happen and count when advantaged.
        statistics.advantage.add_aggregated_line(terminated_line.aggregated_line, terminated_line.odds * EITHER_ORDER)
        statistics.normal.add_aggregated_line(terminated_line.aggregated_line, terminated_line.odds)

    lengthy_rolling = terminate_rolling_combos(counted_terminator_cards, deck_length, lengthy_rolling_combinations)
    for terminated_line in lengthy_rolling:
        statistics.advantage.add_aggregated_line(terminated_line.aggregated_line, terminated_line.odds)
        statistics.normal.add_aggregated_line(terminated_line.aggregated_line, terminated_line.odds)

    two_card_odds_factor = Fraction(1, deck_length * (deck_length - 1))
    advantaged_terminator_pairs = list(itertools.combinations(terminator_cards, 2))
    deck_statistics_by_atk = {}
    for atk in atk_range:
        new_statistics = DeckStatistics(statistics.normal.make_copy(), statistics.advantage.make_copy())
        for terminator_pair in advantaged_terminator_pairs:
            add_terminal_adv_to_stats(new_statistics.advantage, terminator_pair, atk, two_card_odds_factor)

        deck_statistics_by_atk[atk] = new_statistics

        deck_statistics_by_atk[atk].normal.calculate_expected_damage(atk)
        deck_statistics_by_atk[atk].advantage.calculate_expected_damage(atk)

    # for i in atk_range:
    #     assert deck_statistics_by_atk[i].normal.total_odds == 1  # Debug assertion
    #     assert deck_statistics_by_atk[i].advantage.total_odds == 1  # Debug assertion

    return deck_statistics_by_atk


def add_terminal_adv_to_stats(advantage_stats, terminator_pair, atk, two_card_odds_factor):
    cmp = terminator_pair[0].adv_compare(terminator_pair[1], atk)
    if cmp == -1:
        al = AggregatedLine.from_card(terminator_pair[1])
        advantage_stats.add_aggregated_line(al, two_card_odds_factor * EITHER_ORDER)
    elif cmp == 1:
        al = AggregatedLine.from_card(terminator_pair[0])
        advantage_stats.add_aggregated_line(al, two_card_odds_factor * EITHER_ORDER)
    else:
        a = AggregatedLine.from_card(terminator_pair[0])
        advantage_stats.add_aggregated_line(a, two_card_odds_factor)
        b = AggregatedLine.from_card(terminator_pair[1])
        advantage_stats.add_aggregated_line(b, two_card_odds_factor)


def terminate_rolling_combos(counted_terminator_cards, deck_length, rolling_combos) -> List[AggregatedLineWithOdds]:
    terminated_aggregated_lines_with_odds = []
    for rolling_line, rolling_line_occurrence_count in rolling_combos.items():
        rolling_permutations = rolling_line_occurrence_count * math.factorial(len(rolling_line))
        aggregated_rolling_line = AggregatedLine.from_line(rolling_line)
        terminated_line_length = len(rolling_line) + 1
        odds_denominator = reduce(operator.mul, range(deck_length, deck_length - terminated_line_length, -1), 1)
        for terminator_card, count in counted_terminator_cards.items():
            odds = Fraction(rolling_permutations * count, odds_denominator)
            terminated_aggregate_line = aggregated_rolling_line.add_card(terminator_card)

            terminated_aggregated_lines_with_odds.append(AggregatedLineWithOdds(terminated_aggregate_line, odds))

    return terminated_aggregated_lines_with_odds


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
