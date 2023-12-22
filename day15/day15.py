# day15.py
from utils import *


def hash_simple(s: str) -> int:
    """ assert hash_simple('HASH') == 52 """
    cur: int = 0
    for c in s:
        cur += ord(c)
        cur *= 17
        cur %= 256
    return cur


def solve(sequences, for_part2=False):
    if not for_part2:
        return sum([hash_simple(sequence) for i, sequence in enumerate(sequences)])
    else:
        library: dict[int, list[str]] = {i: [] for i in range(256)}
        for sequence in sequences:
            if '=' in sequence:
                label = sequence[:sequence.index('=')]
                box_id = hash_simple(label)
                found_duplicate = False
                for lens_index, lens in enumerate(library[box_id]):
                    if lens.startswith(label):
                        library[box_id][lens_index] = sequence
                        found_duplicate = True
                if not found_duplicate:
                    library[box_id].append(sequence)
            elif '-' in sequence:
                label = sequence[:sequence.index('-')]
                box_id = hash_simple(label)
                for lens in library[box_id]:
                    if lens.startswith(label):
                        library[box_id].remove(lens)
        total = 0
        valid_libs = list((i, x) for i, x in enumerate(library.values()) if x)
        for box_id, lenses in valid_libs:
            for lens_idx, lens in enumerate(lenses):
                idx_eq = lens.index('=')
                focal_len = int(lens[(idx_eq + 1):])
                total += (box_id + 1) * (lenses.index(lens) + 1) * (focal_len)
        return total


# ----------------------------------------------------------------------------------------------------------------------


def part1(data):
    input_data = [data.split(',')][0]
    p1 = solve(input_data, for_part2=False)
    print(f'{p1=}')  # 1320 | 510273


def part2(data):
    input_data = [data.split(',')][0]
    p2 = solve(input_data, for_part2=True)
    print(f'{p2=}')  # 145 | 212449


# ----------------------------------------------------------------------------------------------------------------------

assert hash_simple('HASH') == 52

check_test(part1, part2)
check(part1, part2)
