# day13.py
from utils import *


def part1(data):
    """
    find the reflection lines in the patterns and summarize them based on
    the number of columns to the left of each vertical line of reflection
    and 100 times the number of rows above each horizontal line of reflection
    """
    reflections = parse_reflections(data)
    p1 = solve(reflections)
    print(p1)  # 405 | 37113


def part2(data):
    """
    fix a smudge in each pattern, where exactly one . or # needs to be changed
    to the opposite type to create a different valid reflection line.
    After fixing the smudge, the goal is to find the new reflection line and summarize it similarly to Part 1.

    setting tolerance to 0 in Part 2 is that, in Part 2, look for patterns where exactly
    one smudge needs to be fixed to create a different valid reflection line. By setting tolerance to 0,
    essentially state that in the corrected pattern, there should be no differences between the
    original and the reflected pattern, except for the fixed smudge.
    """
    reflections = parse_reflections(data)
    p2 = solve(reflections, for_part2=True)
    print(p2)  # 400 | 30449


def parse_reflections(data: str):
    return [strtogrid(rg) for rg in data.split('\n\n')]


def solve(reflections, for_part2=False):
    """Derived from @jonathanpaulson: https://github.com/jonathanpaulson/AdventOfCode/blob/master/2023/13.py"""
    total = 0
    tolerance = (1 if for_part2 else 0)

    for grid in reflections:
        NR, NC = len(grid), len(grid[0])

        for r in range(NR - 1):
            vertical_smudge = 0
            for dr in range(NR):
                if 0 <= (up := r - dr) < (down := r + 1 + dr) < NR:
                    vertical_smudge += sum(1 for c in range(NC) if grid[up][c] != grid[down][c])
            total += (vertical_smudge == tolerance) * (100 * (r + 1))  # 400

        for c in range(NC - 1):
            horizontal_smudge = 0
            for dc in range(NC):
                if 0 <= (left := c - dc) < (right := c + 1 + dc) < NC:
                    horizontal_smudge += sum(1 for r in range(NR) if grid[r][left] != grid[r][right])
            total += (horizontal_smudge == tolerance) * (c + 1)  # 5

    return total


# def calculate_total(reflections):
#     total = 0
#     for i, grid in enumerate(reflections, start=1):
#         ref_idx_col = get_reflection_index(grid)
#         ref_idx_row = get_reflection_index(gridtranspose(grid))
#         total += ref_idx_col if ref_idx_col is not None else 0
#         total += 100 * ref_idx_row if ref_idx_row is not None else 0
#         # TODO: find offset only. if reflected side has excess to right then do we remove it?
#         # print(ref_idx_col, ref_idx_row)
#     return total


# ----------------------------------------------------------------------------------------------------------------------

def solve_old(data: str):
    RG = [strtogrid(rg) for rg in data.split('\n\n')]
    n_rows, n_cols = len(RG[0]), len(RG[0][0])
    # assert all(len(grid) == n_rows and len(grid[0]) == n_cols
    #            for grid in RG), 'Expect reflections to have similar dimensions'
    total = 0

    for i, grid in enumerate(RG, start=1):
        # pprint(dict(G=f'R{i}', Grid=grid, n_rows=n_rows, n_cols=n_cols))
        refl_mid_cols = set()
        for r in grid:
            refection_idx = get_reflection_index(''.join(r))
            refl_mid_cols.add(refection_idx)
            # print(r, refection_idx)
        r_mid_setlist = list(refl_mid_cols)
        ref_idx_col = None
        if len(r_mid_setlist) == 1:
            ref_idx_col = r_mid_setlist[0]
        if ref_idx_col is not None:
            total += ref_idx_col
        # print(r_mid_setlist, ref_idx_col)
        refl_mid_rows = set()
        cgrid = gridtranspose(grid)
        for r in cgrid:
            refection_idx = get_reflection_index(''.join(r))
            refl_mid_rows.add(refection_idx)
            # print(r, refection_idx)
        r_mid_setlist = list(refl_mid_rows)
        ref_idx_row = None
        if len(r_mid_setlist) == 1:
            ref_idx_row = r_mid_setlist[0]
        if ref_idx_row is not None:
            total += (100 * ref_idx_row)
        # print(r_mid_setlist, ref_idx_row)

    # print(total)
    return total


def get_reflection_index(grid):
    refl_set = {find_reflection_index(''.join(row)) for row in grid}
    # pprint(dict(reflection_points=refl_set, grid=grid), width=120)
    return refl_set.pop() if len(refl_set) == 1 else None


def find_reflection_index(string: str) -> int | None:
    for i in range(1, len(string)):
        s1, s2 = string[:i], string[i:]
        reversed_s2 = s2[::-1]
        if reversed_s2 in s1:
            return i
    return None


# check_test(part1, part2)
check(part1, part2)
