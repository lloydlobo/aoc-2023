from utils import *

"""
rn=1 becomes 30.
cm- becomes 253.
qp=3 becomes 97.
cm=2 becomes 47.
qp- becomes 14.
pc=4 becomes 180.
ot=9 becomes 9.
ab=5 becomes 197.
pc- becomes 48.
pc=6 becomes 214.
ot=7 becomes 231.
In this example, the sum of these results is 1320. Unfortunately, the reindeer has stolen the page containing the expected verification number and is currently running around the facility with it excitedly.

Run the HASH algorithm on each step in the initialization sequence. What is the sum of the results? (The initialization sequence is one long line; be careful when copy-pasting it.)
"""


# ----------------------------------------------------------------------------------------------------------------------

def hash_simple(s: str) -> int:
    """ assert hash_simple('HASH') == 52 """
    cur: int = 0
    for c in s:
        cur += ord(c)
        cur *= 17
        cur %= 256
    return cur


def solve(sequences, for_part2=False):
    if for_part2:
        return -1

    sum_sequences = 0
    for i, sequence in enumerate(sequences):
        sum_sequences += hash_simple(sequence)

    return sum_sequences


# ----------------------------------------------------------------------------------------------------------------------


def part1(data):
    input_data = [data.split(',')][0]
    print(f'{input_data=}')

    p1 = solve(input_data, for_part2=False)
    print(f'{p1=}')  # 1320 | 510273


def part2(data):
    input_data = strtogrid(copy.deepcopy(data))
    p2 = solve(input_data, for_part2=True)
    print(f'{p2=}')  # ? | ?


# ----------------------------------------------------------------------------------------------------------------------

assert hash_simple('HASH') == 52

check_test(part1, part2)
check(part1, part2)
