from collections import defaultdict
from fractions import Fraction

from perk_sheet_analyzer.aggregated_line import AggregatedLine


class DrawSchemeStatistics:
    def __init__(self) -> None:
        self.countable_effect_odds = defaultdict(Fraction)
        self.singular_effect_odds = defaultdict(Fraction)
        self.total_odds = Fraction()
        self.expected_damage = Fraction()
        self.attack_calculations = defaultdict(Fraction)

    def add_aggregated_line(self, aggregate: AggregatedLine, odds: Fraction) -> None:
        for effect, count in aggregate.countable_effects.items():
            self.countable_effect_odds[(effect, count)] += odds
            self.singular_effect_odds[effect] += odds  # Chance a countable occurred.
        for effect in aggregate.singular_effects:
            self.singular_effect_odds[effect] += odds
        self.total_odds += odds

        aggregate_key = tuple(aggregate.atk_calculation)
        self.attack_calculations[aggregate_key] += odds

    def calculate_expected_damage(self, atk) -> None:
        for atk_calc, odds in self.attack_calculations.items():
            damage_from_card_sequence = atk
            for card_bonus in atk_calc:
                damage_from_card_sequence = card_bonus.calculation(damage_from_card_sequence)
            self.expected_damage += damage_from_card_sequence * odds

    def make_copy(self):
        copy = DrawSchemeStatistics()
        copy.countable_effect_odds = self.countable_effect_odds.copy()
        copy.singular_effect_odds = self.singular_effect_odds.copy()
        copy.total_odds = self.total_odds
        copy.expected_damage = self.expected_damage
        copy.attack_calculations = self.attack_calculations.copy()
        return copy
