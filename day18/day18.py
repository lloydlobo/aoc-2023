from utils import *

DIRECTIONS = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}


def solve(plans, is_part2):
    global DIRECTIONS
    path, cur = [(0, 0)], (0, 0)

    for direction, distance, _ in plans:
        dr, dc = DIRECTIONS[direction]
        prev, cur = cur, (cur[0] + dr * distance, cur[1] + dc * distance)
        path.append(cur)

    # Pick's theorem:
    # I: number of interior lattice points
    # B: number of lattice points on the boundary
    # A = I + (B // 2) - 1
    area = shoelace_formula(path)
    n_outer_cells = sum([x[1] for x in plans])
    n_inner_cells = area - (n_outer_cells // 2) + 1
    # print(f'{area,n_inner_cells,n_outer_cells=}')  # 42.0 | ?
    # area,n_inner_cells,n_outer_cells=(42.0, 24.0, 38) # p1=62.0
    # area,n_inner_cells,n_outer_cells=(31945.0, 30401.0, 3090) # p1=33491.0
    return n_inner_cells + n_outer_cells


def shoelace_formula(vertices):
    """
    # vertices: list of tuples [(x1, y1), (x2, y2), ..., (xn, yn)]
    Thanks to tip from the [community](https://www.reddit.com/r/adventofcode/comments/18l0qtr/2023_day_18_solutions/)
    """
    n = len(vertices)
    area = 0.5 * abs(sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(vertices, vertices[1:] + [vertices[0]])))
    return area


def parse_input(data):
    return [(direction, int(distance), hex_color[1:-1]) for direction, distance, hex_color in (
        tuple(row.rstrip().split()) for row in data.splitlines()
    ) if direction in DIRECTIONS.keys() and distance.isdigit() and len(hex_color) == 9 and hex_color[1] == '#']


def part1(data):
    D = parse_input(data)
    p1 = solve(D, False)
    print(f'{p1=}')  # 62 | 33491


def part2(data):
    if _DEBUG_SOLVE := True:
        return
    D = parse_input(data)
    p2 = solve(D, False)
    print(f'{p2=}')


# Check tests and main execution
check_test(part1, part2)
check(part1, part2)

#
# def _visit_enclosed_cells(grid, enclosed_start):
#     global DIRECTIONS
#     directions = DIRECTIONS.values()
#     NROWS, NCOLS = len(grid), len(grid[0])
#     seen, pq = {enclosed_start}, [(0, enclosed_start)]
#     li, limit = 0, 1_000_000_000
#
#     while pq and (li := li + 1) < limit:
#         dist, cur_cell = heapq.heappop(pq)
#         for dr, dc in directions:
#             nr, nc = cur_cell[0] + dr, cur_cell[1] + dc
#             if 0 <= nr < NROWS and 0 <= nc < NCOLS and (nr, nc) not in seen and grid[nr][nc] == '.':
#                 seen.add((nr, nc))
#                 heapq.heappush(pq, (dist + 1, (nr, nc)))
#
#     _grid_cpy = [['0' if (i, j) in seen else c for j, c in enumerate(r)] for i, r in enumerate(grid)]
#     return seen  # print(*map(' '.join, grid_cpy), sep='\n')
#
#
# def _compute_total_cells(directions, grid, n_edge_cells, ncols, nrows, path):
#     # cells = compute_total_cells(DIRECTIONS, grid, n_edge_cells, ncols, nrows, path)
#     entry_point, incr = None, 0
#     # print(*map(' '.join, grid), sep='\n')
#
#     while not entry_point and incr < ncols:
#         npt = path[0]
#         for ng_dr, ng_dc in directions.values():
#             ngr, ngc = npt[0] + ng_dr * incr, npt[1] + ng_dc * incr
#             count_empty_cells, count_edges_ngbr = 0, 0
#
#             for xdr, ydr in directions.values():
#                 xnr, ynr = ngr + xdr, ngc + ydr
#                 if 0 <= xnr < nrows and 0 <= ynr < ncols:
#                     if grid[xnr][ynr] == '.':
#                         count_empty_cells += 1
#                         npt = (xnr, ynr)
#                     else:
#                         count_edges_ngbr += 1
#
#             if count_empty_cells > 3 and ngc != 0:
#                 entry_point = (ngr, ngc)
#                 break
#
#         incr += 1
#
#     # print(f'{entry_point=}')
#     visited_cells = visit_enclosed_cells(grid, entry_point)
#     # print(len(visited_cells), n_edge_cells)
#     # print(*map(' '.join, grid), sep='\n')
#     cells = len(visited_cells) + n_edge_cells
#     return cells
#
