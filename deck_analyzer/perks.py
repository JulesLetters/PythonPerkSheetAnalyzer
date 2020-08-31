from typing import List

import deck_analyzer.cards as cards

Deck = List[cards.Card]


def none(_: Deck) -> None:
    pass


def remo_two_minus_1(deck: Deck) -> None:
    deck.remove(cards.minus_1)
    deck.remove(cards.minus_1)


def remo_four_plus_0(deck: Deck) -> None:
    deck.remove(cards.plus_0)
    deck.remove(cards.plus_0)
    deck.remove(cards.plus_0)
    deck.remove(cards.plus_0)


def repl_one_plus_0_w_one_plus_2(deck: Deck) -> None:
    deck.remove(cards.plus_0)
    deck.append(cards.plus_2)


def repl_one_minus_1_w_one_plus_1(deck: Deck) -> None:
    deck.remove(cards.minus_1)
    deck.append(cards.plus_1)


def add_two_rolling_plus_1(deck: Deck) -> None:
    deck.append(cards.rolling_plus_1)
    deck.append(cards.rolling_plus_1)


def add_three_rolling_plus_0_muddle(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_muddle)
    deck.append(cards.rolling_plus_0_muddle)
    deck.append(cards.rolling_plus_0_muddle)


def add_three_rolling_plus_0_push_1(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_push_1)
    deck.append(cards.rolling_plus_0_push_1)
    deck.append(cards.rolling_plus_0_push_1)


def add_two_rolling_plus_0_pierce_3(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_pierce_3)
    deck.append(cards.rolling_plus_0_pierce_3)


def add_one_rolling_plus_0_muddle(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_muddle)


def add_one_rolling_plus_0_stun(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_stun)


def add_one_rolling_plus_0_disarm(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_disarm)


def add_one_rolling_plus_0_add_target(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_add_target)


def add_one_plus_0_refresh_item_self(deck: Deck) -> None:
    deck.append(cards.plus_0_refresh_item_self)


def add_two_plus_1(deck: Deck) -> None:
    deck.append(cards.plus_1)
    deck.append(cards.plus_1)


def add_one_plus_3(deck: Deck) -> None:
    deck.append(cards.plus_3)


def add_three_plus_0_fire(deck: Deck) -> None:
    deck.append(cards.plus_0_fire)
    deck.append(cards.plus_0_fire)
    deck.append(cards.plus_0_fire)


def add_three_plus_0_ice(deck: Deck) -> None:
    deck.append(cards.plus_0_ice)
    deck.append(cards.plus_0_ice)
    deck.append(cards.plus_0_ice)


def add_three_plus_0_air(deck: Deck) -> None:
    deck.append(cards.plus_0_air)
    deck.append(cards.plus_0_air)
    deck.append(cards.plus_0_air)


def add_three_plus_0_earth(deck: Deck) -> None:
    deck.append(cards.plus_0_earth)
    deck.append(cards.plus_0_earth)
    deck.append(cards.plus_0_earth)


def repl_two_plus_0_w_one_plus_0_fire_and_one_plus_0_earth(deck: Deck) -> None:
    deck.remove(cards.plus_0)
    deck.remove(cards.plus_0)
    deck.append(cards.plus_0_fire)
    deck.append(cards.plus_0_earth)


def repl_two_plus_0_w_one_plus_0_ice_and_one_plus_0_air(deck: Deck) -> None:
    deck.remove(cards.plus_0)
    deck.remove(cards.plus_0)
    deck.append(cards.plus_0_ice)
    deck.append(cards.plus_0_air)


def add_two_plus_1_push_1(deck: Deck) -> None:
    deck.append(cards.plus_1_push_1)
    deck.append(cards.plus_1_push_1)


def add_one_plus_1_wound(deck: Deck) -> None:
    deck.append(cards.plus_1_wound)


def add_one_plus_0_stun(deck: Deck) -> None:
    deck.append(cards.plus_0_stun)


def add_one_plus_0_add_target(deck: Deck) -> None:
    deck.append(cards.plus_0_add_target)


def add_one_plus_1_shield_1_self(deck: Deck) -> None:
    deck.append(cards.plus_1_shield_1_self)


# def ignore_negative_item(deck: Deck) ->None:
# IGNORE NEGATIVE ITEM EFFECTS HERE


def ignore_negative_item_and_add_one_plus_1(deck: Deck) -> None:
    deck.append(cards.plus_1)
    # IGNORE NEGATIVE ITEM EFFECTS HERE


# def ignore_negative_scenario(deck: Deck) ->None:
# IGNORE NEGATIVE SCENARIO EFFECTS HERE


def add_one_minus_2_and_two_plus_2(deck: Deck) -> None:
    deck.append(cards.minus_2)
    deck.append(cards.plus_2)
    deck.append(cards.plus_2)


def add_one_plus_1_immobilize(deck: Deck) -> None:
    deck.append(cards.plus_1_immobilize)


def add_one_plus_2_muddle(deck: Deck) -> None:
    deck.append(cards.plus_2_muddle)


def add_two_rolling_plus_0_push_2(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_push_2)
    deck.append(cards.rolling_plus_0_push_2)


def add_two_rolling_plus_0_earth(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_earth)
    deck.append(cards.rolling_plus_0_earth)


def add_two_rolling_plus_0_air(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_air)
    deck.append(cards.rolling_plus_0_air)


def add_one_rolling_plus_0_earth_and_one_rolling_plus_0_air(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_air)
    deck.append(cards.rolling_plus_0_earth)


def add_one_rolling_plus_0_light_and_one_rolling_plus_0_dark(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_light)
    deck.append(cards.rolling_plus_0_dark)


def add_one_plus_1_curse(deck: Deck) -> None:
    deck.append(cards.plus_1_curse)


def add_one_plus_2_fire(deck: Deck) -> None:
    deck.append(cards.plus_2_fire)


def add_one_plus_2_ice(deck: Deck) -> None:
    deck.append(cards.plus_2_ice)


def repl_two_plus_1_w_two_plus_2(deck: Deck) -> None:
    deck.remove(cards.plus_1)
    deck.remove(cards.plus_1)
    deck.append(cards.plus_2)
    deck.append(cards.plus_2)


def repl_one_minus_2_w_one_plus_0(deck: Deck) -> None:
    deck.remove(cards.minus_2)
    deck.append(cards.plus_0)


def add_three_rolling_plus_0_pull_1(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_pull_1)
    deck.append(cards.rolling_plus_0_pull_1)
    deck.append(cards.rolling_plus_0_pull_1)


def add_two_rolling_plus_0_immobilize(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_immobilize)
    deck.append(cards.rolling_plus_0_immobilize)


def add_one_rolling_plus_0_disarm_and_one_rolling_plus_0_muddle(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_disarm)
    deck.append(cards.rolling_plus_0_muddle)


def add_two_rolling_plus_0_poison(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_poison)
    deck.append(cards.rolling_plus_0_poison)


def add_two_rolling_plus_0_muddle(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_muddle)
    deck.append(cards.rolling_plus_0_muddle)


def add_one_rolling_plus_0_invisible_self(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_invisible_self)


def add_two_rolling_plus_0_fire(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_fire)
    deck.append(cards.rolling_plus_0_fire)


def add_one_plus_1_heal_2_self(deck: Deck) -> None:
    deck.append(cards.plus_1_heal_2_self)


def add_two_rolling_plus_0_heal_1_self(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_heal_1_self)
    deck.append(cards.rolling_plus_0_heal_1_self)


def repl_one_plus_0_w_one_rolling_plus_2(deck: Deck) -> None:
    deck.remove(cards.plus_0)
    deck.append(cards.rolling_plus_2)


def add_two_rolling_plus_0_wound(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_wound)
    deck.append(cards.rolling_plus_0_wound)


def add_one_rolling_plus_1_disarm(deck: Deck) -> None:
    deck.append(cards.rolling_plus_1_disarm)


def repl_two_plus_0_w_two_plus_1(deck: Deck) -> None:
    deck.remove(cards.plus_0)
    deck.remove(cards.plus_0)
    deck.append(cards.plus_1)
    deck.append(cards.plus_1)


def add_one_plus_1_poison(deck: Deck) -> None:
    deck.append(cards.plus_1_poison)


def add_one_minus_1_dark(deck: Deck) -> None:
    deck.append(cards.minus_1_dark)


def repl_one_minus_1_dark_w_one_plus_1_dark(deck: Deck) -> None:
    deck.remove(cards.minus_1_dark)
    deck.append(cards.plus_1_dark)


def add_two_rolling_plus_0_curse(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_curse)
    deck.append(cards.rolling_plus_0_curse)


def ignore_negative_scenario_and_add_two_plus_1(deck: Deck) -> None:
    # IGNORE NEGATIVE SCENARIO EFFECTS HERE
    deck.append(cards.plus_1)
    deck.append(cards.plus_1)


def add_one_plus_1_invisible_self(deck: Deck) -> None:
    deck.append(cards.plus_1_invisible_self)


def add_three_rolling_plus_0_poison(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_poison)
    deck.append(cards.rolling_plus_0_poison)
    deck.append(cards.rolling_plus_0_poison)


def add_one_plus_1_air(deck: Deck) -> None:
    deck.append(cards.plus_1_air)


def ignore_negative_scenario_and_add_one_plus_1(deck: Deck) -> None:
    # IGNORE NEGATIVE SCENARIO EFFECTS HERE
    deck.append(cards.plus_1)


def ignore_negative_item_and_add_two_plus_1(deck: Deck) -> None:
    # IGNORE NEGATIVE ITEM EFFECTS HERE
    deck.append(cards.plus_1)
    deck.append(cards.plus_1)


def add_one_rolling_plus_0_heal_3_self(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_heal_3_self)


def repl_two_plus_1_w_plus_4(deck: Deck) -> None:
    deck.remove(cards.plus_1)
    deck.remove(cards.plus_1)
    deck.append(cards.plus_4)


def repl_one_plus_0_w_one_plus_1_immobilize(deck: Deck) -> None:
    deck.remove(cards.plus_0)
    deck.append(cards.plus_1_immobilize)


def repl_one_plus_0_w_one_plus_1_disarm(deck: Deck) -> None:
    deck.remove(cards.plus_0)
    deck.append(cards.plus_1_disarm)


def repl_one_plus_0_w_one_plus_2_wound(deck: Deck) -> None:
    deck.remove(cards.plus_0)
    deck.append(cards.plus_2_wound)


def repl_one_plus_0_w_one_plus_2_poison(deck: Deck) -> None:
    deck.remove(cards.plus_0)
    deck.append(cards.plus_2_poison)


def repl_one_plus_0_w_one_plus_2_curse(deck: Deck) -> None:
    deck.remove(cards.plus_0)
    deck.append(cards.plus_2_curse)


def repl_one_plus_0_w_one_plus_3_muddle(deck: Deck) -> None:
    deck.remove(cards.plus_0)
    deck.append(cards.plus_3_muddle)


def repl_one_minus_1_w_one_plus_0_stun(deck: Deck) -> None:
    deck.remove(cards.minus_1)
    deck.append(cards.plus_0_stun)


def add_three_rolling_plus_1(deck: Deck) -> None:
    deck.append(cards.rolling_plus_1)
    deck.append(cards.rolling_plus_1)
    deck.append(cards.rolling_plus_1)


def add_one_rolling_plus_0_fire_and_one_rolling_plus_0_air(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_fire)
    deck.append(cards.rolling_plus_0_air)


def add_two_rolling_plus_0_light(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_light)
    deck.append(cards.rolling_plus_0_light)


def add_two_rolling_plus_0_shield_1_self(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_shield_1_self)
    deck.append(cards.rolling_plus_0_shield_1_self)


def repl_two_plus_1_w_plus_3_shield_1_self(deck: Deck) -> None:
    deck.remove(cards.plus_1)
    deck.remove(cards.plus_1)
    deck.append(cards.plus_3_shield_1_self)


def repl_one_plus_0_w_one_plus_1_shield_1_ally(deck: Deck) -> None:
    deck.remove(cards.plus_0)
    deck.append(cards.plus_1_shield_1_ally)


def repl_one_plus_0_w_one_plus_2_dark(deck: Deck) -> None:
    deck.remove(cards.plus_0)
    deck.append(cards.plus_2_dark)


def repl_one_plus_0_w_one_plus_2_light(deck: Deck) -> None:
    deck.remove(cards.plus_0)
    deck.append(cards.plus_2_light)


def repl_one_plus_0_w_one_plus_2_regenerate_self(deck: Deck) -> None:
    deck.append(cards.plus_2_regenerate_self)


def repl_one_minus_1_w_one_plus_1_heal_2_ally(deck: Deck) -> None:
    deck.remove(cards.minus_1)
    deck.append(cards.plus_1_heal_2_ally)


def repl_one_plus_0_w_one_plus_1_dark(deck: Deck) -> None:
    deck.remove(cards.plus_0)
    deck.append(cards.plus_1_dark)


def repl_one_plus_0_w_one_plus_1_ice(deck: Deck) -> None:
    deck.remove(cards.plus_0)
    deck.append(cards.plus_1_ice)


def repl_one_minus_1_w_one_plus_0_heal_1_ally(deck: Deck) -> None:
    deck.remove(cards.minus_1)
    deck.append(cards.plus_0_heal_1_ally)


def add_one_plus_1_heal_1_ally(deck: Deck) -> None:
    deck.append(cards.plus_1_heal_1_ally)


def remo_one_minus_2_and_one_plus_1(deck: Deck) -> None:
    deck.remove(cards.minus_2)
    deck.remove(cards.plus_1)


def repl_one_plus_1_w_one_plus_2_fire(deck: Deck) -> None:
    deck.remove(cards.plus_1)
    deck.append(cards.plus_2_fire)


def repl_one_plus_1_w_one_plus_2_light(deck: Deck) -> None:
    deck.remove(cards.plus_1)
    deck.append(cards.plus_2_light)


def add_one_plus_1_fire_and_light(deck: Deck) -> None:
    deck.append(cards.plus_1_fire_and_light)


def repl_one_plus_0_w_one_plus_1_wound(deck: Deck) -> None:
    deck.remove(cards.plus_0)
    deck.append(cards.plus_1_wound)


def repl_one_plus_0_w_one_plus_2_muddle(deck: Deck) -> None:
    deck.remove(cards.plus_0)
    deck.append(cards.plus_2_muddle)


def repl_one_minus_1_w_one_plus_0_poison(deck: Deck) -> None:
    deck.remove(cards.minus_1)
    deck.append(cards.plus_0_poison)


def repl_one_plus_1_w_one_plus_2_earth(deck: Deck) -> None:
    deck.remove(cards.plus_1)
    deck.append(cards.plus_2_earth)


def add_one_plus_0_damage_adjacent_enemies_1(deck: Deck) -> None:
    deck.append(cards.plus_0_damage_adjacent_enemies_1)


def repl_one_plus_0_w_one_plus_1_poison(deck: Deck) -> None:
    deck.remove(cards.plus_0)
    deck.append(cards.plus_1_poison)


def repl_one_plus_0_w_one_plus_1_push_2(deck: Deck) -> None:
    deck.remove(cards.plus_0)
    deck.append(cards.plus_1_push_2)


def repl_one_plus_0_w_one_plus_0_stun(deck: Deck) -> None:
    deck.remove(cards.plus_0)
    deck.append(cards.plus_0_stun)


def repl_one_plus_1_w_one_plus_1_stun(deck: Deck) -> None:
    deck.remove(cards.plus_1)
    deck.append(cards.plus_1_stun)


def add_one_plus_2_air(deck: Deck) -> None:
    deck.append(cards.plus_2_air)


def repl_one_plus_1_w_one_plus_3(deck: Deck) -> None:
    deck.remove(cards.plus_1)
    deck.append(cards.plus_3)


def ignore_negative_item_and_remo_one_minus_1(deck: Deck) -> None:
    # IGNORE NEGATIVE ITEM EFFECTS HERE
    deck.remove(cards.minus_1)


def add_one_minus_1_add_bb_counter(deck: Deck) -> None:
    deck.append(cards.minus_1_add_bb_counter)


def add_one_plus_1_regenerate_self(deck: Deck) -> None:
    deck.append(cards.plus_1_regenerate_self)


def ignore_negative_scenario_and_remo_two_plus_0(deck: Deck) -> None:
    # IGNORE NEGATIVE SCENARIO EFFECTS HERE
    deck.remove(cards.plus_0)
    deck.remove(cards.plus_0)


def repl_one_minus_2_w_one_minus_1_and_one_plus_1(deck: Deck) -> None:
    deck.remove(cards.minus_2)
    deck.append(cards.minus_1)
    deck.append(cards.plus_1)


def add_one_rolling_plus_0_heal_2_ally(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_heal_2_ally)


def add_one_plus_2_dark(deck: Deck) -> None:
    deck.append(cards.plus_2_dark)


def ignore_negative_scenario_and_remo_one_minus_1(deck: Deck) -> None:
    # IGNORE NEGATIVE SCENARIO EFFECTS HERE
    deck.remove(cards.minus_1)


def add_one_rolling_plus_0_token_back_one(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_token_back_one)


def repl_one_minus_1_w_plus_0_consume_anye_infuse_anye(deck: Deck) -> None:
    deck.remove(cards.minus_1)
    deck.append(cards.plus_0_consume_anye_infuse_anye)


def repl_one_plus_0_w_one_rolling_plus_1(deck: Deck) -> None:
    deck.remove(cards.plus_0)
    deck.append(cards.rolling_plus_1)


def repl_one_minus_2_w_one_minus_1_and_one_rolling_plus_0_pierce_2(deck: Deck) -> None:
    deck.remove(cards.minus_2)
    deck.append(cards.minus_1)
    deck.append(cards.rolling_plus_0_pierce_2)


def add_one_rolling_plus_0_regenerate_self(deck: Deck) -> None:
    deck.append(cards.rolling_plus_0_regenerate_self)


def add_one_plus_1_heal_1_self(deck: Deck) -> None:
    deck.append(cards.plus_1_heal_1_self)


def repl_one_plus_0_w_one_plus_1_earth(deck: Deck) -> None:
    deck.remove(cards.plus_0)
    deck.append(cards.plus_1_earth)


def remo_one_minus_2(deck: Deck) -> None:
    deck.remove(cards.minus_2)


def add_two_plus_2(deck: Deck) -> None:
    deck.append(cards.plus_2)
    deck.append(cards.plus_2)
