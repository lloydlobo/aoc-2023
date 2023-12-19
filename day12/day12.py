# day12.py
#
# --- Day 12: Hot Springs ---
#
# For each row, count all of the different arrangements of operational and broken springs
# that meet the given criteria. What is the sum of those counts?

from utils import *


def part1(data):
    D = data.strip()
    # p1 = brute_force(d[0], d[1])
    p1 = solve(D)
    print(p1)  # 374 | 10494813


def part2(data):
    D = data.strip()
    # d = parse_data(D)
    # p2 = solve(d)
    # print(p2)  # 8410 | ?


def parse_blueprint(record: str):
    return (','.join([str(len(x)) for x in record.split('.') if x]))


@lru_cache(maxsize=None)
def recurse(record: str, nums: str) -> int:
    # 1. exit if done
    if record.count('?') == 0:  return 1 if parse_blueprint(record) == nums else 0
    # 2. Call itself recursively with '.' and with '#' returning total
    return (recurse(record.replace('?', '.', 1), nums) + recurse(record.replace('?', '#', 1), nums))


def solve(data: str):
    total_sum = 0
    for line in data.rstrip('\n').splitlines():  # pprint(dict(record=record, nums=nums))
        record, nums = line.split(' ')
        total_sum += recurse(record, nums)
    return total_sum


# def match(records: str, nums: list[int]) -> bool:
#     return nums == [
#         sum(1 for _ in grouper)
#         for key, grouper in itertools.groupby(records)
#         if key == "#"
#     ]
#
#
# def brute_force(records: str, nums: list[int]) -> int:
#     pprint((records,nums))
#     gen = ("#." if letter == "?" else letter for letter in records)
#     return sum(match(candidate, nums) for candidate in itertools.product(*gen))


check_test(part1, part2)
check(part1, part2)

"""
data:

???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""
"""
https://gist.github.com/mattieshoes/f9598c4d3839b2675d51b314ce29fdcd
"""
