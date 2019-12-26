import itertools
import math
import operator
from collections import Counter, defaultdict, namedtuple
from fractions import Fraction
from functools import reduce
from typing import Iterable, List

from multiset import FrozenMultiset

from deck_analyzer import perk_sheets, deck_generator
from deck_analyzer.cards import Card
from deck_analyzer.simple_timer_context import SimpleTimerContext


def unique_ordered_combinations(string_counts, length):
    return set(["".join(sorted(c)) for c in itertools.combinations(string_counts, length)])


ATK_RANGE = range(0, 26)
EITHER_ORDER = 2
IRRELEVANT_ATTACK = 3
AggregateLine = namedtuple("AggregateLine", "atk_calculation countable_effects singular_effects")
AggregateLineWithOdds = namedtuple("AggregateLineWithOdds", "aggregate_line odds")
Statistics = namedtuple("Statistics", "normal advantage")


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

    def add_aggregate(self, aggregate: AggregateLine, odds: Fraction) -> None:
        for effect, count in aggregate.countable_effects.items():
            self.countable_effect_odds[(effect, count)] += odds
            self.singular_effect_odds[effect] += odds  # Chance a countable occurred.
        for effect in aggregate.singular_effects:
            self.singular_effect_odds[effect] += odds
        self.total_odds += odds

    def make_copy(self):
        copy = DeckStatistics(self.generation_methods)
        copy.countable_effect_odds = self.countable_effect_odds.copy()
        copy.singular_effect_odds = self.singular_effect_odds.copy()
        copy.total_odds = self.total_odds
        return copy


def analyze_deck(deck, generation_methods) -> List[Statistics]:
    statistics = Statistics(DeckStatistics(generation_methods), DeckStatistics(generation_methods))

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
        terminated_aggregate = card_to_aggregate_line(terminator_card)

        statistics.normal.add_aggregate(terminated_aggregate, odds)

    short_rolling_combinations = Counter()
    short_rolling_combinations.update([FrozenMultiset(c) for c in itertools.combinations(rolling_cards, 1)])

    lengthy_rolling_combinations = Counter()
    for atk in range(2, len(rolling_cards) + 1):
        lengthy_rolling_combinations.update([FrozenMultiset(c) for c in itertools.combinations(rolling_cards, atk)])

    # validate_permutation_count(rolling_cards, unique_rolling_combinations)  # Debug assertion

    short_rolling = analyze_rolling_combos(counted_terminator_cards, deck_length, short_rolling_combinations)
    for terminated_line in short_rolling:
        # Advantage gets odds times two because either order can happen and count when advantaged.
        statistics.advantage.add_aggregate(terminated_line.aggregate_line, terminated_line.odds * EITHER_ORDER)
        statistics.normal.add_aggregate(terminated_line.aggregate_line, terminated_line.odds)

    lengthy_rolling = analyze_rolling_combos(counted_terminator_cards, deck_length, lengthy_rolling_combinations)
    for terminated_line in lengthy_rolling:
        statistics.advantage.add_aggregate(terminated_line.aggregate_line, terminated_line.odds)
        statistics.normal.add_aggregate(terminated_line.aggregate_line, terminated_line.odds)

    critical_terminators = [c for c in terminator_cards if c.is_critical]
    non_critical_terminators = [c for c in terminator_cards if not c.is_critical]

    two_card_odds_denominator = Fraction(1, deck_length * (deck_length - 1))
    advantage_terminators = itertools.combinations(non_critical_terminators, 2)
    for terminator_pair in advantage_terminators:
        add_terminal_adv_to_stats(statistics.advantage, terminator_pair, IRRELEVANT_ATTACK, two_card_odds_denominator)

    critical_terminator_count = len(critical_terminators)

    any_critical_card = critical_terminators[0]
    if critical_terminator_count > 1:
        double_critical_odds = Fraction(critical_terminator_count * (critical_terminator_count - 1), deck_length)
        al = card_to_aggregate_line(any_critical_card)
        statistics.advantage.add_aggregate(al, double_critical_odds)

    result = []
    for atk in ATK_RANGE:
        new_statistics = Statistics(statistics.normal, statistics.advantage.make_copy())
        for terminator in non_critical_terminators:
            terminator_pair = (any_critical_card, terminator)
            add_terminal_adv_to_stats(new_statistics.advantage, terminator_pair, atk, two_card_odds_denominator)
        result.append(new_statistics)

    return result


def add_terminal_adv_to_stats(advantage_stats, terminator_pair, atk, two_card_odds_denominator):
    cmp = terminator_pair[0].adv_compare(terminator_pair[1], atk)
    if cmp == -1:
        al = card_to_aggregate_line(terminator_pair[1])
        advantage_stats.add_aggregate(al, two_card_odds_denominator * EITHER_ORDER)
    elif cmp == 1:
        al = card_to_aggregate_line(terminator_pair[0])
        advantage_stats.add_aggregate(al, two_card_odds_denominator * EITHER_ORDER)
    else:
        a = card_to_aggregate_line(terminator_pair[0])
        advantage_stats.add_aggregate(a, two_card_odds_denominator)
        b = card_to_aggregate_line(terminator_pair[1])
        advantage_stats.add_aggregate(b, two_card_odds_denominator)


def analyze_rolling_combos(counted_terminator_cards, deck_length, rolling_combinations) -> List[AggregateLineWithOdds]:
    result = []
    for line, line_occurrence_count in rolling_combinations.items():
        rolling_permutations = line_occurrence_count * math.factorial(len(line))
        aggregate_line_results = make_aggregate_line_results(line)
        sequence_length = len(line) + 1
        denominator = reduce(operator.mul, range(deck_length, deck_length - sequence_length, -1), 1)
        for terminator_card, count in counted_terminator_cards.items():
            odds = Fraction(rolling_permutations * count, denominator)
            terminated_aggregate = add_card_to_aggregate_line_results(terminator_card, aggregate_line_results)

            result.append(AggregateLineWithOdds(terminated_aggregate, odds))

    return result


def main():
    decks_and_generation_methods = deck_generator.all_decks_and_generations_for(perk_sheets.three_spears)
    deck_count = len(decks_and_generation_methods)
    print("Decks to analyze: {}".format(deck_count))

    all_deck_statistics = {}
    n = 0
    for deck, generation_methods in decks_and_generation_methods.items():
        n += 1
        if n % 100 == 0:
            print(".", end="", flush=True)

        all_atk_statistics = analyze_deck(deck, generation_methods)
        statistics = all_atk_statistics[3]
        all_deck_statistics[deck] = statistics
        # for i in ATK_RANGE:
        #     assert all_atk_statistics[i].normal.total_odds == 1  # Debug assertion
        #     assert all_atk_statistics[i].advantage.total_odds == 1  # Debug assertion
    print("")

    decks_by_odds = defaultdict(list)
    for deck, statistics in all_deck_statistics.items():
        odds = statistics.advantage.countable_effect_odds[("Refresh_Item", 1)]
        decks_by_odds[odds].append(statistics.advantage.generation_methods)

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
