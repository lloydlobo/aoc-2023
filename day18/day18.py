from utils import *


def solve(plans: List[Tuple[str, int, str]], is_part2: bool) -> int:
    DIRECTIONS = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
    visited = set()
    path = [(0, 0)]
    cur = (0, 0)
    for direction, distance, _ in plans:
        dr, dc = DIRECTIONS[direction]
        prev, cur = cur, (cur[0] + dr * distance, cur[1] + dc * distance)
        visited.add(((prev, cur), distance, (dr, dc)))
        path.append(cur)
    max_x_coord = max(path, key=lambda coord: coord[0])[0] + 1
    max_y_coord = max(path, key=lambda coord: coord[1])[1] + 1
    nrows, ncols = max_x_coord, max_y_coord
    grid = [['#' if (r, c) in path else '.' for c in range(ncols)] for r in range(nrows)]
    for direction, distance, _ in plans:
        dr, dc = DIRECTIONS[direction]
        prev, cur = cur, (cur[0] + (dr * distance), cur[1] + (dc * distance))
        for i in range(1, distance + 1):
            nr, nc = prev[0] + dr * i, prev[1] + dc * i
            if 0 <= nr < nrows and 0 <= nc < ncols:
                grid[nr][nc] = '#'
    pprint(grid, compact=True, width=nrows * 4)  # edges
    lava_meter_cube_edges = sum(row.count('#') for row in grid)  # 38
    total_volume = 0
    for i, r in enumerate(grid):
        lo, hi = 0, ncols - 1
        found_lo, found_hi = False, False
        while lo < hi:
            if not found_lo:
                if grid[i][lo] == '#':
                    found_lo = True
                else:
                    lo += 1
            if not found_hi:
                if grid[i][hi] == '#':
                    found_hi = True
                else:
                    hi -= 1
            if found_lo and found_hi:
                if _DEBUG_FIXME := False and '#' in r:
                    count_edges = r.count('#')  # Row can have odd number of `#` but `#` at lo and hi ,ust be pairs
                    assert count_edges % 2 == 0, f'Expect pair of edges. Got {count_edges=}'
                break
        for x in range(lo, hi + 1):
            grid[i][x] = '#'
            total_volume += 1
    lava_meter_cube_new = sum(row.count('#') for row in grid)  # 38
    print(lava_meter_cube_new)
    pprint(grid, compact=True, width=2000)  # edges + inner filled

    # pprint(dict(grid=grid, lava_meter_cube=lava_meter_cube_edges, lava_meter_cube_inner=lava_meter_cube_inner))
    return total_volume


# ('visited,path=({(((7, 0), (5, 0)), 2, (-1, 0)), (((2, 2), (2, 0)), 2, (0, '
#  '-1)), (((5, 0), (5, 2)), 2, (0, 1)), (((9, 1), (7, 1)), 2, (-1, 0)), (((0, '
#  '6), (5, 6)), 5, (1, 0)), (((7, 4), (7, 6)), 2, (0, 1)), (((9, 6), (9, 1)), '
#  '5, (0, -1)), (((7, 6), (9, 6)), 2, (1, 0)), (((5, 2), (2, 2)), 3, (-1, 0)), '
#  '(((2, 0), (0, 0)), 2, (-1, 0)), (((5, 6), (5, 4)), 2, (0, -1)), (((0, 0), '
#  '(0, 6)), 6, (0, 1)), (((5, 4), (7, 4)), 2, (1, 0)), (((7, 1), (7, 0)), 1, '
#  '(0, -1))}, [(0, 0), (0, 6), (5, 6), (5, 4), (7, 4), (7, 6), (9, 6), (9, 1), '
#  '(7, 1), (7, 0), (5, 0), (5, 2), (2, 2), (2, 0), (0, 0)])')
# max_pos=(9, 6)
# [['#', '#', '#', '#', '#', '#', '#'],
#  ['#', '.', '.', '.', '.', '.', '#'],
#  ['#', '#', '#', '.', '.', '.', '#'],
#  ['.', '.', '#', '.', '.', '.', '#'],
#  ['.', '.', '#', '.', '.', '.', '#'],
#  ['#', '#', '#', '.', '#', '#', '#'],
#  ['#', '.', '.', '.', '#', '.', '.'],
#  ['#', '#', '.', '.', '#', '#', '#'],
#  ['.', '#', '.', '.', '.', '.', '#'],
#  ['.', '#', '#', '#', '#', '#', '#']]
# p1=None


def parse_input(data: str) -> list[tuple[str, int, str]]:
    return [(direction, int(distance), hex_color[1:-1]) for direction, distance, hex_color in (
        tuple(row.rstrip().split()) for row in data.splitlines()
    ) if direction in {'U', 'D', 'L', 'R'} and distance.isdigit() and len(hex_color) == 9 and hex_color[1] == '#']


def part1(data):
    D = parse_input(data)
    p1 = solve(D, False)
    print(f'{p1=}')  # 62 | ?


def part2(data):
    if _DEBUG_SOLVE := True:
        return
    D = parse_input(data)
    p1 = solve(D, False)
    print(f'{p2=}')  # ? | ?


check_test(part1, part2)
# check(part1, part2)

"""
The digger starts in a 1 meter cube hole in the ground. They then dig the specified number of meters up (U), down (D), left (L), or right (R), clearing full 1 meter cubes as they go. The directions are given as seen from above, so if "up" were north, then "right" would be east, and so on. Each trench is also listed with the color that the edge of the trench should be painted as an RGB hexadecimal color code.

When viewed from above, the above example dig plan would result in the following loop of trench (#) having been dug out from otherwise ground-level terrain (.):

#######
#.....#
###...#
..#...#
..#...#
###.###
#...#..
##..###
.#....#
.######
At this point, the trench could contain 38 cubic meters of lava. However, this is just the edge of the lagoon; the next step is to dig out the interior so that it is one meter deep as well:

#######
#######
#######
..#####
..#####
#######
#####..
#######
.######
.######

how many cubic meters of lava could it hold?
"""
