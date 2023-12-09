import sys
import itertools
import math
import regex
import re
from collections import deque, defaultdict, Counter
from typing import TypeVar, Generator, Iterable, Tuple, List, Any
from pprint import pprint

sys.setrecursionlimit(100_000)

# Instead of changing these functions, copy it

# https://github.com/nthistle/advent-of-code/blob/master/2022/day25/aoc_tools.py
_T = TypeVar("T")


def read_input(filename) -> str:
    with open(filename) as f:
        return f.read()


def check_test(part1, part2):
    filename = 'testinput.txt'
    data: str = read_input(filename)
    part1(data)
    part2(data)


def check(part1, part2):
    filename = 'input.txt'
    data: str = read_input(filename)
    part1(data)
    part2(data)


# region Strings, lists, dicts
#
# References:
#   - https://github.com/mcpower/adventofcode/blob/master/utils.py

def lmap(func, *iterables):
    return list(map(func, *iterables))


def ints(s: str) -> list[int]:
    return lmap(int, re.findall(r"-?\d+", s))

# endregion
