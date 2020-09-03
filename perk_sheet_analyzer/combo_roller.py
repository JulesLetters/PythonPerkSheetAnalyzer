import math

BASE_COUNT = 20


def count_combos(rollings, term_count):
    if len(rollings) == 0:
        return [([], term_count)]
    combos = []
    head = rollings[0]
    tail = count_combos(rollings[1:], term_count)
    count_factor = 1
    for i in range(1 + rollings[0]["count"]):
        for tail_combo in tail:
            combo = ([head["symbol"]] * i, count_factor * tail_combo[1])
            combo[0].extend(tail_combo[0])
            combos.append(combo)
        count_factor *= head["count"] - i
        count_factor /= (i + 1)
    return combos


def adjust_count(combo, total):
    count = combo[1] * math.factorial(len(combo[0])) \
            * math.factorial(total - 1 - len(combo[0]))
    return (combo[0], count)


def build_deck(rollings=[], term_count=1):
    total = term_count
    for rolling in rollings:
        total += rolling["count"]
    return {
        "combos": [adjust_count(combo, total)
                   for combo in count_combos(rollings, term_count)],
        "permutations": math.factorial(total)
    }


def collect_decks(rollings=[], terminals=[]):
    decks = []
    max_term_count = BASE_COUNT
    for terminal in terminals:
        max_term_count += terminal["count"]
    max_rollings = [rolling["count"] for rolling in rollings]
    for term_count in range(BASE_COUNT, max_term_count + 1):
        while True:
            decks.append(build_deck(rollings, term_count))
            for (i, rolling) in enumerate(rollings):
                if rolling["count"]:
                    rolling["count"] -= 1
                    break
                else:
                    rolling["count"] = max_rollings[i]
            else:
                break
    return decks


def main():
    rollings = []
    rollings.append({'symbol': "A", 'count': 1})
    rollings.append({'symbol': "B", 'count': 2})
    rollings.append({'symbol': "C", 'count': 2})
    rollings.append({'symbol': "D", 'count': 2})
    rollings.append({'symbol': "E", 'count': 2})

    terminals = []
    terminals.append({'symbol': "t", 'count': 5})

    print(collect_decks(rollings, terminals))


if __name__ == '__main__':
    main()
