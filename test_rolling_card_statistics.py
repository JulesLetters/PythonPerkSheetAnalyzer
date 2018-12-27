from collections import Counter
from unittest import TestCase

from multiset import FrozenMultiset

import rolling_card_statistics


class TestRollingCardStatistics(TestCase):
    def test_no_rolling_modifiers(self):
        deck = FrozenMultiset(['+0', '+0', '+0'])
        expected = Counter({FrozenMultiset(): 1})

        actual = rolling_card_statistics.generate(deck)
        self.assertEqual(expected, actual)

    def test_one_rolling_modifier(self):
        deck = FrozenMultiset(['+0', 'R+0', '+0'])
        expected = Counter({FrozenMultiset(): 1,
                            FrozenMultiset({'R+0'}): 1})

        actual = rolling_card_statistics.generate(deck)
        self.assertEqual(expected, actual)

    def test_two_rolling_modifiers_get_combined(self):
        deck = FrozenMultiset(['+0', 'R+0', 'R+1'])
        expected = Counter({FrozenMultiset(): 1,
                            FrozenMultiset({'R+0'}): 1,
                            FrozenMultiset({'R+1'}): 1,
                            FrozenMultiset({'R+0', 'R+1'}): 2})

        actual = rolling_card_statistics.generate(deck)
        self.assertEqual(expected, actual)

    def test_two_equal_name_rolling_modifiers_are_counted_in_same_bucket(self):
        deck = FrozenMultiset(['+0', 'R+0', 'R+0'])
        expected = Counter({FrozenMultiset(): 1,
                            FrozenMultiset({'R+0'}): 2,
                            FrozenMultiset({'R+0': 2}): 2})

        actual = rolling_card_statistics.generate(deck)
        self.assertEqual(expected, actual)

    def test_two_equal_name_rolling_modifiers_and_one_different(self):
        deck = FrozenMultiset(['+0', 'R+0', 'R+0', 'R+1'])
        expected = Counter({FrozenMultiset(): 1,
                            FrozenMultiset({'R+0': 1}): 2,
                            FrozenMultiset({'R+1': 1}): 1,
                            FrozenMultiset({'R+0': 2}): 2,
                            FrozenMultiset({'R+0': 1, 'R+1': 1}): 4,
                            FrozenMultiset({'R+0': 2, 'R+1': 1}): 6
                            })

        actual = rolling_card_statistics.generate(deck)
        self.assertEqual(expected, actual)

    def test_three_card_types_with_two_duplicate_types(self):
        deck = FrozenMultiset(['R+0', 'R+0', 'R+1', 'R+1', 'R+2'])
        expected = Counter({FrozenMultiset(): 1,

                            FrozenMultiset({'R+0'}): 2,
                            FrozenMultiset({'R+1'}): 2,
                            FrozenMultiset({'R+2'}): 1,

                            FrozenMultiset({'R+0': 2}): 2,
                            FrozenMultiset({'R+0': 1, 'R+1': 1}): 8,
                            FrozenMultiset({'R+0': 1, 'R+2': 1}): 4,
                            FrozenMultiset({'R+1': 2}): 2,
                            FrozenMultiset({'R+1': 1, 'R+2': 1}): 4,

                            FrozenMultiset({'R+0': 2, 'R+1': 1}): 12,
                            FrozenMultiset({'R+0': 2, 'R+2': 1}): 6,
                            FrozenMultiset({'R+0': 1, 'R+1': 2}): 12,
                            FrozenMultiset({'R+0': 1, 'R+1': 1, 'R+2': 1}): 24,
                            FrozenMultiset({'R+1': 2, 'R+2': 1}): 6,

                            FrozenMultiset({'R+0': 2, 'R+1': 2}): 24,
                            FrozenMultiset({'R+0': 2, 'R+1': 1, 'R+2': 1}): 48,
                            FrozenMultiset({'R+0': 1, 'R+1': 2, 'R+2': 1}): 48,

                            FrozenMultiset({'R+0': 2, 'R+1': 2, 'R+2': 1}): 120
                            })

        actual = rolling_card_statistics.generate(deck)
        self.assertEqual(expected, actual)

    def test_three_duplicates_of_the_same_card_type(self):
        deck = FrozenMultiset(['R+0', 'R+1', 'R+1', 'R+1'])
        expected = Counter({FrozenMultiset(): 1,

                            FrozenMultiset({'R+0'}): 1,
                            FrozenMultiset({'R+1'}): 3,

                            FrozenMultiset({'R+0': 1, 'R+1': 1}): 6,
                            FrozenMultiset({'R+1': 2}): 6,

                            FrozenMultiset({'R+0': 1, 'R+1': 2}): 18,
                            FrozenMultiset({'R+1': 3}): 6,

                            FrozenMultiset({'R+0': 1, 'R+1': 3}): 24,
                            })

        actual = rolling_card_statistics.generate(deck)
        self.assertEqual(expected, actual)
