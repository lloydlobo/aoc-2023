# day09.py

# --- Day 9: Mirage Maintenance ---
#
# Analyze your OASIS report and extrapolate the next value for each history.
# What is the sum of these extrapolated values?

from utils import *


def part1(data):
    D = data.strip()
    ldata = parse_data(D)
    diffs = [consec_diffs(lst=lst) for lst in ldata]
    p1 = solve(ldata, diffs)
    # print(p1)  # 114 | 1953784198


def part2(data):
    D = data.strip()
    d = parse_data(D)
    ldata = [np.flip(lst).tolist() for lst in d]  # np.flip(lst).tolist() == lst[::-1]
    diffs = [consec_diffs(lst=lst) for lst in ldata]
    p2 = solve(ldata, diffs)
    # print(p2)  # 2 | 957


def parse_data(data: str) -> list[list[int]]:
    """[list(map(int, line.split())) for line in data.splitlines()]"""
    return list(map(ints, data.splitlines()))


def consec_diffs_recursive(lst: list[int]) -> list[list[int]]:
    return [np.diff(lst).tolist()] + consec_diffs_recursive(np.diff(lst)) if len(lst) > 1 else []


def consec_diffs(lst: list[int]) -> list[list[int]]:
    """
    Calculate consecutive differences for a given list of integers.
    Return a list of lists representing differences at each step.

    0 3 6 9 12 15 -> [[3, 3, 3, 3, 3], [0, 0, 0, 0], [0, 0, 0], [0, 0], [0]]
    1 3 6 10 15 21 -> [[2, 3, 4, 5, 6], [1, 1, 1, 1], [0, 0, 0], [0, 0], [0]]
    10 13 16 21 30 45 -> [[3, 3, 5, 9, 15], [0, 2, 4, 6], [2, 2, 2], [0, 0], [0]]
    """
    diffs = []
    while len(lst) > 1:  # lst = [lst[i + 1] - lst[i] for i in range(len(lst) - 1)]
        lst = np.diff(lst)
        diffs.append(lst.tolist())
    return diffs


def solve(head_vals: list[list[int]], diffs_lines: list[list[list[int]]]):
    """
    Solve the problem by extrapolating the next value for each history.
    Return the sum of these extrapolated values.

    0: [0, 3, 6, 9, 12, 15, _] [[3, 3, 3, 3, 3, _]]
    1: [1, 3, 6, 10, 15, 21, _] [[2, 3, 4, 5, 6, _], [1, 1, 1, 1, _]]
    2: [10, 13, 16, 21, 30, 45, _] [[3, 3, 5, 9, 15, _], [0, 2, 4, 6, _], [2, 2, 2, _]]
    """
    extrapolated_vals: list[int] = [
        (head_row[-1] + sum(diff_row[-1]
                            for diff_row in diff_lines[::-1]
                            if any(diff_row))
         ) for (head_row, diff_lines) in zip(head_vals, diffs_lines)
    ]
    return sum(extrapolated_vals)


def dbg_inverted_triangle(triangle: list[list[int]]) -> None:
    """pascal_triangles = [[data_lsts[i]] + [lst for lst in diff if any(lst)] for i, diff in enumerate(diffs)]"""
    for depth, row in enumerate(triangle):
        n_row = len(row)
        print(' ' * depth + ' '.join(map(str, row)))


profile_stats_test = 'profile_stats_check_test'
cProfile.run('check_test(part1, part2)', profile_stats_test)
stats = pstats.Stats(profile_stats_test).strip_dirs()
stats.sort_stats('cumulative')
stats.print_stats(10)
"""
Sat Dec 16 12:37:42 2023    profile_stats_check_test (using recursion for diffs)
         769 function calls (732 primitive calls) in 0.002 seconds
Sat Dec 16 12:22:43 2023    profile_stats_check_test 587 function calls (580 primitive calls) in 0.001 seconds
Sat Dec 16 12:01:21 2023    profile_stats_check_test 587 function calls (580 primitive calls) in 0.001 seconds
Fri Dec 15 13:24:19 2023    profile_stats_check_test 20 function calls in 0.000 seconds
"""

profile_stats = 'profile_stats_check'
cProfile.run('check(part1, part2)', profile_stats)
stats = pstats.Stats(profile_stats).strip_dirs()
stats.sort_stats('cumulative')
stats.print_stats(10)
"""
Sat Dec 16 12:37:42 2023    profile_stats_check (using recursion for diffs)
         137121 function calls (129121 primitive calls) in 0.250 seconds
Sat Dec 16 12:22:43 2023    profile_stats_check 89119 function calls in 0.136 seconds
Sat Dec 16 12:01:21 2023    profile_stats_check 89119 function calls in 0.151 seconds
Sat Dec 16 10:12:40 2023    profile_stats_check 98915 function calls in 0.166 seconds
Sat Dec 16 08:22:41 2023    profile_stats_check 97715 function calls in 0.233 seconds
Sat Dec 16 08:18:32 2023    profile_stats_check 96515 function calls in 0.164 seconds
Sat Dec 16 08:15:34 2023    profile_stats_check 527591 function calls (455113 primitive calls) in 0.488 seconds
Fri Dec 15 19:04:03 2023    profile_stats_check 249645 function calls (213406 primitive calls) in 0.192 seconds
"""

"""
# https://publish.reddit.com/embed?url=https://www.reddit.com/r/adventofcode/comments/18e5ytd/comment/kclmg2j/
import sys
import numpy as np
lines = [[int(x) for x in line.split()] for line in sys.stdin.read().strip().splitlines()]
for p2 in (False, True):
    s = 0
    for line in lines:
        nums = np.array(line[::-1] if p2 else line)
        while np.any(nums):
            s += nums[-1]
            nums = np.diff(nums)
    print(s)
"""

"""
# LLM Summary

The given program is a solution for an Advent of Code problem, aiming to
analyze an OASIS report and extrapolate the next value for each historical
sequence. Here's a concise summary:

1. **Objective**: Find the sum of extrapolated values for historical sequences
   in an OASIS report.

2. **Approach**:
   - Consecutive differences are calculated using both recursive and iterative
     methods.
   - The program utilizes `numpy` for efficient array operations.

3. **Functions**:
   - `parse_data`: Converts raw input data into a list of lists of integers.
   - `consec_diffs_recursive` and `consec_diffs`: Calculate consecutive
     differences.
   - `solve`: Extrapolates the next value for each history and returns the sum.

4. **Code Flow**:
   - `part1`: Parses data, calculates differences, and solves the problem.
   - `part2`: Similar to `part1` with some data modifications.

5. **Performance Analysis**:
   - Profiling information compares recursive and iterative approaches,
     showing the iterative method is more efficient.

6. **Miscellaneous**:
   - Includes debugging functions (`dbg_inverted_triangle`).
   - Mentions a Reddit comment with an alternative solution using NumPy.

7. **Profile Statistics**:
   - Profiling results highlight the more efficient performance of the
     iterative approach.
"""
