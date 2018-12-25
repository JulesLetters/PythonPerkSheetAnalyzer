from collections import Counter

from attack_drawer import Draw


class Result:
    def __init__(self, draws: Draw, effects):
        self.draws = draws
        self.effects = effects

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Result):
            return self.draws == o.draws and self.effects == o.effects
        return False

    def __repr__(self) -> str:
        return "Result({!r}, {!r})".format(self.draws, self.effects)


class DrawParser:
    @classmethod
    def make_result(cls, draws: Draw) -> Result:
        effects = Counter()
        if draws.partitions == 2:
            real_draws = cls.extract_better_advantaged_draw(draws)
        else:
            real_draws = draws

        for card in real_draws.cards:
            if DrawParser.has_effect(card):
                effects[card.split()[1]] += 1
        return Result(draws, effects)

    @classmethod
    def extract_better_advantaged_draw(cls, draws):
        card_1 = draws.cards[0]
        card_2 = draws.cards[1]
        card_1_has_effect = cls.has_effect(card_1)
        card_2_has_effect = cls.has_effect(card_2)
        card_1_number = cls.extract_number(card_1)
        card_2_number = cls.extract_number(card_2)
        if card_2_has_effect and not card_1_has_effect and card_2_number >= card_1_number:
            real_draws = Draw((card_2,), 1)
        else:
            real_draws = Draw((card_1,), 1)
        return real_draws

    @classmethod
    def has_effect(cls, card: str) -> bool:
        return len(card.split()) is 2

    @classmethod
    def extract_number(cls, card: str) -> int:
        if card == 'x0':
            return -10
        if card == 'x2':
            return 10
        return int(card.split()[0])
