# day3.py

# --- Day 3: Gear Ratios ---
#
#
# https://adventofcode.com/2023/day/3
#
# --- Part 1 ---
#
# To find the sum of all part numbers in the engine schematic,
# you need to consider each number adjacent to a symbol,
# including diagonally. Periods (.) do not count as symbols.
#
# Let's calculate the sum based on the provided example:
#
# Example engine schematic:
# ```
# 467..114..
# ...*......
# ..35..633.
# ......#...
# 617*......
# .....+.58.
# ..592.....
# ......755.
# ...$.*....
# .664.598..
# ```
#
# In this schematic, two numbers are not part numbers because they are not
# adjacent to a symbol: 114 (top right) and 58 (middle right).
# Every other number is adjacent to a symbol and so is a part number;
# their sum is 4361.
#
# --- Part 2 ---

# You've got a machine with some gears that affect its speed.
# There are symbols (*) next to two numbers,
# and multiplying those numbers together gives you a gear ratio.
# Your task is to find the gear ratios for each gear and add them up.
#
# Look at the numbers around the star (*) symbols, multiply the two
# adjacent numbers, and then add all those gear ratios together.
# The total of these gear ratios will help identify which gear needs fixing.
#
# https://www.reddit.com/r/adventofcode/comments/189m3qw/2023_day_3_solutions/
#
# Wow! This makes two assumptions that ended up being true for the input:
# - No number touches more than one symbol
# - No non-star symbol touches exactly two numbers

import math
import os
from pprint import pprint
from typing import List, TextIO

FILEPATH = os.path.join('input', 'day3')


def check() -> int:
    infile: TextIO
    with open(FILEPATH) as infile:
        assert (part1(infile) == 535235)
        assert (part2(infile) == 79844424)

    return 0


def part1(infile: TextIO) -> int:
    grid = list(open(FILEPATH))

    max_i, max_j = len(grid), len(grid[0].strip())

    chars: dict = {(r, c): [] for r in range(max_i) for c in range(max_j) if
                   grid[r][c] not in '0123456789.'}

    for r, row in enumerate(grid):
        buf = ''

        for c, col_val in enumerate(row):
            if col_val.isdigit():
                buf += col_val
            elif buf:
                edge = {(r, c_idx) for r in (r - 1, r, r + 1) for c_idx in
                        range(max(0, c - len(buf) - 1), min(max_j, c + 1))}

                for o in edge & chars.keys():
                    chars[o].append(int(buf))

                buf = ''
    # pprint(chars)
    sum_part_nums = sum(sum(p) for p in chars.values())
    # print(sum_part_nums)

    return sum_part_nums


def part2(infile: TextIO) -> int:
    grid = list(open(FILEPATH))

    max_i, max_j = len(grid), len(grid[0].strip())

    chars: dict = {(r, c): [] for r in range(max_i) for c in range(max_j) if
                   grid[r][c] not in '0123456789.'}

    for r, row in enumerate(grid):
        buf = ''

        for c, col_val in enumerate(row):
            if col_val.isdigit():
                buf += col_val
            elif buf:
                edge = {(r, c_idx) for r in (r - 1, r, r + 1) for c_idx in
                        range(max(0, c - len(buf) - 1), min(max_j, c + 1))}

                for o in edge & chars.keys():
                    chars[o].append(int(buf))

                buf = ''
    # pprint(chars)

    product_part_nums = sum(math.prod(p) for p in chars.values() if len(p) == 2)
    # print(product_part_nums)
    return product_part_nums


def part1_old(data: str) -> int:
    grid: List[List[str]] = [list(row) for row in data.splitlines()]
    max_y, max_x = len(grid), len(grid[0])  # rows = 140, cols = 140

    all_nums = []
    nums, char_buf = [], []

    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char.isdigit():
                char_buf.append(char)
            elif char_buf:
                all_nums.append(int(''.join(char_buf)))
                nums.append(int(''.join(char_buf)))

                found_symbol = False
                n_char_buf = len(char_buf)

                for idx_, n in enumerate(char_buf):
                    j_tmp_idx = (j - 1) - (idx_ % n_char_buf)  # reverse order.
                    for y in range(-1, 2):
                        if found_symbol:
                            break
                        for x in range(-1, 2):
                            ny, nx = (y + i), (j_tmp_idx + x)

                            if (0 <= ny < max_y) and (0 <= nx < max_x):
                                if is_symbol(grid[ny][nx]) and not found_symbol:
                                    found_symbol = True
                                    break
                if not found_symbol:  # pop last num if no symbols found near tmp_nums its char digits
                    nums.pop()
                else:
                    found_symbol = False

                char_buf.clear()

    return sum(nums)


"""
chars = {(0, 3): [], (0, 4): [], (0, 8): [], (0, 9): [], (1, 0): [], (1, 1): [], (1, 2): [], (1, 3): [], (1, 4): [], (1, 5): [], (1, 6): [], (1, 7): [], (1, 8): [], (1, 9): [], (2, 0): [], (2, 1): [], (2, 4): [], (2, 5): [], (2, 9): [], (3, 0): [], (3, 1): [], (3, 2): [], (3, 3): [], (3, 4): [], (3, 5): [], (3, 6): [], (3, 7): [], (3, 8): [], (3, 9): [], (4, 3): [], (4, 4): [], (4, 5): [], (4, 6): [], (4, 7): [], (4, 8): [], (4, 9): [], (5, 0): [], (5, 1): [], (5, 2): [], (5, 3): [], (5, 4): [], (5, 5): [], (5, 6): [], (5, 9): [], (6, 0): [], (6, 1): [], (6, 5): [], (6, 6): [], (6, 7): [], (6, 8): [], (6, 9): [], (7, 0): [], (7, 1): [], (7, 2): [], (7, 3): [], (7, 4): [], (7, 5): [], (7, 9): [], (8, 0): [], (8, 1): [], (8, 2): [], (8, 3): [], (8, 4): [], (8, 5): [], (8, 6): [], (8, 7): [], (8, 8): [], (8, 9): [], (9, 0): [], (9, 4): [], (9, 8): [], (9, 9): []}
{(1, 7): [954],
 (1, 27): [52, 398],
 (1, 57): [806, 983],
 (1, 95): [217],
 (2, 62): [664, 943],
 (2, 79): [677, 6],
 (2, 102): [459, 687],
 (2, 114): [687],
 (3, 37): [548],
 (3, 45): [495, 488],
 (3, 85): [282, 773],
 (3, 106): [973],
 (3, 112): [2, 244],
 (3, 118): [248],
 (3, 123): [409, 311],
 (3, 128): [722, 286],
 (3, 133): [165],
 (4, 5): [261],
 (4, 10): [663],
 (4, 33): [704, 842],
 (4, 40): [268, 696],
 (5, 20): [442],
 (5, 28): [828, 563],
 (5, 54): [534],
 (5, 65): [512],
 ...

"""

"""
edge = {(-1, 11), (0, 7), (-1, 8), (0, 10), (1, 11), (-1, 7), (1, 8), (0, 9), (-1, 10), (1, 7), (-1, 9), (1, 10), (0, 8), (1, 9), (0, 11)}
"""
