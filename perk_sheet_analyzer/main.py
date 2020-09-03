from collections import defaultdict
from typing import NamedTuple, List, Dict

from multiset import FrozenMultiset

from perk_sheet_analyzer import perk_sheets, deck_generator, deck_analyzer
from perk_sheet_analyzer.deck_analyzer import DeckStatistics
from perk_sheet_analyzer.deck_generator import NamedPerk
from perk_sheet_analyzer.simple_timer_context import SimpleTimerContext


class Analysis(NamedTuple):
    statistics_by_atk: Dict[int, DeckStatistics]
    generation_methods: List[List[NamedPerk]]


def main():
    atk_range = range(0, 4)
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

            statistics_by_atk = deck_analyzer.derive_statistics(deck, atk_range)
            all_analysis[deck] = Analysis(statistics_by_atk, generation_methods)
        print("")

    maximum_damage_example(all_analysis)
    three_spears_refresh_item_example(all_analysis)

    print('Done!')


def maximum_damage_example(all_analysis: Dict[FrozenMultiset, Analysis]) -> None:
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


def three_spears_refresh_item_example(all_analysis: Dict[FrozenMultiset, Analysis]) -> None:
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


if __name__ == '__main__':
    main()
