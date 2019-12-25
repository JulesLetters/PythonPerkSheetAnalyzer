import itertools
import timeit
from collections import OrderedDict
from fractions import Fraction
from typing import List, Dict

from deck_analyzer.combo_roller import collect_decks


def generate_string(counts: Dict) -> str:
    return "".join([str(unit) * quantity for unit, quantity in counts.items()])


def _ordered_combination(counts: Dict, max_combo_len: int, counts_keys: List, counts_index: int,
                         previous_pieces: Dict) -> List:
    result = []

    current_sum = sum(previous_pieces.values())
    if current_sum == max_combo_len:
        return [previous_pieces.copy()]

    if counts_index == len(counts_keys):
        return []

    unit = counts_keys[counts_index]
    maximum = counts[unit]
    max_current_allocatable = min(maximum, max_combo_len - current_sum)
    for i in range(max_current_allocatable, -1, -1):
        previous_pieces[unit] = i
        result.extend(_ordered_combination(counts, max_combo_len, counts_keys, counts_index + 1, previous_pieces))
    return result


def ordered_combinations(counts: Dict, max_combo_len: int) -> List:
    return _ordered_combination(counts, max_combo_len, list(counts.keys()), 0, {})


def main():
    dict_tester = {'a': Fraction(2, 3)}

    new_dict = dict_tester.copy()
    new_dict['a'] += Fraction(3, 3)

    assert new_dict['a'] == Fraction(5, 3)
    assert dict_tester['a'] == Fraction(2, 3)
    print(new_dict['a'])
    print(dict_tester['a'])

    frac_a = Fraction(2, 3)
    frac_b = Fraction(5, 7)

    frac_c = frac_b
    frac_x = Fraction(frac_b)

    frac_b += frac_a
    print(frac_b)
    print(frac_c)

    # counts = {"A": 1, "B": 2, "C": 3, "D": 1}
    counts = OrderedDict([("A", 1), ("B", 2), ("C", 3), ("D", 1)])
    string_counts = generate_string(counts)
    print(string_counts)

    expected_set = generate_expected_set(string_counts, 3)
    combinations = ordered_combinations(counts, 3)

    # rollings.append({'symbol': "B", 'count': 3})
    combo_setup = [{'symbol': k, 'count': v} for k, v in counts.items()]
    # print(count_combos(combo_setup, 3))

    a = timeit.timeit(lambda: [generate_expected_set(string_counts, x) for x in range(1, sum(counts.values()) + 1)],
                      number=10000)
    b = timeit.timeit(lambda: [ordered_combinations(counts, x) for x in range(1, sum(counts.values()) + 1)],
                      number=10000)
    c = timeit.timeit(lambda: collect_decks(combo_setup, []), number=10000)
    print(a)
    print(b)
    print(c)

    all_strings = [generate_string(x) for x in combinations]

    # print()
    # print()
    # print("-- Expected Strings --")
    # for s in expected_set:
    #     print(s)
    #
    # print("-- Generated Strings --")
    # for s in all_strings:
    #     print(s)

    print("", flush=True)
    assert expected_set == set(all_strings)


def generate_expected_set(string_counts, length):
    return set(["".join(sorted(c)) for c in itertools.combinations(string_counts, length)])


if __name__ == '__main__':
    main()
