from collections import Counter
from unittest import TestCase

from attack_drawer import Draw
from draw_parser import DrawParser, Result


class TestDrawParser(TestCase):

    def setUp(self):
        self.testObject = DrawParser()

    def test_simple_parse(self):
        draw = Draw(['+0'], 1)
        expected = Result(draw, Counter())

        actual = self.testObject.make_result(draw)
        self.assertEqual(expected, actual)

    def test_simple_effect(self):
        draw = Draw(['+0 STUN'], 1)
        expected = Result(draw, Counter({'STUN': 1}))

        actual = self.testObject.make_result(draw)
        self.assertEqual(expected, actual)

    def test_two_effects(self):
        draw = Draw(['R+0 STUN', '+0 STUN'], 1)
        expected = Result(draw, Counter({'STUN': 2}))

        actual = self.testObject.make_result(draw)
        self.assertEqual(expected, actual)

    def test_two_different_effects(self):
        draw = Draw(['R+0 MUDDLE', '+0 STUN'], 1)
        expected = Result(draw, Counter({'MUDDLE': 1, 'STUN': 1}))

        actual = self.testObject.make_result(draw)
        self.assertEqual(expected, actual)

    def test_rolling_modifier_in_reverse(self):
        draw = Draw(['+0 STUN', 'R+0 MUDDLE'], 1)
        expected = Result(draw, Counter({'MUDDLE': 1, 'STUN': 1}))

        actual = self.testObject.make_result(draw)
        self.assertEqual(expected, actual)

    def test_advantage_with_effects(self):
        draw = Draw(['+0 MUDDLE', '+0 STUN'], 2)
        expected = Result(draw, Counter({'MUDDLE': 1}))

        actual = self.testObject.make_result(draw)
        self.assertEqual(expected, actual)

    def test_advantage_with_two_terminating_effect_cards_selects_first_card(self):
        draw = Draw(['+0 STUN', '+0 MUDDLE'], 2)
        expected = Result(draw, Counter({'STUN': 1}))

        actual = self.testObject.make_result(draw)
        self.assertEqual(expected, actual)

    def test_advantage_makes_tied_number_and_effect_become_effect(self):
        draw_1 = Draw(['-2', '-2 MUDDLE'], 2)
        draw_2 = Draw(['+0', '+0 MUDDLE'], 2)
        draw_3 = Draw(['+2', '+2 MUDDLE'], 2)
        expected_1 = Result(draw_1, Counter({'MUDDLE': 1}))
        expected_2 = Result(draw_2, Counter({'MUDDLE': 1}))
        expected_3 = Result(draw_3, Counter({'MUDDLE': 1}))

        actual_1 = self.testObject.make_result(draw_1)
        actual_2 = self.testObject.make_result(draw_2)
        actual_3 = self.testObject.make_result(draw_3)
        self.assertEqual(expected_1, actual_1)
        self.assertEqual(expected_2, actual_2)
        self.assertEqual(expected_3, actual_3)

    def test_advantage_makes_tied_effect_and_number_become_effect(self):
        draw_1 = Draw(['-2 MUDDLE', '-2'], 2)
        draw_2 = Draw(['+0 MUDDLE', '+0'], 2)
        draw_3 = Draw(['+2 MUDDLE', '+2'], 2)
        expected_1 = Result(draw_1, Counter({'MUDDLE': 1}))
        expected_2 = Result(draw_2, Counter({'MUDDLE': 1}))
        expected_3 = Result(draw_3, Counter({'MUDDLE': 1}))

        actual_1 = self.testObject.make_result(draw_1)
        actual_2 = self.testObject.make_result(draw_2)
        actual_3 = self.testObject.make_result(draw_3)
        self.assertEqual(expected_1, actual_1)
        self.assertEqual(expected_2, actual_2)
        self.assertEqual(expected_3, actual_3)

    def test_greater_number_first_with_advantage_precedes_effect(self):
        draw_1 = Draw(['-1', '-2 MUDDLE'], 2)
        draw_2 = Draw(['+1', '+0 MUDDLE'], 2)
        draw_3 = Draw(['+3', '+2 MUDDLE'], 2)
        expected_1 = Result(draw_1, Counter())
        expected_2 = Result(draw_2, Counter())
        expected_3 = Result(draw_3, Counter())

        actual_1 = self.testObject.make_result(draw_1)
        actual_2 = self.testObject.make_result(draw_2)
        actual_3 = self.testObject.make_result(draw_3)
        self.assertEqual(expected_1, actual_1)
        self.assertEqual(expected_2, actual_2)
        self.assertEqual(expected_3, actual_3)

    def test_effect_with_advantage_precedes_greater_number_if_first(self):
        draw_1 = Draw(['-2 MUDDLE', '-1'], 2)
        draw_2 = Draw(['+0 MUDDLE', '+1'], 2)
        draw_3 = Draw(['+2 MUDDLE', '+3'], 2)
        expected_1 = Result(draw_1, Counter({'MUDDLE': 1}))
        expected_2 = Result(draw_2, Counter({'MUDDLE': 1}))
        expected_3 = Result(draw_3, Counter({'MUDDLE': 1}))

        actual_1 = self.testObject.make_result(draw_1)
        actual_2 = self.testObject.make_result(draw_2)
        actual_3 = self.testObject.make_result(draw_3)
        self.assertEqual(expected_1, actual_1)
        self.assertEqual(expected_2, actual_2)
        self.assertEqual(expected_3, actual_3)

    def test_effect_with_advantage_always_beats_null(self):
        draw_1 = Draw(['x0', '-4 MUDDLE'], 2)
        expected_1 = Result(draw_1, Counter({'MUDDLE': 1}))

        actual_1 = self.testObject.make_result(draw_1)
        self.assertEqual(expected_1, actual_1)

    def test_effect_first_with_advantage_precedes_critical(self):
        draw_1 = Draw(['-4 MUDDLE', 'x2'], 2)
        expected_1 = Result(draw_1, Counter({'MUDDLE': 1}))

        actual_1 = self.testObject.make_result(draw_1)
        self.assertEqual(expected_1, actual_1)

    def test_critical_with_advantage_is_ambiguous_with_effect(self):
        draw_1 = Draw(['x2', '-4 MUDDLE'], 2)
        expected_1 = Result(draw_1, Counter())

        actual_1 = self.testObject.make_result(draw_1)
        self.assertEqual(expected_1, actual_1)
