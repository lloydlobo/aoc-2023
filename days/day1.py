# day1.py

"""
--- Day 1: Trebuchet?! ---

https://adventofcode.com/2023/day/1
"""

import os


def check() -> int:
    assert (part1() == 55002)
    assert (part2() == 55093)
    return 0


def part1() -> int:
    data: str
    with open(os.path.join('input', 'day1')) as infile:
        data = (infile.read()).strip()
    total: int = 0
    for line in data.splitlines():
        first, last = None, None
        for (f, l) in zip(line, line[::-1]):
            if first and last:
                break
            if f.isdigit() and first is None:
                first = f
            if l.isdigit() and last is None:
                last = l
        if first and last:
            total += int(f'{first}{last}')
    return total


def part2() -> int:
    # NOTE: data used is same as day1 part 1
    data: str
    with open(os.path.join('input', 'day1')) as infile:
        data = (infile.read()).strip()
    digits: list[str] = ['one', 'two', 'three', 'four', 'five', 'six', 'seven',
                         'eight', 'nine', ]
    total: int = 0
    for line in data.splitlines():
        first, last = None, None
        buf_first, buf_last = list(), list()
        for (f, l) in zip(line, line[::-1]):
            if first and last:
                break
            if first is None:
                if f.isdigit():
                    first = f
                if f.isalpha():
                    buf_first.append(f)
                    str_first = ''.join(buf_first)
                    for d in digits:
                        if d in str_first:
                            first = str(digits.index(d) + 1)
                            break
            if last is None:
                if l.isdigit():
                    last = l
                if l.isalpha():
                    buf_last.append(l)
                    str_last = ''.join(buf_last[::-1])
                    for d in digits:
                        if d in str_last:
                            last = str(digits.index(d) + 1)
                            break
        if first and last:
            total += int(f'{first}{last}')
    return total
