import cProfile
import collections
import copy
import heapq
import itertools
import math
import numpy as np
import os
import pstats
import re
import regex
import sys
import time
import timeit

from collections import deque, defaultdict, Counter, OrderedDict
from enum import Enum
from functools import lru_cache
from io import StringIO
from pprint import pprint
from typing import TypeVar, Generator, Iterable, Tuple, List, Any, Union

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

def lmap(func, *iterables) -> list:
    return list(map(func, *iterables))


def ljoinstr(lst: list[Any], sep='') -> str:
    return sep.join(lmap(str, lst))


def ints(s: str) -> list[int]:
    # regex r"-?\d+" matches seqs of one or more digits (\d+) optionally preceded by a minus sign (-?).
    # Doesn't explicitly match a single zero (0), especially when it stood alone.
    return lmap(int, re.findall(r"-?\d+", s))


def intsall(s: str) -> list[int]:
    return lmap(int, re.findall(r"-?\d+|\b0\b", s))


# endregion


# region Grid


def gridinit(rows, cols, value=None):
    """Create a 2D grid with the specified number of rows and columns."""
    return [[value] * cols for _ in range(rows)]  # return [[default_value for _ in range(cols)] for _ in range(rows)]


def transpose(x):
    return list(map(list, zip(*x)))


def gridtranspose(grid: list[list]):
    """Transpose a 2D grid by swapping rows and columns."""
    nr, nc = len(grid), len(grid[0])
    return [[grid[j][i] for j in range(nr)] for i in range(nc)]


def strtogrid(multiline_str: str) -> list[list[str]]:
    """Convert a multi-line string to a 2D list of chars: each line becomes a sub-list."""
    return [list(r.strip()) for r in multiline_str.splitlines()]


# endregion

# region Debug printing

printlns = lambda data: print(*map(' '.join, data), sep='\n')


def dbg_lstrasgrid(lst_str: list[str]):
    for r in lst_str:
        for c in r:
            print(end=f'{c}\t')
        print()


# endregion

# region OS specific
OS_ENVIRON = os.environ.get('OS', '').lower()
CMD_CLEAR = 'cls' if 'win' in OS_ENVIRON else 'clear'
# clear_screen = lambda: os.system('cls' if os.name == 'nt' else 'clear')
clear_screen_ansi = lambda: print("\033[H\033[J")  # Moves cursor to top-left corner and clears screen


# endregion

# region Math

def gcd(a: int, b: int) -> int:
    """Greatest Common Divisor @usage: lcm = abs(a * b) // gcd(a, b)"""
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int):
    """Least Common Multiple @usage: lcm_of_3 = lcm(lcm(12, 18), 24)"""
    return abs(a * b) // gcd(a, b)


def picks_theorem(I: int, B: int) -> int:
    """
    I: number of interior lattice points
    B: number of lattice points on the boundary
    A = I + (B // 2) - 1
    """
    A = I + (B // 2) - 1
    return A


def shoelace_formula(vertices) -> float:
    """
    # vertices: list of tuples [(x1, y1), (x2, y2), ..., (xn, yn)]
    Thanks to tip from the [community](https://www.reddit.com/r/adventofcode/comments/18l0qtr/2023_day_18_solutions/)
    """
    n = len(vertices)
    area = 0.5 * abs(sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(vertices, vertices[1:] + [vertices[0]])))
    return area

# endregion
