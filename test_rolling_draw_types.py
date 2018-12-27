from unittest import TestCase

from multiset import FrozenMultiset

import rolling_draw_types


class TestRollingDrawTypes(TestCase):
    def test_one_card_outputs_one_and_empty(self):
        deck = FrozenMultiset(['R+0'])
        expected = {FrozenMultiset(),
                    FrozenMultiset({'R+0': 1})}

        actual = rolling_draw_types.generate_from(deck)
        self.assertEqual(expected, actual)

    def test_two_cards_outputs_all_combinations(self):
        deck = FrozenMultiset(['R+0', 'R+1'])
        expected = {FrozenMultiset(),
                    FrozenMultiset({'R+0': 1}),
                    FrozenMultiset({'R+1': 1}),
                    FrozenMultiset({'R+0': 1, 'R+1': 1})}

        actual = rolling_draw_types.generate_from(deck)
        self.assertEqual(expected, actual)

    def test_two_identical_cards_outputs_one_and_two_draws(self):
        deck = FrozenMultiset(['R+0', 'R+0'])
        expected = {FrozenMultiset(),
                    FrozenMultiset({'R+0': 1}),
                    FrozenMultiset({'R+0': 2})}

        actual = rolling_draw_types.generate_from(deck)
        self.assertEqual(expected, actual)

    def test_two_identical_cards_and_one_different_outputs_one_and_two_draws(self):
        deck = FrozenMultiset(['R+0', 'R+0', 'R+1'])
        expected = {FrozenMultiset(),
                    FrozenMultiset({'R+0': 1}),
                    FrozenMultiset({'R+1': 1}),
                    FrozenMultiset({'R+0': 2}),
                    FrozenMultiset({'R+0': 1, 'R+1': 1}),
                    FrozenMultiset({'R+0': 2, 'R+1': 1})
                    }

        actual = rolling_draw_types.generate_from(deck)
        self.assertEqual(expected, actual)
