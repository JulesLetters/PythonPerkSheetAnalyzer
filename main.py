import deck_analyzer
import deck_generator
import perk_sheets


def main():
    results = []
    maximum = 0

    all_decks = deck_generator.generate_all_decks_for(perk_sheets.triforce)
    deck_count = len(all_decks)
    print("Decks to analyze: {}".format(deck_count))
    for deck in all_decks:
        deck_stats = deck_analyzer.calculate_statistics(deck)
        rate = deck_stats.effect_rates['ICE']
        if maximum < rate:
            results = [(deck, deck_stats)]
            maximum = rate
        elif maximum == rate:
            results += [(deck, deck_stats)]

    print()
    print("Attack Type: Normal")
    print("  Maximal decks: {}".format(len(results)))
    print("  Maximum value: {}".format(maximum))
    print("   Decks:")
    for (deck, deck_stats) in results:
        print("   {}".format(deck))


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
