# day8.py
#
# --- Day 8: Haunted Wasteland ---

from utils import *


def part1(data):
    D = data.strip()
    directions, nodes = parse_data(D)
    p1 = solve(directions=directions, nodes=nodes)
    print(p1)  # 6 | 22199


def part2(data):
    D = data.strip()
    directions, nodes = parse_data(D)
    p2 = solve(directions=directions, nodes=nodes)
    print(p2)  # 6 | ?


def solve(directions: list[int], nodes: tuple[str]) -> int:
    """
    LLR

    AAA = (BBB, BBB)
    BBB = (AAA, ZZZ)
    ZZZ = (ZZZ, ZZZ)
    """
    loop_limit = 100_000
    node_dst = 'ZZZ'
    n_dir = len(directions)

    node_cur = 'AAA'
    steps = 0

    while node_cur != node_dst and steps < loop_limit:
        cur_d = directions[steps % n_dir]
        node_cur = nodes[node_cur][cur_d]
        steps += 1

    print(directions, nodes)
    return steps


def get_neighbour_nodes(line: str) -> tuple[str]:
    ns: list[str] = line.replace('(', '').replace(')', '').split(',')
    return tuple(map(str.strip, ns))


def parse_data(D: str) -> tuple[list[int], dict]:
    directions = [1 if d == 'R' else 0 for d in (list(D.split()[0]))]
    nodes = {line.split('=')[0].strip(): get_neighbour_nodes(line.split('=')[1]) for line in D.splitlines()[2:]}
    return directions, nodes


check_test(part1, part2)
# cProfile.run(statement='check_test(part1, part2)', sort='cumulative')

# cProfile.run(statement='check(part1, part2)', sort='cumulative')
"""
"""
