from utils import *


def solve(grid, lo, hi, is_part2):
    """
    Purpose: Find the ~shortest~ least heat-loss accumulating path from a source node
    to all other nodes in a weighted graph with non-negative weights.
    Assign a tentative distance of `0` to the source node and `infinity` to all other nodes.

    @note Ported from https://github.com/michaeljgallagher/Advent-of-Code/blob/master/2023/17.py
    """
    NROWS, NCOLS = len(grid), len(grid[0])
    start, end = (0, 0), (NROWS - 1, NCOLS - 1)
    target = end
    _cost = 0
    _drdc1, _drdc2 = (0, 1), (1, 0)
    _nxt1, _nxt2 = (*start, _drdc1), (*start, _drdc2)
    # ------------------------------------------------------
    q = [(_cost, _nxt1), (_cost, _nxt2)]
    dists = defaultdict(lambda: math.inf)  # distances = {node: float('inf') for node in graph}
    predecessors = {}
    li, limit = 0, 1_000_000
    # ------------------------------------------------------
    while q and (li := li + 1) < limit:
        # time.sleep(0.00125)  # os.system(CMD_CLEAR) # print("\033[2J\033[H", end="")
        # print_visited(grid, dists)
        cur_cost, cur_node = heapq.heappop(q)
        (r, c, d) = cur_node
        if (r, c) == target:
            pretty_print_visited(grid, predecessors, start, target)
            return cur_cost
        if cur_cost > dists[r, c, d]:
            predecessors[(r, c)] = None
            continue
        # ------------------------------------------------------
        dr, dc = d
        for ndr, ndc in [(-dc, dr), (dc, -dr)]:  # [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            ncost = cur_cost
            for dist in range(1, hi + 1):
                nr, nc = r + (ndr * dist), c + (ndc * dist)
                if not (0 <= nr < NROWS and 0 <= nc < NCOLS): continue
                ncost += grid[nr][nc]
                if dist < lo: continue
                # ------------------------------------------------------
                ngbr_node = (*(nr, nc), (ndr, ndc))
                if ncost < dists[ngbr_node]:
                    dists[ngbr_node] = ncost
                    predecessors[(r, c)] = None
                    predecessors[*ngbr_node[:2]] = cur_node[:2]
                    heapq.heappush(q, (ncost, ngbr_node))
    return None


def pretty_print_visited(grid, predecessors, start, target):
    visited_grid = grid.copy()
    for k, v in predecessors.items():
        if v is not None:
            visited_grid[k[0]][k[1]] = '#'
        else:
            visited_grid[k[0]][k[1]] = '.'
    visited_grid[start[0]][start[1]] = 'A'
    visited_grid[target[0]][target[1]] = 'B'
    for r in visited_grid: print(*r)


def print_visited(grid, distances):
    for i, r in enumerate(grid):
        for j, c in enumerate(r):
            found = False
            for (rs, cs, _ds) in distances.keys():
                if (i, j) == (rs, cs):
                    found = True
                    break
            print(end=(f'#{c}' if found else f'{c:2}'))
        print()


def parse_input(data: str):
    return [list(map(int, list(r.rstrip()))) for r in data.splitlines()]


def part1(data):
    D = parse_input(data)
    p1 = solve(D, 1, 3, False)
    print(f'{p1=}')  # 102 | 1263


def part2(data):
    D = parse_input(data)
    p2 = solve(D, 4, 10, True)
    print(f'{p2=}')  # 94 | 1411


check_test(part1, part2)
check(part1, part2)
