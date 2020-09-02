import itertools
import math
import operator
from collections import Counter, defaultdict, namedtuple
from fractions import Fraction
from functools import reduce
from typing import List, Dict

from multiset import FrozenMultiset

from deck_analyzer import perk_sheets, deck_generator
from deck_analyzer.aggregated_line import AggregatedLine
from deck_analyzer.deck_scheme_statistics import DrawSchemeStatistics
from deck_analyzer.simple_timer_context import SimpleTimerContext

ATK_RANGE = range(0, 4)
EITHER_ORDER = 2
AggregatedLineWithOdds = namedtuple("AggregatedLineWithOdds", "aggregated_line odds")
DeckStatistics = namedtuple("DeckStatistics", "normal advantage")
Analysis = namedtuple("Analysis", "statistics_by_atk generation_methods")


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

    # Split between critical and non-critical terminators.
    # Critical x Non-critical are mixed in the double terminal section.
    critical_terminators = [c for c in terminator_cards if c.is_critical]
    non_critical_terminators = [c for c in terminator_cards if not c.is_critical]

    # Avoid doing pointless iterations of comparing x2. This won't happen without bless, shuffles, or redraws.
    critical_terminator_count = len(critical_terminators)
    any_critical_card = critical_terminators[0]
    if critical_terminator_count > 1:
        double_critical_odds = Fraction(critical_terminator_count * (critical_terminator_count - 1), deck_length)
        al = AggregatedLine.from_card(any_critical_card)
        statistics.advantage.add_aggregated_line(al, double_critical_odds)

    two_card_odds_factor = Fraction(1, deck_length * (deck_length - 1))
    advantaged_terminator_pairs = list(itertools.combinations(non_critical_terminators, 2))
    deck_statistics_by_atk = {}
    for atk in atk_range:
        new_statistics = DeckStatistics(statistics.normal.make_copy(), statistics.advantage.make_copy())
        for terminator_pair in advantaged_terminator_pairs:
            add_terminal_adv_to_stats(new_statistics.advantage, terminator_pair, atk, two_card_odds_factor)

        for terminator in non_critical_terminators:
            terminator_pair = (any_critical_card, terminator)
            add_terminal_adv_to_stats(new_statistics.advantage, terminator_pair, atk, two_card_odds_factor)

        deck_statistics_by_atk[atk] = new_statistics

        deck_statistics_by_atk[atk].normal.calculate_expected_damage(atk)
        deck_statistics_by_atk[atk].advantage.calculate_expected_damage(atk)

    # for i in ATK_RANGE:
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


def main():
    decks_and_generation_methods = deck_generator.all_decks_and_generations_for(perk_sheets.three_spears)
    deck_count = len(decks_and_generation_methods)
    print("Decks to analyze: {}".format(deck_count))

    all_analysis = {}
    n = 0
    with SimpleTimerContext("Calculating all character decks."):
        for deck, generation_methods in decks_and_generation_methods.items():
            n += 1
            if n % 100 == 0:
                print(".", end="", flush=True)

            statistics_by_atk = derive_statistics(deck, ATK_RANGE)
            all_analysis[deck] = Analysis(statistics_by_atk, generation_methods)
        print("")

    maximum_damage_example(all_analysis)
    three_spears_refresh_item_example(all_analysis)

    print('Done!')


def maximum_damage_example(all_analysis):
    chosen_atk = 3
    decks_by_expected_damage = defaultdict(list)
    for deck, analysis in all_analysis.items():
        expected_damage = analysis.statistics_by_atk[chosen_atk].normal.expected_damage
        decks_by_expected_damage[expected_damage].append(analysis.generation_methods)

    level_9_decks = defaultdict(list)
    for expected_damage, generation_methods in decks_by_expected_damage.items():
        for method in generation_methods:
            if len(method[0]) >= 8:
                level_9_decks[expected_damage].append(method)
    top_four_expected_damages = sorted(level_9_decks.keys())[-4:]
    print("Top four expected damages: ", top_four_expected_damages)

    for expected_damage in top_four_expected_damages:
        print(expected_damage)
        print("Ways to generate this deck:")
        for generation_methods in level_9_decks[expected_damage]:
            for generation_method in generation_methods:
                perk_names = [perk.name for perk in generation_method]
                print(perk_names)


def three_spears_refresh_item_example(all_analysis):
    print("Ways to maximum Refresh Item, with Advantage:")
    chosen_atk = 3
    all_deck_at_given_atk_statistics = {}
    for deck, analysis in all_analysis.items():
        statistics_at_chosen_atk = analysis.statistics_by_atk[chosen_atk]
        generation_methods = analysis.generation_methods
        all_deck_at_given_atk_statistics[deck] = {'statistics': statistics_at_chosen_atk,
                                                  'generation_methods': generation_methods}

    decks_by_odds = defaultdict(list)
    for deck, analysis in all_deck_at_given_atk_statistics.items():
        odds = analysis['statistics'].advantage.countable_effect_odds[("Refresh_Item_Self", 1)]
        decks_by_odds[odds].append(analysis['generation_methods'])

    level_9_decks = defaultdict(list)

    for odds, generation_methods in decks_by_odds.items():
        for method in generation_methods:
            if len(method[0]) >= 8:
                level_9_decks[odds].append(method)
    top_four_odds = sorted(level_9_decks.keys())[-4:]
    print("Top four odds: ", top_four_odds)

    for odds in top_four_odds:
        print(odds)
        print("Ways to generate this deck:")
        for generation_methods in level_9_decks[odds]:
            for generation_method in generation_methods:
                perk_names = [perk.name for perk in generation_method]
                print(perk_names)


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
