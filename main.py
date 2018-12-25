from multiset import Multiset

from attack_drawer import AttackDrawer
from draw_parser import DrawParser
from simple_timer_context import SimpleTimerContext


def main():
    default_deck = ['+0', '+0', '+0', '+0', '+0', '+0',
                    '+1', '+1', '+1', '+1', '+1',
                    '-1', '-1', '-1', '-1', '-1',
                    '-2', '+2', 'x0', 'x2']
    deck = default_deck.copy()
    print(deck)

    input_deck = Multiset(deck)
    with SimpleTimerContext("Generating all possible draws for deck."):
        all_possible_draws = AttackDrawer.form_all_advantage_draws(input_deck)
    for draw in all_possible_draws:
        print(DrawParser.make_result(draw))


# Final output:
# Average Damage: +#.##
# Terminators:
#   x2: ##.##%
#   x0: ##.##%
#   +0: ##.##%
#   etc: etc%
# Special procs:
# Stun: ##.##%
# Wound: ##.##%
# Refresh: ##.##%
# etc.  Bare rolling modifiers are not found here (personal preference!).


if __name__ == '__main__':
    main()

# Desired output: Frequency of each result. That is, what's my expected % outcome for a given card-type?
# I don't actually care about the "big chains" of rolling modifiers.
# I just want to know what my odds of a given effect happening are.

# If last attack is all rolling modifiers, shuffle the non-rolled part of the deck in.
# (shouldn't matter for this program v1.)
