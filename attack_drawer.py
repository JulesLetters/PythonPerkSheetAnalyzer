from typing import List


class Draws(List[str]):
    def __init__(self, cards: List[str], partitions: int):
        super().__init__(cards)
        self.partitions = partitions

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Draws):
            return super().__eq__(o) and self.partitions == o.partitions


class AttackDrawer:
    @staticmethod
    def form_all_draws(deck: List[str]) -> List[Draws]:
        result = []
        for card in deck:
            if card.startswith('R'):
                result.extend(AttackDrawer.rolling_modifier_draws(deck, card))
            else:
                result.append(Draws([card], 1))
        return result

    @staticmethod
    def rolling_modifier_draws(deck: List[str], card: str) -> List[Draws]:
        result = []
        remaining_deck = deck.copy()
        remaining_deck.remove(card)

        nested_results = AttackDrawer.form_all_draws(remaining_deck)
        for nested_draws in nested_results:
            result.append(Draws([card] + nested_draws, 1))
        return result

    @staticmethod
    def form_all_advantage_draws(deck: List[str]) -> List[Draws]:
        result = []
        for card in deck:
            remaining_cards = deck.copy()
            remaining_cards.remove(card)
            for next_card in remaining_cards:
                first_rolling = card.startswith('R')
                second_rolling = next_card.startswith('R')
                partitions = 1 if first_rolling or second_rolling else 2
                if first_rolling and second_rolling:
                    rolling_deck = remaining_cards.copy()
                    rolling_deck.remove(next_card)
                    rolling_draws = AttackDrawer.form_all_draws(rolling_deck)
                    for rolling_draw in rolling_draws:
                        result.append(Draws([card, next_card] + rolling_draw, 1))
                else:
                    result.append(Draws([card, next_card], partitions))
        return result
