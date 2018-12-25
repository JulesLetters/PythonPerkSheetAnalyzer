from typing import Iterable

from multiset import Multiset, FrozenMultiset


class Draw:
    def __init__(self, cards: Iterable[str], partitions: int):
        self.cards = tuple(cards)
        self.partitions = partitions

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Draw):
            return super().__eq__(o) and self.partitions == o.partitions

    def __hash__(self) -> int:
        return hash((self.cards, self.partitions))

    def __repr__(self) -> str:
        return "Draw({!r}, {!r})".format(self.cards, self.partitions)


class AttackDrawer:
    @staticmethod
    def form_all_draws(deck: FrozenMultiset) -> Multiset:
        result = FrozenMultiset()
        for card in deck:
            if card.startswith('R'):
                result = result.combine(AttackDrawer.rolling_modifier_draws(deck, card))
            else:
                result = result.combine([Draw((card,), 1)])
        return result

    @staticmethod
    def rolling_modifier_draws(deck: FrozenMultiset, card: str) -> Multiset:
        result = Multiset()
        remaining_deck = deck.difference([card])

        nested_results = AttackDrawer.form_all_draws(remaining_deck)
        for nested_draw in nested_results:
            result.add(Draw((card,) + nested_draw.cards, 1))
        return result

    @staticmethod
    def form_all_advantage_draws(deck: FrozenMultiset) -> Multiset:
        result = Multiset()
        for card in deck:
            remaining_cards = deck.difference([card])
            for next_card in remaining_cards:
                first_rolling = card.startswith('R')
                second_rolling = next_card.startswith('R')
                partitions = 1 if first_rolling or second_rolling else 2
                if first_rolling and second_rolling:
                    rolling_deck = remaining_cards.difference([next_card])
                    rolling_draws = AttackDrawer.form_all_draws(rolling_deck)
                    for rolling_draw in rolling_draws:
                        result.add(Draw((card, next_card) + rolling_draw.cards, 1))
                else:
                    result.add(Draw((card, next_card), partitions))
        return result
