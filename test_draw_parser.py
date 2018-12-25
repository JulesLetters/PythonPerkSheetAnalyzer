from collections import Counter
from unittest import TestCase

from attack_drawer import Draws
from draw_parser import DrawParser, Result


class TestDrawParser(TestCase):

    def setUp(self):
        self.testObject = DrawParser()

    def test_simple_parse(self):
        draws = Draws(['+0'], 1)
        expected = Result(draws, Counter())

        actual = self.testObject.make_result(draws)
        self.assertEqual(expected, actual)

    def test_simple_effect(self):
        draws = Draws(['+0 STUN'], 1)
        expected = Result(draws, Counter({'STUN': 1}))

        actual = self.testObject.make_result(draws)
        self.assertEqual(expected, actual)

    def test_two_effects(self):
        draws = Draws(['R+0 STUN', '+0 STUN'], 1)
        expected = Result(draws, Counter({'STUN': 2}))

        actual = self.testObject.make_result(draws)
        self.assertEqual(expected, actual)

    def test_two_different_effects(self):
        draws = Draws(['R+0 MUDDLE', '+0 STUN'], 1)
        expected = Result(draws, Counter({'MUDDLE': 1, 'STUN': 1}))

        actual = self.testObject.make_result(draws)
        self.assertEqual(expected, actual)

    def test_rolling_modifier_in_reverse(self):
        draws = Draws(['+0 STUN', 'R+0 MUDDLE'], 1)
        expected = Result(draws, Counter({'MUDDLE': 1, 'STUN': 1}))

        actual = self.testObject.make_result(draws)
        self.assertEqual(expected, actual)

    def test_advantage_with_effects(self):
        draws = Draws(['+0 MUDDLE', '+0 STUN'], 2)
        expected = Result(draws, Counter({'MUDDLE': 1}))

        actual = self.testObject.make_result(draws)
        self.assertEqual(expected, actual)

    def test_advantage_with_two_terminating_effect_cards_selects_first_card(self):
        draws = Draws(['+0 STUN', '+0 MUDDLE'], 2)
        expected = Result(draws, Counter({'STUN': 1}))

        actual = self.testObject.make_result(draws)
        self.assertEqual(expected, actual)

    def test_advantage_makes_tied_number_and_effect_become_effect(self):
        draws_1 = Draws(['-2', '-2 MUDDLE'], 2)
        draws_2 = Draws(['+0', '+0 MUDDLE'], 2)
        draws_3 = Draws(['+2', '+2 MUDDLE'], 2)
        expected_1 = Result(draws_1, Counter({'MUDDLE': 1}))
        expected_2 = Result(draws_2, Counter({'MUDDLE': 1}))
        expected_3 = Result(draws_3, Counter({'MUDDLE': 1}))

        actual_1 = self.testObject.make_result(draws_1)
        actual_2 = self.testObject.make_result(draws_2)
        actual_3 = self.testObject.make_result(draws_3)
        self.assertEqual(expected_1, actual_1)
        self.assertEqual(expected_2, actual_2)
        self.assertEqual(expected_3, actual_3)

    def test_advantage_makes_tied_effect_and_number_become_effect(self):
        draws_1 = Draws(['-2 MUDDLE', '-2'], 2)
        draws_2 = Draws(['+0 MUDDLE', '+0'], 2)
        draws_3 = Draws(['+2 MUDDLE', '+2'], 2)
        expected_1 = Result(draws_1, Counter({'MUDDLE': 1}))
        expected_2 = Result(draws_2, Counter({'MUDDLE': 1}))
        expected_3 = Result(draws_3, Counter({'MUDDLE': 1}))

        actual_1 = self.testObject.make_result(draws_1)
        actual_2 = self.testObject.make_result(draws_2)
        actual_3 = self.testObject.make_result(draws_3)
        self.assertEqual(expected_1, actual_1)
        self.assertEqual(expected_2, actual_2)
        self.assertEqual(expected_3, actual_3)

    def test_greater_number_first_with_advantage_precedes_effect(self):
        draws_1 = Draws(['-1', '-2 MUDDLE'], 2)
        draws_2 = Draws(['+1', '+0 MUDDLE'], 2)
        draws_3 = Draws(['+3', '+2 MUDDLE'], 2)
        expected_1 = Result(draws_1, Counter())
        expected_2 = Result(draws_2, Counter())
        expected_3 = Result(draws_3, Counter())

        actual_1 = self.testObject.make_result(draws_1)
        actual_2 = self.testObject.make_result(draws_2)
        actual_3 = self.testObject.make_result(draws_3)
        self.assertEqual(expected_1, actual_1)
        self.assertEqual(expected_2, actual_2)
        self.assertEqual(expected_3, actual_3)

    def test_effect_with_advantage_precedes_greater_number_if_first(self):
        draws_1 = Draws(['-2 MUDDLE', '-1'], 2)
        draws_2 = Draws(['+0 MUDDLE', '+1'], 2)
        draws_3 = Draws(['+2 MUDDLE', '+3'], 2)
        expected_1 = Result(draws_1, Counter({'MUDDLE': 1}))
        expected_2 = Result(draws_2, Counter({'MUDDLE': 1}))
        expected_3 = Result(draws_3, Counter({'MUDDLE': 1}))

        actual_1 = self.testObject.make_result(draws_1)
        actual_2 = self.testObject.make_result(draws_2)
        actual_3 = self.testObject.make_result(draws_3)
        self.assertEqual(expected_1, actual_1)
        self.assertEqual(expected_2, actual_2)
        self.assertEqual(expected_3, actual_3)

    def test_effect_with_advantage_always_beats_null(self):
        draws_1 = Draws(['x0', '-4 MUDDLE'], 2)
        expected_1 = Result(draws_1, Counter({'MUDDLE': 1}))

        actual_1 = self.testObject.make_result(draws_1)
        self.assertEqual(expected_1, actual_1)

    def test_effect_first_with_advantage_precedes_critical(self):
        draws_1 = Draws(['-4 MUDDLE', 'x2'], 2)
        expected_1 = Result(draws_1, Counter({'MUDDLE': 1}))

        actual_1 = self.testObject.make_result(draws_1)
        self.assertEqual(expected_1, actual_1)

    def test_critical_with_advantage_is_ambiguous_with_effect(self):
        draws_1 = Draws(['x2', '-4 MUDDLE'], 2)
        expected_1 = Result(draws_1, Counter())

        actual_1 = self.testObject.make_result(draws_1)
        self.assertEqual(expected_1, actual_1)
