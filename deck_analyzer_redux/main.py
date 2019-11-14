import itertools
import math
from collections import Counter

from multiset import FrozenMultiset

from deck_analyzer_redux import perk_sheets, deck_generator


def unique_ordered_combinations(string_counts, length):
    return set(["".join(sorted(c)) for c in itertools.combinations(string_counts, length)])


def main():
    decks_and_generation_methods = deck_generator.all_decks_and_generations_for(perk_sheets.three_spears)
    deck_count = len(decks_and_generation_methods)
    print("Decks to analyze: {}".format(deck_count))

    for deck in decks_and_generation_methods:
        # Of all possible unique decks, there's still a lot of non-unique rolling and terminator collections.
        # That means an optimization is possible here, caching the result of this loop for given collections.
        # (This isn't done, but should be done at some point)
        rolling_cards = [card for card in deck if is_rolling(card)]
        terminator_cards = [card for card in deck if not is_rolling(card)]

        print()
        print(rolling_cards)

        # The count is here is the number of ways the set of rolling cards can be GENERATED INTO a deck,
        # Not the ways it can be drawn OUT of a deck.

        # However, this is the same as the numerator of the probability of drawing out it.

        rolling_combination_counts = Counter()
        for i in range(0, len(rolling_cards) + 1):
            rolling_combination_counts.update([FrozenMultiset(c) for c in itertools.combinations(rolling_cards, i)])

        for line, combination_occurrences in rolling_combination_counts.items():
            permutations = combination_occurrences * math.factorial(len(line))
            # Success!
            # print(line, permutations)
        # Okay, we've got the rolling permutation odds.
        # While going through the line, we should aggregate the cards.
        # Then, depending on advantage:
        # 0 rolling: 2 terminators. Rolling isn't used. Analyze and pick better.
        # 1 rolling: 1 terminator is used. Aggregate rolls and terminators. Cartesian join.
        # 2 rolling: 1 terminator is used. Aggregate rolls and terminators. Cartesian join.

        # s = defaultdict(int)
        # for line, combination_occurrences in rolling_combination_counts.items():
        #     permutations = combination_occurrences * math.factorial(len(line))
        #     s[len(line)] += permutations
        # for line_length, actual_permutations in s.items():
        #     rc_count = len(rolling_cards)
        #     expected_permutations = math.factorial(rc_count) // math.factorial(rc_count - line_length)
        #     print(line_length, actual_permutations, expected_permutations)
        #     assert actual_permutations == expected_permutations

    print('done')

    # We've got all the decks, and rather quickly.
    # Separate rolling and terminators.
    # Do rolling fractional frequency analysis.
    # Do analysis of the prefixes to see the result (atk bonus, effect-trigger boolean, effect-repetition.)
    # Do terminator analysis of the above.
    # Multiply rolling and terminators, reduce.
    # Present results.

    # for line_length, v in decks_and_generation_methods.items():
    #     print(line_length, v)
    # x = timeit.timeit(lambda: deck_generator.all_decks_and_generations_for(perk_sheets.three_spears), number=1000)
    # print(x)
    # Around 100ms. Good enough!

    # return object:
    #


def is_rolling(card: str) -> bool:
    return card.startswith('R')


if __name__ == '__main__':
    main()
