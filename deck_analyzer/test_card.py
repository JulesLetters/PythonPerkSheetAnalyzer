from unittest import TestCase

from deck_analyzer.cards import minus_2, minus_1, plus_0, plus_1, plus_2, _minus_2_atk, \
    Card, _plus_2_atk, _minus_1_atk, _plus_0_atk, _plus_1_atk, times_2, times_0

minus_2_s_x = Card(_minus_2_atk, False, singular_effect="X")
minus_1_s_x = Card(_minus_1_atk, False, singular_effect="X")
plus_0_s_x = Card(_plus_0_atk, False, singular_effect="X")
plus_1_s_x = Card(_plus_1_atk, False, singular_effect="X")
plus_2_s_x = Card(_plus_2_atk, False, singular_effect="X")

minus_2_c_x = Card(_minus_2_atk, False, countable_effect="X")
minus_1_c_x = Card(_minus_1_atk, False, countable_effect="X")
plus_0_c_x = Card(_plus_0_atk, False, countable_effect="X")
plus_1_c_x = Card(_plus_1_atk, False, countable_effect="X")
plus_2_c_x = Card(_plus_2_atk, False, countable_effect="X")

atk = 3


class TestCard(TestCase):
    def test_adv_compare_returns_negative_for_non_effect_cards_when_first_less_than_second(self):
        self.assertEqual(-1, minus_1.adv_compare(plus_0, atk))
        self.assertEqual(-1, plus_0.adv_compare(plus_1, atk))
        self.assertEqual(-1, plus_1.adv_compare(plus_2, atk))
        self.assertEqual(-1, minus_2.adv_compare(plus_2, atk))

    def test_adv_compare_returns_zero_for_non_effect_cards_when_first_equal_to_second(self):
        self.assertEqual(0, minus_1.adv_compare(minus_1, atk))
        self.assertEqual(0, plus_0.adv_compare(plus_0, atk))
        self.assertEqual(0, plus_1.adv_compare(plus_1, atk))
        self.assertEqual(0, minus_2.adv_compare(minus_2, atk))

    def test_adv_compare_returns_positive_for_non_effect_cards_when_first_greater_than_second(self):
        self.assertEqual(1, plus_0.adv_compare(minus_1, atk))
        self.assertEqual(1, plus_1.adv_compare(plus_0, atk))
        self.assertEqual(1, plus_2.adv_compare(plus_1, atk))
        self.assertEqual(1, plus_2.adv_compare(minus_2, atk))

    def test_adv_compare_returns_zero_for_first_card_with_effect_when_first_less_than_second(self):
        self.assertEqual(0, minus_2_s_x.adv_compare(plus_0, atk))
        self.assertEqual(0, minus_2_c_x.adv_compare(plus_0, atk))
        self.assertEqual(0, minus_1_s_x.adv_compare(plus_0, atk))
        self.assertEqual(0, minus_1_c_x.adv_compare(plus_0, atk))
        self.assertEqual(0, plus_0_s_x.adv_compare(plus_2, atk))
        self.assertEqual(0, plus_0_c_x.adv_compare(plus_2, atk))
        self.assertEqual(0, plus_1_s_x.adv_compare(plus_2, atk))
        self.assertEqual(0, plus_1_c_x.adv_compare(plus_2, atk))

    def test_adv_compare_returns_positive_for_first_card_with_effect_when_first_equal_to_second(self):
        self.assertEqual(1, minus_2_s_x.adv_compare(minus_2, atk))
        self.assertEqual(1, minus_2_c_x.adv_compare(minus_2, atk))
        self.assertEqual(1, plus_0_s_x.adv_compare(plus_0, atk))
        self.assertEqual(1, plus_0_c_x.adv_compare(plus_0, atk))
        self.assertEqual(1, plus_2_s_x.adv_compare(plus_2, atk))
        self.assertEqual(1, plus_2_c_x.adv_compare(plus_2, atk))

    def test_adv_compare_returns_positive_for_first_card_with_effect_when_first_greater_than_second(self):
        self.assertEqual(1, minus_1_s_x.adv_compare(minus_2, atk))
        self.assertEqual(1, minus_1_c_x.adv_compare(minus_2, atk))
        self.assertEqual(1, plus_1_s_x.adv_compare(plus_0, atk))
        self.assertEqual(1, plus_1_c_x.adv_compare(plus_0, atk))
        self.assertEqual(1, plus_2_s_x.adv_compare(plus_1, atk))
        self.assertEqual(1, plus_2_c_x.adv_compare(plus_1, atk))

    def test_adv_compare_returns_zero_for_second_card_with_effect_when_first_less_than_second(self):
        self.assertEqual(-1, minus_2.adv_compare(plus_0_s_x, atk))
        self.assertEqual(-1, minus_2.adv_compare(plus_0_c_x, atk))
        self.assertEqual(-1, minus_1.adv_compare(plus_0_s_x, atk))
        self.assertEqual(-1, minus_1.adv_compare(plus_0_c_x, atk))
        self.assertEqual(-1, plus_0.adv_compare(plus_2_s_x, atk))
        self.assertEqual(-1, plus_0.adv_compare(plus_2_c_x, atk))
        self.assertEqual(-1, plus_1.adv_compare(plus_2_s_x, atk))
        self.assertEqual(-1, plus_1.adv_compare(plus_2_c_x, atk))

    def test_adv_compare_returns_negative_for_second_card_with_effect_when_first_equal_to_second(self):
        self.assertEqual(-1, minus_2.adv_compare(minus_2_s_x, atk))
        self.assertEqual(-1, minus_2.adv_compare(minus_2_c_x, atk))
        self.assertEqual(-1, plus_0.adv_compare(plus_0_s_x, atk))
        self.assertEqual(-1, plus_0.adv_compare(plus_0_c_x, atk))
        self.assertEqual(-1, plus_2.adv_compare(plus_2_s_x, atk))
        self.assertEqual(-1, plus_2.adv_compare(plus_2_c_x, atk))

    def test_adv_compare_returns_zero_for_second_card_with_effect_when_first_greater_than_second(self):
        self.assertEqual(0, plus_0.adv_compare(minus_1_s_x, atk))
        self.assertEqual(0, plus_0.adv_compare(minus_1_c_x, atk))
        self.assertEqual(0, plus_2.adv_compare(plus_1_s_x, atk))
        self.assertEqual(0, plus_2.adv_compare(plus_1_c_x, atk))
        self.assertEqual(0, plus_2.adv_compare(minus_2_s_x, atk))
        self.assertEqual(0, plus_2.adv_compare(minus_2_c_x, atk))

    def test_adv_compare_returns_zero_for_both_cards_with_effect_when_first_less_than_second(self):
        self.assertEqual(0, plus_0_s_x.adv_compare(minus_2_s_x, atk))
        self.assertEqual(0, plus_0_c_x.adv_compare(minus_2_c_x, atk))
        self.assertEqual(0, plus_0_s_x.adv_compare(minus_1_s_x, atk))
        self.assertEqual(0, plus_0_c_x.adv_compare(minus_1_c_x, atk))
        self.assertEqual(0, plus_2_s_x.adv_compare(plus_0_s_x, atk))
        self.assertEqual(0, plus_2_c_x.adv_compare(plus_0_c_x, atk))
        self.assertEqual(0, plus_2_s_x.adv_compare(plus_1_s_x, atk))
        self.assertEqual(0, plus_2_c_x.adv_compare(plus_1_c_x, atk))

    def test_adv_compare_returns_zero_for_both_cards_with_effect_when_first_equal_to_second(self):
        self.assertEqual(0, minus_2_s_x.adv_compare(minus_2_s_x, atk))
        self.assertEqual(0, minus_2_c_x.adv_compare(minus_2_c_x, atk))
        self.assertEqual(0, plus_0_s_x.adv_compare(plus_0_s_x, atk))
        self.assertEqual(0, plus_0_c_x.adv_compare(plus_0_c_x, atk))
        self.assertEqual(0, plus_2_s_x.adv_compare(plus_2_s_x, atk))
        self.assertEqual(0, plus_2_c_x.adv_compare(plus_2_c_x, atk))

    def test_adv_compare_returns_zero_for_both_cards_with_effect_when_first_greater_than_second(self):
        self.assertEqual(0, minus_2_s_x.adv_compare(minus_1_s_x, atk))
        self.assertEqual(0, minus_2_c_x.adv_compare(minus_1_c_x, atk))
        self.assertEqual(0, plus_0_s_x.adv_compare(plus_1_s_x, atk))
        self.assertEqual(0, plus_0_c_x.adv_compare(plus_1_c_x, atk))
        self.assertEqual(0, plus_1_s_x.adv_compare(plus_2_s_x, atk))
        self.assertEqual(0, plus_1_c_x.adv_compare(plus_2_c_x, atk))

    def test_adv_compare_returns_zero_for_times_2_when_both_results_are_the_same(self):
        self.assertEqual(0, plus_2.adv_compare(times_2, 2))
        self.assertEqual(0, plus_1.adv_compare(times_2, 1))
        self.assertEqual(0, plus_0.adv_compare(times_2, 0))

    def test_is_critical(self):
        self.assertEqual(True, times_2.is_critical)
        self.assertEqual(False, plus_1.is_critical)
        self.assertEqual(False, plus_0.is_critical)
        self.assertEqual(False, times_0.is_critical)
