import unittest
from fractions import Fraction

from multiset import FrozenMultiset

from perk_sheet_analyzer import deck_analyzer
import perk_sheet_analyzer.cards as cards


class TestDeckAnalyzer(unittest.TestCase):
    def test_two_0s(self):
        base_attack = 5
        atk_range = range(base_attack, base_attack + 1)
        deck = [cards.plus_0] * 2
        statistics_by_atk = deck_analyzer.derive_statistics(FrozenMultiset(deck), atk_range)

        self.assertEqual(5, statistics_by_atk[base_attack].normal.expected_damage)
        self.assertEqual(5, statistics_by_atk[base_attack].advantage.expected_damage)

    def test_two_1s(self):
        base_attack = 5
        atk_range = range(base_attack, base_attack + 1)
        deck = [cards.plus_1] * 2
        statistics_by_atk = deck_analyzer.derive_statistics(FrozenMultiset(deck), atk_range)

        self.assertEqual(6, statistics_by_atk[base_attack].normal.expected_damage)
        self.assertEqual(6, statistics_by_atk[base_attack].advantage.expected_damage)

    def test_0_and_x2(self):
        base_attack = 5
        atk_range = range(base_attack, base_attack + 1)
        deck = [cards.plus_0] + [cards.times_2]
        statistics_by_atk = deck_analyzer.derive_statistics(FrozenMultiset(deck), atk_range)

        self.assertEqual(Fraction(5 + 10, 2), statistics_by_atk[base_attack].normal.expected_damage)
        self.assertEqual(10, statistics_by_atk[base_attack].advantage.expected_damage)

    def test_0_and_x0(self):
        base_attack = 5
        atk_range = range(base_attack, base_attack + 1)
        deck = [cards.plus_0] + [cards.times_0]
        statistics_by_atk = deck_analyzer.derive_statistics(FrozenMultiset(deck), atk_range)

        self.assertEqual(Fraction(5 + 0, 2), statistics_by_atk[base_attack].normal.expected_damage)
        self.assertEqual(5, statistics_by_atk[base_attack].advantage.expected_damage)

    def test_0_and_1(self):
        base_attack = 5
        atk_range = range(base_attack, base_attack + 1)
        deck = [cards.plus_0] + [cards.plus_1]
        statistics_by_atk = deck_analyzer.derive_statistics(FrozenMultiset(deck), atk_range)

        self.assertEqual(Fraction(5 + 6, 2), statistics_by_atk[base_attack].normal.expected_damage)
        self.assertEqual(6, statistics_by_atk[base_attack].advantage.expected_damage)


if __name__ == '__main__':
    unittest.main()
