from unittest import TestCase

from multiset import FrozenMultiset

import deck_generator
import perks


class TestGenerateAllDecksFor(TestCase):

    def test_generate_default_deck(self):
        deck_1 = FrozenMultiset(['+0', '+0', '+0', '+0', '+0', '+0',
                                 '+1', '+1', '+1', '+1', '+1',
                                 '-1', '-1', '-1', '-1', '-1',
                                 '-2', '+2', 'x0', 'x2'])
        expected = {deck_1}
        actual = deck_generator.generate_all_decks_for([perks.none])

        self.assertEqual(expected, actual)

    def test_generate_one_perk_decks(self):
        deck_1 = FrozenMultiset(['+0', '+0', '+0', '+0', '+0', '+0',
                                 '+1', '+1', '+1', '+1', '+1',
                                 '-1', '-1', '-1', '-1', '-1',
                                 '-2', '+2', 'x0', 'x2'])
        deck_2 = FrozenMultiset(['+0', '+0', '+0', '+0', '+0', '+0',
                                 '+1', '+1', '+1', '+1', '+1', '+1', '+1',
                                 '-1', '-1', '-1', '-1', '-1',
                                 '-2', '+2', 'x0', 'x2'])
        expected = {deck_1, deck_2}
        actual = deck_generator.generate_all_decks_for([perks.add_two_plus_ones])

        self.assertEqual(expected, actual)

    def test_generate_two_perks_decks(self):
        deck_1 = FrozenMultiset(['+0', '+0', '+0', '+0', '+0', '+0',
                                 '+1', '+1', '+1', '+1', '+1',
                                 '-1', '-1', '-1', '-1', '-1',
                                 '-2', '+2', 'x0', 'x2'])
        deck_2 = FrozenMultiset(['+0', '+0', '+0', '+0', '+0', '+0',
                                 '+1', '+1', '+1', '+1', '+1', '+1', '+1',
                                 '-1', '-1', '-1', '-1', '-1',
                                 '-2', '+2', 'x0', 'x2'])
        deck_3 = FrozenMultiset(['+0', '+0',
                                 '+1', '+1', '+1', '+1', '+1',
                                 '-1', '-1', '-1', '-1', '-1',
                                 '-2', '+2', 'x0', 'x2'])
        deck_4 = FrozenMultiset(['+0', '+0',
                                 '+1', '+1', '+1', '+1', '+1', '+1', '+1',
                                 '-1', '-1', '-1', '-1', '-1',
                                 '-2', '+2', 'x0', 'x2'])
        expected = {deck_1, deck_2, deck_3, deck_4}
        actual = deck_generator.generate_all_decks_for([perks.add_two_plus_ones,
                                                        perks.remove_four_zeroes])
        self.assertEqual(expected, actual)
