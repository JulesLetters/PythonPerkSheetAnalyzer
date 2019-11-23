from fractions import Fraction
from unittest import TestCase

from multiset import FrozenMultiset

import deck_analyzer


class TestDeckAnalyzer(TestCase):
    def test_deck_with_one_ice(self):
        deck = FrozenMultiset(['+2', '+1', '+0 ICE'])

        actual = deck_analyzer.calculate_statistics(deck)

        self.assertEqual(Fraction(1, 3), actual.effect_rates['ICE'])

    def test_deck_with_two_ice(self):
        deck = FrozenMultiset(['+2', '+0 ICE', '+0 ICE'])

        actual = deck_analyzer.calculate_statistics(deck)

        self.assertEqual(Fraction(2, 3), actual.effect_rates['ICE'])

    def test_deck_with_two_different_ice(self):
        deck = FrozenMultiset(['+2', '+1 ICE', '+0 ICE'])

        actual = deck_analyzer.calculate_statistics(deck)

        self.assertEqual(Fraction(2, 3), actual.effect_rates['ICE'])

    def test_deck_with_two_different_elements_aggregates_them_separately(self):
        deck = FrozenMultiset(['+2', '+1 FIRE', '+1 ICE', '+0 ICE'])

        actual = deck_analyzer.calculate_statistics(deck)

        self.assertEqual(Fraction(1, 4), actual.effect_rates['FIRE'])
        self.assertEqual(Fraction(2, 4), actual.effect_rates['ICE'])

    def test_deck_with_one_rolling_modifier(self):
        deck = FrozenMultiset(['R+0', '+0', '+0 ICE'])

        actual = deck_analyzer.calculate_statistics(deck)

        self.assertEqual(Fraction(3, 6), actual.effect_rates['ICE'])

    def test_deck_with_one_rolling_modifier_and_two_different_quantities_of_elements(self):
        deck = FrozenMultiset(['R+0', '+0', '+0 FIRE', '+0 ICE', '+0 ICE'])

        actual = deck_analyzer.calculate_statistics(deck)

        self.assertEqual(Fraction(5, 20), actual.effect_rates['FIRE'])
        self.assertEqual(Fraction(10, 20), actual.effect_rates['ICE'])

    def test_deck_with_two_rolling_modifiers_and_one_ice(self):
        deck = FrozenMultiset(['R+0', 'R+0', '+0', '+0 ICE'])

        actual = deck_analyzer.calculate_statistics(deck)

        self.assertEqual(Fraction(1, 2), actual.effect_rates['ICE'])

    def test_deck_with_three_rolling_modifiers_two_ice_and_three_fire(self):
        deck = FrozenMultiset(['R+0', 'R+0', 'R+0',
                               '+0 ICE', '+0 ICE',
                               '+0 FIRE', '+0 FIRE', '+0 FIRE'])

        actual = deck_analyzer.calculate_statistics(deck)

        self.assertEqual(Fraction(2, 5), actual.effect_rates['ICE'])
        self.assertEqual(Fraction(3, 5), actual.effect_rates['FIRE'])

    def test_deck_with_ice_on_rolling_modifier(self):
        deck = FrozenMultiset(['R+0 ICE', '+0', '+0'])

        actual = deck_analyzer.calculate_statistics(deck)

        self.assertEqual(Fraction(1, 3), actual.effect_rates['ICE'])

    def test_deck_with_two_ice_on_rolling_modifiers(self):
        deck = FrozenMultiset(['R+0 ICE', 'R+0 ICE', '+0'])

        actual = deck_analyzer.calculate_statistics(deck)

        self.assertEqual(Fraction(2, 3), actual.effect_rates['ICE'])

    def test_deck_with_three_ice_on_rolling_modifiers(self):
        deck = FrozenMultiset(['R+0 ICE', 'R+0 ICE', 'R+0 ICE',
                               '+0', '+0', '+0'])

        actual = deck_analyzer.calculate_statistics(deck)

        self.assertEqual(Fraction(1, 2), actual.effect_rates['ICE'])

    def test_deck_with_ice_on_rolling_modifier_and_ice_on_terminator(self):
        deck = FrozenMultiset(['R+0 ICE', '+0', '+0 ICE'])

        actual = deck_analyzer.calculate_statistics(deck)

        self.assertEqual(Fraction(2, 3), actual.effect_rates['ICE'])

    def test_deck_with_ice_on_rolling_modifier_and_two_ice_on_terminator(self):
        deck = FrozenMultiset(['R+0 ICE', '+0', '+0 ICE', '+0 ICE'])

        actual = deck_analyzer.calculate_statistics(deck)

        self.assertEqual(Fraction(3, 4), actual.effect_rates['ICE'])

    def test_deck_with_three_rolling_ice_and_two_terminating_ice_and_one_zero(self):
        deck = FrozenMultiset(['R+0 ICE', 'R+0 ICE', 'R+0 ICE',
                               '+0',
                               '+0 ICE', '+0 ICE'])

        actual = deck_analyzer.calculate_statistics(deck)

        self.assertEqual(Fraction(2, 3), actual.effect_rates['ICE'])

    def test_deck_with_three_rolling_ice_and_two_terminating_ice_and_two_zeroes(self):
        deck = FrozenMultiset(['R+0 ICE', 'R+0 ICE', 'R+0 ICE',
                               '+0', '+0'
                               '+0 ICE', '+0 ICE'])

        actual = deck_analyzer.calculate_statistics(deck)

        self.assertEqual(Fraction(1, 2), actual.effect_rates['ICE'])
