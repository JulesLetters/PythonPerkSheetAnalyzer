from typing import Callable, Tuple, Optional, NamedTuple


class AtkBonus(NamedTuple):
    display: str
    calculation: Callable[[int], int]


class Card:
    def __init__(self, bonus: AtkBonus, rolling: bool,
                 countable_effect: Optional[str] = None, singular_effect: Optional[str] = None):
        self.bonus = bonus
        self.rolling = rolling
        self.singular_effect = singular_effect
        self.countable_effect = countable_effect

        self.is_critical = bonus is _times_2_atk
        self.has_effect = singular_effect or countable_effect

        text = "R" if rolling else ""
        text += bonus.display
        if countable_effect:
            text += " " + countable_effect
        if singular_effect:
            text += " " + singular_effect

        self.text = text

    def adv_compare(self, other, atk: int):
        atk1 = self.bonus.calculation(atk)
        atk2 = other.bonus.calculation(atk)
        if not self.has_effect and not other.has_effect:
            if atk1 > atk2:
                return 1
            elif atk1 < atk2:
                return -1
        elif self.has_effect and not other.has_effect:
            if atk1 >= atk2:
                return 1
        elif not self.has_effect and other.has_effect:
            if atk1 <= atk2:
                return -1
        return 0

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


_times_2_atk = AtkBonus("2x", lambda x: x * 2)
_times_0_atk = AtkBonus("0x", lambda x: x * 0)
_minus_2_atk = AtkBonus("-2", lambda x: x - 2)
_minus_1_atk = AtkBonus("-1", lambda x: x - 1)
_plus_0_atk = AtkBonus("+0", lambda x: x)
_plus_1_atk = AtkBonus("+1", lambda x: x + 1)
_plus_2_atk = AtkBonus("+2", lambda x: x + 2)
_plus_3_atk = AtkBonus("+3", lambda x: x + 3)

times_2 = Card(_times_2_atk, False)
times_0 = Card(_times_0_atk, False)
minus_2 = Card(_minus_2_atk, False)
minus_1 = Card(_minus_1_atk, False)
plus_0 = Card(_plus_0_atk, False)
plus_1 = Card(_plus_1_atk, False)
plus_2 = Card(_plus_2_atk, False)
plus_3 = Card(_plus_3_atk, False)

rolling_plus_1 = Card(_plus_1_atk, True)
rolling_plus_0_muddle = Card(_plus_0_atk, True, singular_effect="Muddle")
rolling_plus_0_disarm = Card(_plus_0_atk, True, singular_effect="Disarm")
rolling_plus_0_stun = Card(_plus_0_atk, True, singular_effect="Stun")
rolling_plus_0_pierce_3 = Card(_plus_0_atk, True, countable_effect="Pierce_3")
rolling_plus_0_add_target = Card(_plus_0_atk, True, countable_effect="Add_Target")
rolling_plus_0_push_1 = Card(_plus_0_atk, True, countable_effect="Push_1")

plus_0_fire = Card(_plus_0_atk, False, singular_effect="Fire")
plus_0_ice = Card(_plus_0_atk, False, singular_effect="Ice")
plus_0_air = Card(_plus_0_atk, False, singular_effect="Air")
plus_0_earth = Card(_plus_0_atk, False, singular_effect="Earth")
plus_0_light = Card(_plus_0_atk, False, singular_effect="Light")
plus_0_dark = Card(_plus_0_atk, False, singular_effect="Dark")

plus_0_stun = Card(_plus_0_atk, False, singular_effect="Stun")
plus_0_add_target = Card(_plus_0_atk, False, countable_effect="Add_Target")
plus_0_refresh_item = Card(_plus_0_atk, False, countable_effect="Refresh_Item")
plus_1_push_1 = Card(_plus_1_atk, False, countable_effect="Push_1")
plus_1_wound = Card(_plus_1_atk, False, singular_effect="Wound")
plus_1_shield_1_self = Card(_plus_1_atk, False, countable_effect="Shield_1")
