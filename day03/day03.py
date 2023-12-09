from utils import *


def part1(data: str):
    D: list[str] = list(data.splitlines())
    max_i, max_j = len(D), len(D[0].strip())
    chars: dict = {(r, c): [] for r in range(max_i) for c in range(max_j) if
                   D[r][c] not in '0123456789.'}

    for r, row in enumerate(D):
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
    p1 = sum(sum(p) for p in chars.values())

    print(p1)


def part2(data: str):
    D: list[str] = list(data.splitlines())
    max_i, max_j = len(D), len(D[0].strip())
    chars: dict = {(r, c): [] for r in range(max_i) for c in range(max_j) if
                   D[r][c] not in '0123456789.'}

    for r, row in enumerate(D):
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

    p2 = sum(math.prod(p) for p in chars.values() if len(p) == 2)

    print(p2)


check_test(part1, part2)
check(part1, part2)

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
