# day8.py
#
# --- Day 8: Haunted Wasteland ---

from utils import *


def part1(data):
    D = data.strip()
    directions, nodes = parse_data(D)
    p1 = solve_1_iter(directions=directions, nodes=nodes)
    # p1 = solve_1_dfs(directions=directions, nodes=nodes)
    # print(p1)  # 6 | 22199


def part2(data):
    D = data.strip()
    directions, nodes = parse_data(D)
    node_srcs = [node for node in nodes if node.endswith('A')]
    history: dict[str, list[int]] = solve_2(directions=directions, nodes=nodes, node_srcs=node_srcs)
    steps_list: list[int] = [list(history[node])[0] for node in node_srcs]
    #   (['AAA', 'DVA', 'VXA', 'JHA', 'NMA', 'PXA'], [22199, 13207, 16579, 18827, 17141, 14893])
    p2 = lcm_of_list(steps_list)
    # print(p2)  # 6 | 13334102464297


def solve_1_iter(directions: list[int], nodes: dict[str, tuple[str]]) -> int:
    n_dir: int = len(directions)
    node_dst = 'ZZZ'
    node_cur = 'AAA'
    steps = 0
    while node_cur != node_dst:
        cur_d = directions[steps % n_dir]
        node_cur = nodes[node_cur][cur_d]
        steps += 1
    return steps


def solve_1_dfs(directions: list[int], nodes: dict[str, tuple[str]]) -> int:
    def solve_1_recursive(node_cur, directions, nodes, steps: int = 0):
        if node_cur == 'ZZZ':
            return steps
        cur_d = directions[steps % len(directions)]
        nxt_node = nodes[node_cur][cur_d]
        return solve_1_recursive(nxt_node, directions, nodes, steps + 1)

    node_cur = 'AAA'
    return solve_1_recursive(node_cur, directions, nodes)


def solve_2(directions: list[int], nodes: dict[str, tuple[str]], node_srcs: list[str]) -> dict[str, list[int]]:
    n_dir: int = len(directions)
    history = {node: [] for node in node_srcs}
    for node in node_srcs:
        cur_node = node
        steps = 0
        while True:
            if cur_node.endswith('Z'):
                history[node].append(steps)
                break
            cur_dir = directions[steps % n_dir]
            cur_node = nodes[cur_node][cur_dir]
            steps += 1
    return history


def lcm_of_list(steps_list: list[int]) -> int | None:
    """Returns number of steps for all nodes to land on 'Z' at the same time"""
    if not steps_list: return None
    cur_lcm = steps_list[0]
    for steps in steps_list[1:]:
        cur_lcm = lcm(cur_lcm, steps)
    return cur_lcm


def parse_data(D: str) -> tuple[list[int], dict[str, tuple[str]]]:
    def get_neighbour_nodes(line: str) -> tuple[str]:
        ns: list[str] = line.replace('(', '').replace(')', '').split(',')
        return tuple(map(str.strip, ns))

    directions = [1 if d == 'R' else 0 for d in D.split()[0]]
    nodes = {line.split('=')[0].strip(): get_neighbour_nodes(line.split('=')[1]) for line in D.splitlines()[2:]}

    return directions, nodes


# @deprecated
# def steps_to_common_node_ending(history, node_srcs) -> int | None:
#     common_steps = set(history[node_srcs[0]]).intersection(*history.values())
#     s = min(common_steps, default=None)
#     return s


cProfile.run(statement='check_test(part1, part2)', sort='cumulative')
"""
         79 function calls in 0.000 seconds
         80 function calls in 0.000 seconds
"""

cProfile.run(statement='check(part1, part2)', sort='cumulative')
"""
         113969 function calls in 0.096 seconds
         113970 function calls in 0.096 seconds
"""

"""
# LLM Summary

The mission is to make nodes that end with 'A' all reach 'Z' together. To pull this off, we turn to the Least Common 
Multiple (LCM) of their individual steps to 'Z'. Here's how it works:

1. **Different Steps for Each Node:** Each 'A'-ending node needs a different number of steps to reach 'Z'. The 
challenge is to find a common time frame for all nodes.

2. **LCM to the Rescue:** The LCM is like the smallest shared time unit that all nodes can sync with. It tells us 
when each 'A' node will finish its journey and reach 'Z'.

3. **Teamwork with LCM:** Calculating the LCM helps us pinpoint the exact moment when all nodes complete one full 
cycle and land at 'Z' at the same time.

4. **Syncing Periodic Paths:** Think of it as aligning different repeating paths ('A'-ending nodes). The LCM is the 
magic number that makes sure all paths align perfectly.

In a nutshell, getting all 'A' nodes to 'Z' together, despite having different step counts, boils down to finding the 
LCM."""
