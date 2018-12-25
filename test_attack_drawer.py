from unittest import TestCase

from multiset import Multiset, FrozenMultiset

from attack_drawer import AttackDrawer, Draw


class TestAttackDrawer(TestCase):

    def setUp(self):
        self.testObject = AttackDrawer()

    test_object = AttackDrawer()

    def test_single_draw(self):
        deck = FrozenMultiset(['+0', '+1', '+2'])
        expected = Multiset([Draw(x, 1) for x in
                             [['+0'], ['+1'], ['+2']]
                             ])

        actual = self.test_object.form_all_draws(deck)
        self.assertEqual(expected, actual)

    def test_single_draw_with_rolling_modifier(self):
        deck = FrozenMultiset(['+0', 'R+1', '+2'])
        expected = Multiset([Draw(x, 1) for x in
                             [['+0'], ['R+1', '+0'], ['R+1', '+2'], ['+2']]
                             ])

        actual = self.test_object.form_all_draws(deck)
        self.assertEqual(expected, actual)

    def test_single_draw_with_two_rolling_modifies(self):
        deck = FrozenMultiset(['+0', 'R+1', 'R+0', '+2'])
        expected = Multiset([Draw(x, 1) for x in
                             [['+0'],
                              ['R+1', '+0'], ['R+1', 'R+0', '+0'], ['R+1', 'R+0', '+2'], ['R+1', '+2'],
                              ['R+0', '+0'], ['R+0', 'R+1', '+0'], ['R+0', 'R+1', '+2'], ['R+0', '+2'],
                              ['+2']]
                             ])

        actual = self.test_object.form_all_draws(deck)
        self.assertEqual(expected, actual)

    def test_draw_with_advantage(self):
        deck = FrozenMultiset(['+0', '+1', '+2'])
        expected = Multiset([Draw(['+0', '+1'], 2), Draw(['+0', '+2'], 2),
                             Draw(['+1', '+0'], 2), Draw(['+1', '+2'], 2),
                             Draw(['+2', '+0'], 2), Draw(['+2', '+1'], 2)
                             ])

        actual = self.test_object.form_all_advantage_draws(deck)
        self.assertEqual(expected, actual)

    def test_draw_with_advantage_and_rolling_modifier(self):
        deck = FrozenMultiset(['+0', '+1', 'R+1', '+2'])

        expected = Multiset([Draw(['+0', '+1'], 2), Draw(['+0', 'R+1'], 1), Draw(['+0', '+2'], 2),
                             Draw(['+1', '+0'], 2), Draw(['+1', 'R+1'], 1), Draw(['+1', '+2'], 2),
                             Draw(['R+1', '+0'], 1), Draw(['R+1', '+1'], 1), Draw(['R+1', '+2'], 1),
                             Draw(['+2', '+0'], 2), Draw(['+2', '+1'], 2), Draw(['+2', 'R+1'], 1)
                             ])

        actual = self.test_object.form_all_advantage_draws(deck)
        self.assertEqual(expected, actual)

    def test_draw_with_advantage_and_two_rolling_modifiers(self):
        deck = FrozenMultiset(['+0', 'R+1', 'R+2', '+2'])

        expected = Multiset([Draw(['+0', 'R+1'], 1), Draw(['+0', 'R+2'], 1), Draw(['+0', '+2'], 2),
                             Draw(['R+1', '+0'], 1),
                             Draw(['R+1', 'R+2', '+0'], 1), Draw(['R+1', 'R+2', '+2'], 1),
                             Draw(['R+1', '+2'], 1),
                             Draw(['R+2', '+0'], 1),
                             Draw(['R+2', 'R+1', '+0'], 1), Draw(['R+2', 'R+1', '+2'], 1),
                             Draw(['R+2', '+2'], 1),
                             Draw(['+2', '+0'], 2), Draw(['+2', 'R+1'], 1), Draw(['+2', 'R+2'], 1)
                             ])

        actual = self.test_object.form_all_advantage_draws(deck)
        self.assertEqual(expected, actual)

    def test_draw_with_advantage_and_three_rolling_modifiers(self):
        deck = FrozenMultiset(['+0', 'R+1', 'R+2', 'R+1', '+2'])

        expected = Multiset(
            [Draw(['+0', 'R+1'], 1), Draw(['+0', 'R+2'], 1), Draw(['+0', 'R+1'], 1), Draw(['+0', '+2'], 2),
             Draw(['R+1', '+0'], 1),
             Draw(['R+1', 'R+2', '+0'], 1),
             Draw(['R+1', 'R+2', 'R+1', '+0'], 1), Draw(['R+1', 'R+2', 'R+1', '+2'], 1),
             Draw(['R+1', 'R+2', '+2'], 1),
             Draw(['R+1', 'R+1', '+0'], 1),
             Draw(['R+1', 'R+1', 'R+2', '+0'], 1), Draw(['R+1', 'R+1', 'R+2', '+2'], 1),
             Draw(['R+1', 'R+1', '+2'], 1),
             Draw(['R+1', '+2'], 1),
             Draw(['R+2', '+0'], 1),
             Draw(['R+2', 'R+1', '+0'], 1),
             Draw(['R+2', 'R+1', 'R+1', '+0'], 1), Draw(['R+2', 'R+1', 'R+1', '+2'], 1),
             Draw(['R+2', 'R+1', '+2'], 1),
             Draw(['R+2', 'R+1', '+0'], 1),
             Draw(['R+2', 'R+1', 'R+1', '+0'], 1), Draw(['R+2', 'R+1', 'R+1', '+2'], 1),
             Draw(['R+2', 'R+1', '+2'], 1),
             Draw(['R+2', '+2'], 1),
             Draw(['R+1', '+0'], 1),
             Draw(['R+1', 'R+2', '+0'], 1),
             Draw(['R+1', 'R+2', 'R+1', '+0'], 1), Draw(['R+1', 'R+2', 'R+1', '+2'], 1),
             Draw(['R+1', 'R+2', '+2'], 1),
             Draw(['R+1', 'R+1', '+0'], 1),
             Draw(['R+1', 'R+1', 'R+2', '+0'], 1), Draw(['R+1', 'R+1', 'R+2', '+2'], 1),
             Draw(['R+1', 'R+1', '+2'], 1),
             Draw(['R+1', '+2'], 1),
             Draw(['+2', '+0'], 2), Draw(['+2', 'R+1'], 1), Draw(['+2', 'R+2'], 1), Draw(['+2', 'R+1'], 1)
             ])

        actual = self.test_object.form_all_advantage_draws(deck)
        self.assertEqual(expected, actual)
