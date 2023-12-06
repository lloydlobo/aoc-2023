# day2.py

"""
--- Day 2: Cube Conundrum ---

https://adventofcode.com/2023/day/2
"""

import os


def check() -> int:
    assert (part1() == 0)
    assert (part2() == 0)
    return 0


def part1() -> int:
    data: str
    with open(os.path.join('input', 'day2')) as infile:
        data = (infile.read()).strip()
    # print(data)
    sum_ids = 0
    # return sum_ids
    return 0


def part2() -> int:
    # NOTE: data used is same as day1 part 1
    data: str
    with open(os.path.join('input', 'day2')) as infile:
        data = (infile.read()).strip()
    total: int = 0
    # return total
    return 0
