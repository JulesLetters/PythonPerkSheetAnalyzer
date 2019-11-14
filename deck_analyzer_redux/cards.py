from typing import Callable, Tuple, Optional

Atk_Bonus = Tuple[str, Callable[[int], int]]


class Card:
    def __init__(self, bonus: Atk_Bonus, rolling: bool,
                 countable_effect: Optional[str]=None, singular_effect: Optional[str]=None):
        self.bonus = bonus
        self.rolling = rolling
        self.singular_effect = singular_effect
        self.countable_effect = countable_effect

        text = "R" if rolling else ""
        text += bonus[0]
        if countable_effect:
            text += " " + countable_effect
        if singular_effect:
            text += " " + singular_effect

        self.text = text

    def __str__(self) -> str:
        return self.text

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Card):
            return self.text == o.text
        return False

    def __repr__(self) -> str:
        return "Card({!r}, {!r}, {!r}, {!r})".format(self.bonus, self.rolling,
                                                     self.countable_effect, self.singular_effect)


_times_two_atk = ("2x", lambda x: x * 2)
_null_atk = ("0x", lambda x: x * 0)
_negative_two_atk = ("-2", lambda x: x - 2)
_negative_one_atk = ("-1", lambda x: x - 1)
_plus_zero_atk = ("+0", lambda x: x)
_plus_one_atk = ("+1", lambda x: x + 1)
_plus_two_atk = ("+2", lambda x: x + 2)

times_two = Card(_times_two_atk, False)
null_card = Card(_null_atk, False)
negative_two = Card(_negative_two_atk, False)
negative_one = Card(_negative_one_atk, False)
plus_zero = Card(_plus_zero_atk, False)
plus_one = Card(_plus_one_atk, False)
plus_two = Card(_plus_two_atk, False)
