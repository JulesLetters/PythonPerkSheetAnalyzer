from typing import Iterable

from multiset import Multiset


class Draws:
    def __init__(self, cards: Iterable[str], partitions: int):
        self.cards = tuple(cards)
        self.partitions = partitions

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Draws):
            return super().__eq__(o) and self.partitions == o.partitions

    def __hash__(self) -> int:
        return hash((self.cards, self.partitions))

    def __repr__(self) -> str:
        return "Draws({!r}, {!r})".format(self.cards, self.partitions)


class AttackDrawer:
    @staticmethod
    def form_all_draws(deck: Multiset) -> Multiset:
        result = []
        for card in deck:
            if card.startswith('R'):
                result.extend(AttackDrawer.rolling_modifier_draws(deck, card))
            else:
                result.append(Draws((card,), 1))
        return Multiset(result)

    @staticmethod
    def rolling_modifier_draws(deck: Multiset, card: str) -> Multiset:
        result = []
        remaining_deck = AttackDrawer.subtract_from_deck(deck, card)

        nested_results = AttackDrawer.form_all_draws(remaining_deck)
        for nested_draws in nested_results:
            result.append(Draws((card,) + nested_draws.cards, 1))
        return Multiset(result)

    @staticmethod
    def form_all_advantage_draws(deck: Multiset) -> Multiset:
        result = []
        for card in deck:
            remaining_cards = AttackDrawer.subtract_from_deck(deck, card)
            for next_card in remaining_cards:
                first_rolling = card.startswith('R')
                second_rolling = next_card.startswith('R')
                partitions = 1 if first_rolling or second_rolling else 2
                if first_rolling and second_rolling:
                    rolling_deck = AttackDrawer.subtract_from_deck(remaining_cards, next_card)
                    rolling_draws = AttackDrawer.form_all_draws(rolling_deck)
                    for rolling_draw in rolling_draws:
                        result.append(Draws((card, next_card) + rolling_draw.cards, 1))
                else:
                    result.append(Draws((card, next_card), partitions))
        return Multiset(result)

    @classmethod
    def subtract_from_deck(cls, deck: Multiset, card: str):
        result = deck.copy()
        result.remove(card, 1)
        return result
