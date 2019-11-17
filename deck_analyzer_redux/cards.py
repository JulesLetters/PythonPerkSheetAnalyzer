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

    def __lt__(self, other) -> bool:
        return self.text < other.text

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Card):
            return self.text == o.text
        return False

    def __hash__(self) -> int:
        return hash(self.text)

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

rolling_plus_one = Card(_plus_one_atk, True)
rolling_plus_zero_muddle = Card(_plus_zero_atk, True, singular_effect="Muddle")
rolling_plus_zero_pierce_3 = Card(_plus_zero_atk, True, countable_effect="Pierce_3")
rolling_plus_zero_stun = Card(_plus_zero_atk, True, singular_effect="Stun")
rolling_plus_zero_add_target = Card(_plus_zero_atk, True, countable_effect="Add_Target")
rolling_plus_one_refresh_item = Card(_plus_one_atk, True, countable_effect="Refresh_Item")

plus_zero_fire = Card(_plus_zero_atk, False, singular_effect="Fire")
plus_zero_ice = Card(_plus_zero_atk, False, singular_effect="Ice")
plus_zero_air = Card(_plus_zero_atk, False, singular_effect="Air")
plus_zero_earth = Card(_plus_zero_atk, False, singular_effect="Earth")

plus_one_push_one = Card(_plus_one_atk, False, countable_effect="Push_1")
plus_one_wound = Card(_plus_one_atk, False, singular_effect="Wound")
plus_zero_stun = Card(_plus_zero_atk, False, singular_effect="Stun")
plus_zero_add_target = Card(_plus_zero_atk, False, countable_effect="Add_Target")
