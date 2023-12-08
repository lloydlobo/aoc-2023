from utils import *


def part1(input):
    D: str = input.strip()
    p1 = 0
    for row in D.split('\n'):
        p1_digits = []
        for c, col in enumerate(row):
            if col.isdigit():
                p1_digits.append(col)
        p1 += int(p1_digits[0] + p1_digits[-1])

    print(p1)


def part2(input):
    D: str = input.strip()
    p2 = 0
    for row in D.split('\n'):
        p2_digits = []
        for c, col in enumerate(row):
            if col.isdigit():
                p2_digits.append(col)
            for d, val in enumerate(
                    ['one', 'two', 'three', 'four', 'five', 'six', 'seven',
                     'eight', 'nine']):
                if row[c:].startswith(val):
                    p2_digits.append(str(d + 1))
        p2 += int(p2_digits[0] + p2_digits[-1])

    print(p2)


check_test(part1, part2)
check(part1, part2)
