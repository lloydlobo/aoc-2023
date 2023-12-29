from utils import *

DIRECTIONS = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}


def visit_enclosed_cells(grid, enclosed_start):
    global DIRECTIONS
    directions = DIRECTIONS.values()
    NROWS, NCOLS = len(grid), len(grid[0])
    seen, zero_counter, pq = {enclosed_start}, 0, [(0, enclosed_start)]
    li, limit = 0, 1_000_000_000

    while pq and (li := li + 1) < limit:
        dist, cur_cell = heapq.heappop(pq)
        for dr, dc in directions:
            nr, nc = cur_cell[0] + dr, cur_cell[1] + dc
            if 0 <= nr < NROWS and 0 <= nc < NCOLS and (nr, nc) not in seen and grid[nr][nc] == '.':
                seen.add((nr, nc))
                heapq.heappush(pq, (dist + 1, (nr, nc)))

    print(f'{li=}')
    grid_cpy = [['0' if (i, j) in seen else c for j, c in enumerate(r)] for i, r in enumerate(grid)]
    print(*map(' '.join, grid_cpy), sep='\n')
    print(f'{zero_counter=}')
    return seen


def solve(plans, is_part2):
    global DIRECTIONS
    visited, path, cur = set(), [(0, 0)], (0, 0)

    for direction, distance, _ in plans:
        dr, dc = DIRECTIONS[direction]
        prev, cur = cur, (cur[0] + dr * distance, cur[1] + dc * distance)
        visited.add(((prev, cur), distance, (dr, dc)))
        path.append(cur)

    max_x_coord, max_y_coord = max(path, key=lambda coord: coord[0])[0] + 1, max(path, key=lambda coord: coord[1])[
        1] + 1
    nrows, ncols = max_x_coord, max_y_coord
    grid = [['#' if (r, c) in path else '.' for c in range(ncols)] for r in range(nrows)]
    print(*map(' '.join, grid), sep='\n')

    for direction, distance, _ in plans:
        dr, dc = DIRECTIONS[direction]
        prev, cur = cur, (cur[0] + (dr * distance), cur[1] + (dc * distance))
        for i in range(1, distance + 1):
            nr, nc = prev[0] + dr * i, prev[1] + dc * i
            if 0 <= nr < nrows and 0 <= nc < ncols:
                grid[nr][nc] = '#'

    print(*map(' '.join, grid), sep='\n')
    n_edge_cells = sum(r.count('#') for r in grid)
    cells = compute_total_cells(DIRECTIONS, grid, n_edge_cells, ncols, nrows, path)
    return cells


def compute_total_cells(directions, grid, n_edge_cells, ncols, nrows, path):
    entry_point, incr = None, 0

    while not entry_point and incr < ncols:
        npt = path[0]
        for ng_dr, ng_dc in directions.values():
            ngr, ngc = npt[0] + ng_dr * incr, npt[1] + ng_dc * incr
            count_empty_cells, count_edges_ngbr = 0, 0

            for xdr, ydr in directions.values():
                xnr, ynr = ngr + xdr, ngc + ydr
                if 0 <= xnr < nrows and 0 <= ynr < ncols:
                    if grid[xnr][ynr] == '.':
                        count_empty_cells += 1
                        npt = (xnr, ynr)
                    else:
                        count_edges_ngbr += 1

            if count_empty_cells > 3 and ngc != 0:
                entry_point = (ngr, ngc)
                break

        incr += 1

    print(f'{entry_point=}')
    visited_cells = visit_enclosed_cells(grid, entry_point)
    print(len(visited_cells), n_edge_cells)
    print(*map(' '.join, grid), sep='\n')
    cells = len(visited_cells) + n_edge_cells
    return cells


def parse_input(data):
    return [(direction, int(distance), hex_color[1:-1]) for direction, distance, hex_color in (
        tuple(row.rstrip().split()) for row in data.splitlines()
    ) if direction in {'U', 'D', 'L', 'R'} and distance.isdigit() and len(hex_color) == 9 and hex_color[1] == '#']


def part1(data):
    D = parse_input(data)
    p1 = solve(D, False)
    print(f'{p1=}')


def part2(data):
    if _DEBUG_SOLVE := True:
        return
    D = parse_input(data)
    p2 = solve(D, False)
    print(f'{p2=}')


# Check tests and main execution
check_test(part1, part2)
check(part1, part2)
