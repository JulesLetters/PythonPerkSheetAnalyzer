from collections import Counter
from dataclasses import dataclass
from typing import List, Dict, Iterable

from perk_sheet_analyzer.cards import Card, AtkBonus


@dataclass
class AggregatedLine:
    atk_calculation: List[AtkBonus]
    countable_effects: Dict[str, int]
    singular_effects: Dict[str, bool]

    @classmethod
    def from_line(cls, line: Iterable[Card]):
        atk_calculation = []
        countable_effects = Counter()
        singular_effects = {}
        for card in line:
            # Another optimization is to intelligently combine the functions.
            atk_calculation.append(card.bonus)
            if card.countable_effect:
                countable_effects[card.countable_effect] += 1
            if card.singular_effect:
                singular_effects[card.singular_effect] = True

        return cls(atk_calculation, countable_effects, singular_effects)

    @classmethod
    def from_card(cls, card: Card):
        return cls.from_line([card])

    def add_card(self, card: Card):
        atk_calculation = self.atk_calculation + [card.bonus]

        if card.countable_effect:
            countable_effects = self.countable_effects.copy()
            countable_effects[card.countable_effect] += 1
        else:
            countable_effects = self.countable_effects

        if card.singular_effect:
            singular_effects = self.singular_effects.copy()
            singular_effects[card.singular_effect] = True
        else:
            singular_effects = self.singular_effects

        return AggregatedLine(atk_calculation, countable_effects, singular_effects)
