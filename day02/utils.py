import sys
import itertools
import regex
from collections import deque, defaultdict, Counter
from typing import TypeVar, Generator, Iterable, Tuple, List, Any

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
