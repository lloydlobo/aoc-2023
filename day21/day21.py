from utils import *


def solve(data: str, n_steps: int, is_part2: bool = False):
    """
    Ported from https://github.com/jmd-dk/advent-of-code/blob/main/2023/solution/21/solve.py
    Explanation: https://www.reddit.com/r/adventofcode/comments/18nevo3/comment/kee6vn6/

    > Part one is solved using breadth-first search with no back-tracking. Any positions reached in an even number of
    > steps (≤ 64) counts toward the total number of reachable positions within the 64 total steps (if a position is
    > reached in say 60 steps (even), the remaining 4 steps can be spent taking a single step back and then forth 4/2 =
    > 2 times).

    The function uses breadth-first search without back-tracking to traverse the grid. Cells are added to the
    `reachable_cells` set under two conditions:

        1. If the step number is even, all visited cells are implicitly deemed reachable and included in the set.
        2. If the step number is odd, cells are explicitly included based on the condition
           `(step & 1) == visitable_on_odd_steps`. This condition selectively adds cells based on odd or even steps.

    Flexible back-and-forth movements within the remaining steps, ensuring an inclusive definition of "reachable"
    positions.
    """
    grid = [list(r.rstrip()) for r in data.splitlines()]
    start = next((i, j) for i, r in enumerate(grid) for j, c in enumerate(r) if c == 'S')
    visited = set((i, j) for i, r in enumerate(grid) for j, c in enumerate(r) if c == '#')
    visit_odd_steps = n_steps & 1  # >>> assert (2 & 1 == 0 and 3 & 1 == 1) # n_steps % 2 == 1
    grid_shape = (len(grid), len(grid[0]))  # (n_rows, n_cols)
    directions = {(-1, 0), (0, -1), (1, 0), (0, 1)}

    cur_visits: set[tuple[int, int]] = {start}
    reachable_cells: set[tuple[int, int]] = set()

    for step in range(n_steps + 1):
        nxt_visits = set()

        while cur_visits:
            r, c = cur_visits.pop()
            visited.add((r, c))

            if (step & 1) == visit_odd_steps:  # assert 0 == 0 and 1 == 1
                reachable_cells.add((r, c))

            for (dr, dc) in directions:
                nr, nc = r + dr, c + dc
                if not (0 <= nr < grid_shape[0] and 0 <= nc < grid_shape[1]):
                    continue
                if (nr, nc) in visited:
                    continue
                nxt_visits.add((nr, nc))

        cur_visits = nxt_visits

    return len(reachable_cells)


def part1(data: str):
    p1 = solve(data, n_steps=64)
    print(f'{p1 = }')  # 16 | 3660


def part2(data: str):
    p2 = solve(data, n_steps=64, is_part2=True)
    print(f'{p2 = }')


check_test(part1, part2)
check(part1, part2)
