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
    gshape = (len(grid), len(grid[0]))  # (n_rows, n_cols)
    directions = {(-1, 0), (0, -1), (1, 0), (0, 1)}

    cur_visits: set[tuple[int, int]] = {start}
    reachable_cells: set[tuple[int, int]] = set()

    def wrap_row(nr, row_size):
        return ((nr % row_size) + row_size) % row_size

    def wrap_col(nc, col_size):
        return ((nc % col_size) + col_size) % col_size

    def wrap_coordinate(coord, size):
        return ((coord % size) + size) % size

    for step in range(n_steps + 1):
        nxt_visits = set()

        while cur_visits:
            r, c = cur_visits.pop()
            visited.add((r, c))

            if (step & 1) == visit_odd_steps:  # assert 0 == 0 and 1 == 1
                reachable_cells.add((r, c))

            for (dr, dc) in directions:
                nr, nc = r + dr, c + dc
                if is_part2:
                    if grid[wrap_coordinate(nr, gshape[0])][wrap_coordinate(nc, gshape[1])] == '#':
                        visited.add((nr, nc))
                        continue
                    nxt_visits.add((nr, nc))
                else:
                    if not (0 <= nr < gshape[0] and 0 <= nc < gshape[1]):
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
    # Define expected results for different step counts
    expected_results = {
        6   : 16,
        10  : 50,
        50  : 1594,
        100 : 6536,
        500 : 167004,
        1000: 668697,
        5000: 16733044,
    }

    # Check results for specified step counts
    for n_steps, expected_result in expected_results.items():
        print(f'{n_steps, expected_result = }')
        result = solve(data, n_steps=n_steps, is_part2=True)
        assert result == expected_result, f'For {n_steps} steps, expect {expected_result}. Got {result}'

    # Final check for the provided step count (commented for now)
    # p2 = solve(data, n_steps=50, is_part2=True)  # 16733044 | ?
    # p2 = solve(data, n_steps=26501365, is_part2=True) # ?
    print(f'{p2 = }')


check_test(part1, part2)
# check(part1, part2)

# def imagine_infinite_grid_map(data: str):
#     grid = [list(r.rstrip()) for r in data.splitlines()]
#     shape = (len(grid), len(grid[0]))
#
#     print(f'  {" ".join([s.rjust(2, "O") for s in (list(map(str, range(shape[0]))))])}', sep=' ')
#
#     directions = {(-1, 0), (0, -1), (1, 0), (0, 1)}
#
#     for i, r in enumerate(grid):
#         print(str(i).rjust(2, 'O'), end=' ')
#
#         for j, c in enumerate(r):
#             print(end=f'{c}  ')
#         print()
#
#     # wrap_around
#     wrap_row = lambda delta_r: ((delta_r % shape[0]) + shape[0]) % shape[0]
#     wrap_col = lambda delta_c: ((delta_c % shape[1]) + shape[1]) % shape[1]
#
#     for i in range(1, shape[0] + 1):
#         row, col = wrap_row(-i), wrap_col(-i)
#         shape_i_r, shape_i_c = shape[0] - i, shape[1] - i
#         assert row == shape[0] - i, f'Expect {shape_i_r}. Got {row}.'
#         assert col == shape[1] - i, f'Expect {shape_i_c}. Got {col}.'
#
#     for r in range(shape[0]):
#         for c in range(shape[1]):
#             for (dr, dc) in directions:
#                 nr, nc = r + dr, c + dc
#                 if not (0 <= nr < shape[0]):
#                     nr = wrap_row(nr)
#                 if not (0 <= nc < shape[1]):
#                     nc = wrap_col(nc)
#                 assert 0 <= nr < shape[0] and 0 <= nc < shape[1], f'Expect new positions wrapped in grid bounds'
#                 # print(f'{nr, nc} ', end='')
#             # print()
#             # print(f'{(nr, nc)}', end='  ')
#
