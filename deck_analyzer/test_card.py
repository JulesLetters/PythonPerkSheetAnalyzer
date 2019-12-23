from unittest import TestCase

from deck_analyzer.cards import negative_two, negative_one, plus_zero, plus_one, plus_two, _negative_two_atk, \
    Card, _plus_two_atk, _negative_one_atk, _plus_zero_atk, _plus_one_atk

negative_two_x = Card(_negative_two_atk, False, singular_effect="X")
negative_one_x = Card(_negative_one_atk, False, singular_effect="X")
plus_zero_x = Card(_plus_zero_atk, False, singular_effect="X")
plus_one_x = Card(_plus_one_atk, False, singular_effect="X")
plus_two_x = Card(_plus_two_atk, False, singular_effect="X")

atk = 3


class TestCard(TestCase):
    def test_adv_compare_returns_negative_for_non_effect_cards_when_first_less_than_second(self):
        self.assertEqual(-1, negative_one.adv_compare(plus_zero, atk))
        self.assertEqual(-1, plus_zero.adv_compare(plus_one, atk))
        self.assertEqual(-1, plus_one.adv_compare(plus_two, atk))
        self.assertEqual(-1, negative_two.adv_compare(plus_two, atk))

    def test_adv_compare_returns_zero_for_non_effect_cards_when_first_equal_to_second(self):
        self.assertEqual(0, negative_one.adv_compare(negative_one, atk))
        self.assertEqual(0, plus_zero.adv_compare(plus_zero, atk))
        self.assertEqual(0, plus_one.adv_compare(plus_one, atk))
        self.assertEqual(0, negative_two.adv_compare(negative_two, atk))

    def test_adv_compare_returns_positive_for_non_effect_cards_when_first_greater_than_second(self):
        self.assertEqual(1, plus_zero.adv_compare(negative_one, atk))
        self.assertEqual(1, plus_one.adv_compare(plus_zero, atk))
        self.assertEqual(1, plus_two.adv_compare(plus_one, atk))
        self.assertEqual(1, plus_two.adv_compare(negative_two, atk))

    def test_adv_compare_returns_zero_for_first_card_with_effect_when_first_less_than_second(self):
        self.assertEqual(0, negative_two_x.adv_compare(plus_zero, atk))
        self.assertEqual(0, negative_one_x.adv_compare(plus_zero, atk))
        self.assertEqual(0, plus_zero_x.adv_compare(plus_two, atk))
        self.assertEqual(0, plus_one_x.adv_compare(plus_two, atk))

    def test_adv_compare_returns_positive_for_first_card_with_effect_when_first_equal_to_second(self):
        self.assertEqual(1, negative_two_x.adv_compare(negative_two, atk))
        self.assertEqual(1, plus_zero_x.adv_compare(plus_zero, atk))
        self.assertEqual(1, plus_two_x.adv_compare(plus_two, atk))

    def test_adv_compare_returns_positive_for_first_card_with_effect_when_first_greater_than_second(self):
        self.assertEqual(1, negative_one_x.adv_compare(negative_two, atk))
        self.assertEqual(1, plus_one_x.adv_compare(plus_zero, atk))
        self.assertEqual(1, plus_two_x.adv_compare(plus_one, atk))

    def test_adv_compare_returns_zero_for_second_card_with_effect_when_first_less_than_second(self):
        self.assertEqual(-1, negative_two.adv_compare(plus_zero_x, atk))
        self.assertEqual(-1, negative_one.adv_compare(plus_zero_x, atk))
        self.assertEqual(-1, plus_zero.adv_compare(plus_two_x, atk))
        self.assertEqual(-1, plus_one.adv_compare(plus_two_x, atk))

    def test_adv_compare_returns_negative_for_second_card_with_effect_when_first_equal_to_second(self):
        self.assertEqual(-1, negative_two.adv_compare(negative_two_x, atk))
        self.assertEqual(-1, plus_zero.adv_compare(plus_zero_x, atk))
        self.assertEqual(-1, plus_two.adv_compare(plus_two_x, atk))

    def test_adv_compare_returns_zero_for_second_card_with_effect_when_first_greater_than_second(self):
        self.assertEqual(0, plus_zero.adv_compare(negative_one_x, atk))
        self.assertEqual(0, plus_two.adv_compare(plus_one_x, atk))
        self.assertEqual(0, plus_two.adv_compare(negative_two_x, atk))

    def test_adv_compare_returns_zero_for_both_cards_with_effect_when_first_less_than_second(self):
        self.assertEqual(0, plus_zero_x.adv_compare(negative_two_x, atk))
        self.assertEqual(0, plus_zero_x.adv_compare(negative_one_x, atk))
        self.assertEqual(0, plus_two_x.adv_compare(plus_zero_x, atk))
        self.assertEqual(0, plus_two_x.adv_compare(plus_one_x, atk))

    def test_adv_compare_returns_zero_for_both_cards_with_effect_when_first_equal_to_second(self):
        self.assertEqual(0, negative_two_x.adv_compare(negative_two_x, atk))
        self.assertEqual(0, plus_zero_x.adv_compare(plus_zero_x, atk))
        self.assertEqual(0, plus_two_x.adv_compare(plus_two_x, atk))

    def test_adv_compare_returns_zero_for_both_cards_with_effect_when_first_greater_than_second(self):
        self.assertEqual(0, negative_two_x.adv_compare(negative_one_x, atk))
        self.assertEqual(0, plus_zero_x.adv_compare(plus_one_x, atk))
        self.assertEqual(0, plus_one_x.adv_compare(plus_two_x, atk))
