from collections import deque
from typing import Dict, Tuple

from utils import *


def manhattan_distance(x1, y1, x2, y2) -> int | float:
    return abs(x1 - x2) + abs(y1 - y2)


def solve(grid: list[list[str]], is_part2: bool = False) -> tuple[int, int, int, int]:
    """
    #2   4  #1  #3  #4  #3  #2   3   1   1   3   2   3
    #3  #2  #1   5   4   5  #3   5   3   5   6   2   3
     3   2   5   5   2   4  #5   6   5   4   2   5   4
     3   4   4   6   5   8  #5   8   4   5   4   5   2
     4   5   4   6  #6  #5  #7   8   6   7   5   3   6
     1   4   3   8  #5   9   8   7   9   8   4   5   4
     4   4   5   7  #8  #7  #6   9   8   7   7   6   6
     3   6   3   7   8   7  #7   9   7   9   6   5   3
     4   6   5   4   9  #6  #7   9   8   6   8   8   7
     4   5   6   4   6  #7   9   9   8   6   4   5   3
     1   2   2   4   6  #8   6   8   6   5   5   6   3
     2   5   4   6   5  #4   8   8   8   7   7   3   5
     4   3   2   2   6  #7  #4  #6  #5  #5  #5  #3  #3
    155
    """
    NR, NC = len(grid), len(grid[0])
    pprint(dict(grid=grid))

    # -------------------------------------------------------------------------
    seen = set()
    start = (0, 0)
    end = (NR - 1, NC - 1)
    q: deque[tuple[int, tuple[int, int]]] = deque([(cost := 0, start)])
    counter = 0
    print(f'Initial:\t{(counter, q)=}')
    while q and counter < 33:  # 102
        cur_cost, cur = q.pop()
        print(f'{(counter, q)=}\n'f'\t{(cost, cur)=}')
        counter += 1
        tmp_q = []
        for dr, dc in (D_NSWE := {(-1, 0), (0, -1), (1, 0), (0, 1)}):
            r, c = cur
            seen.add((cost := int(grid[r][c]), (r, c)))
            nr, nc = r + dr, c + dc
            if not (0 <= nr < NR and 0 <= nc < NC):
                continue
            nxt_cost = int(grid[nr][nc])
            if (nxt_cost, (nr, nc)) in seen:
                nc_ = (nxt_cost, (nr, nc))
                if nc_ in q:
                    q.remove(nc_)
                continue
            tmp_q.append((cost := (nxt_cost + cur_cost), pos := (nr, nc)))
            # q.append((cost := (nxt_cost + cur_cost), pos := (nr, nc)))

        heuristics = [(cost := (manhattan_distance(*tmp_nxt, *end) + tmp_cost), tmp_nxt)
                      for tmp_cost, tmp_nxt in tmp_q]
        if heuristics:
            min_heuristic = sorted(heuristics, key=lambda x: x[0])[0]
            new_pos = min_heuristic[1]
            new_cost = cur_cost + int(grid[new_pos[0]][new_pos[1]])
            q.append((cost := new_cost, (new_pos)))

        q = sorted(q, key=lambda x: x[0], reverse=True)
        if cur == end:
            break

    print(seen)
    lst_seen = list(seen)

    total_heat_loss = 0
    for i, r in enumerate(grid):
        for j, c in enumerate(r):
            found = []
            for s in lst_seen:
                cost, (row, col) = s
                if row == i and col == j:
                    print(end=f'#{c:2} ')
                    found.append((i, j))
                    total_heat_loss += int(c)
                    break
            if (i, j) not in found:
                print(end=f' {c:2} ')
        print()
    print(total_heat_loss)
    return total_heat_loss


def count_multiple_visited(seen: tuple[int, int, int, int]) -> int:
    return len(energized := {pos := s[:2] for s in seen})


def part1(data: str):
    D = [list(r.rstrip()) for r in data.rstrip().splitlines()]
    p1 = solve(D)
    print(f'{p1=}')  # 102 | ?


def part2(data: str):
    D = [list(r.rstrip()) for r in data.rstrip().splitlines()]
    p2 = solve(D, is_part2=True)
    print(f'{p2=}')  # ? | ?


check_test(part1, part2)
# check(part1, part2)
