# day11.py
#
# --- Day 11: Cosmic Expansion ---
#
# Expand the universe, then find the length of the shortest path between every pair of galaxies.
# What is the sum of these lengths?


from utils import *


def part1(data):
    D = data.strip()
    d = parse_data(D)
    p1 = solve(d)
    print(p1)  # 374 | 10494813


def part2(data):
    D = data.strip()
    d = parse_data(D)
    # p2 = solve(d)
    # print(p2)  # 2 | 957


def parse_data(data: str):
    # """
    # [list(map(int, line.split())) for line in data.splitlines()]
    # rows = list(map(str.rsplit, data.splitlines()))
    # grid = [list(r.strip()) for r in data.splitlines()]  # 2D grid
    # """
    return strtogrid(multiline_str=data)


class Universes:
    def __init__(self, grid):
        self.grid = grid
        self.grid_as_cols = gridtranspose(grid)
        self.symbol_galaxy = '#'
        self.symbol_empty = '.'
        self.nr = len(self.grid)
        self.nc = len(self.grid[0])

    def count_row(self, idx_row):
        return Counter(self.grid[idx_row])

    def count_transposed_col(self, idx_col):
        return Counter(self.grid_as_cols[idx_col])

    def row_has_universe(self, idx_row):
        return self.symbol_galaxy in self.count_row(idx_row=idx_row)

    def col_has_universe(self, idx_col):
        return self.symbol_galaxy in self.count_transposed_col(idx_col=idx_col)

    def get_empty_row_col(self):
        r_index = [i for i, r in enumerate(self.grid) if not self.row_has_universe(idx_row=i)]
        c_index = [i for i, r in enumerate(self.grid_as_cols) if not self.col_has_universe(idx_col=i)]
        return dict(r_index=r_index, c_index=c_index)

    def lst_galaxy_pos(self):
        gs = []
        for i, r in enumerate(self.grid):
            for j, c in enumerate(r):
                if self.is_sym_galaxy(symbol=c):
                    gs.append((i, j))
        return gs

    def is_sym_galaxy(self, symbol):
        return symbol == self.symbol_galaxy

    def is_pos_galaxy(self, x, y):
        return self.grid[x][y] == self.symbol_galaxy

    def __assign_galaxy_id(self) -> list[list]:
        empty_id = '.'  # OR 0
        universe = gridinit(rows=len(self.grid), cols=len(self.grid[0]), value=empty_id)
        ids, visited = 1, set()  # galaxy seen
        for i, r in enumerate(self.grid):
            for j, c in enumerate(r):
                if c == self.symbol_galaxy:
                    universe[i][j] = ids
                    visited.add((i, j))
                    ids += 1
        assert len(visited) == (ids - 1)
        return universe

    def expand_universe(self):
        grid_galaxy_id = self.__assign_galaxy_id()
        zero_rows, zero_cols = self.get_empty_row_col().values()
        for col in reversed(zero_cols):  # Duplicate all 'zero cols' in place
            for row in range(self.nr):
                grid_galaxy_id[row].insert(col + 1, '.')
        for row in reversed(zero_rows):  # Duplicate all 'zero rows' in place
            grid_galaxy_id.insert(row + 1, grid_galaxy_id[row][:])
        return grid_galaxy_id

    def describe(self, grid=None, with_pos=False):
        cur = grid if grid else self.grid
        if not with_pos:
            pprint(cur, indent=8, compact=False, width=120, depth=2)
        else:
            for i, r in enumerate(cur):
                # for j, c in enumerate(r): print((i, j), c, end=' ')
                for j, c in enumerate(r): print(f'{i}_{j} {repr(c)}', end=' ')
                print()


def manhattan_distance(x1, y1, x2, y2) -> int:
    return abs(x2 - x1) + abs(y2 - y1)


def solve(data):
    """
    for i, r in enumerate(U.grid):
        for j, c in enumerate(r):
            # print((i, j), (c), end=' ')
            pass
        # print()
        pass
    """
    U = Universes(data)
    universe = U.expand_universe()
    # U.describe(universe)

    galaxy_positions = []
    for i, r in enumerate(universe):
        for j, c in enumerate(r):
            if isinstance(c, int):
                galaxy_positions.append((c, (i, j)))
    # pprint(dict(galaxy_positions=galaxy_positions))

    history = {}
    visited = set()
    for id1, galaxy in galaxy_positions:
        cur = galaxy
        x1, y1 = cur
        history[id1] = 0
        for i in range(len(galaxy_positions)):
            tmp = galaxy_positions[i]
            id2, (x2, y2) = tmp
            # compared = (id1, (x1, y1, x2, y2))
            # compared = ((x1, y1), (x2, y2))
            compared = (id1, id2)
            if id1 != id2 and (id1, id2) not in visited and (id2, id1) not in visited:
                # if id1 != id2 and compared not in visited:
                visited.add(compared)
                history[id1] += manhattan_distance(x1, y1, x2, y2)
    # pprint(history)
    # pprint(visited, indent=4, width=80, compact=True)
    sum_min_dist_btw_g = sum([x for x in history.values()])

    return sum_min_dist_btw_g


profile_stats_test = 'profile_stats_check_test'
cProfile.run('check_test(part1, part2)', profile_stats_test)
stats = pstats.Stats(profile_stats_test).strip_dirs()
stats.sort_stats('cumulative')
# stats.print_stats(10)
"""
"""

profile_stats = 'profile_stats_check'
cProfile.run('check(part1, part2)', profile_stats)
stats = pstats.Stats(profile_stats).strip_dirs()
stats.sort_stats('cumulative')
stats.print_stats(10)
"""
Mon Dec 18 23:07:39 2023    profile_stats_check

         430907 function calls in 0.424 seconds

   Ordered by: cumulative time
   List reduced from 43 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.424    0.424 {built-in method builtins.exec}
        1    0.000    0.000    0.424    0.424 <string>:1(<module>)
        1    0.000    0.000    0.424    0.424 utils.py:39(check)
        1    0.011    0.011    0.423    0.423 day11.py:12(part1)
        1    0.238    0.238    0.411    0.411 day11.py:113(solve)
   101025    0.076    0.000    0.120    0.000 day11.py:109(manhattan_distance)
   202050    0.043    0.000    0.043    0.000 {built-in method builtins.abs}
   101475    0.040    0.000    0.040    0.000 {method 'add' of 'set' objects}
        1    0.000    0.000    0.007    0.007 day11.py:88(expand_universe)
    22465    0.005    0.000    0.005    0.000 {built-in method builtins.isinstance}
"""

# """
# def txt2gridmap(data: str): return list(map(list, map(str.strip, data.splitlines())))
# def txt2dgrid(data: str): return [list(line.strip()) for line in data.splitlines()]
# data_string = "\n".join(["ABCD", "EFGH", "IJKL"] * 1000)  # Repeat the sample data for a larger dataset
# time_map = timeit.timeit(lambda: txt2gridmap(data_string), number=1000) # Benchmark the map version
# time_list_comp = timeit.timeit(lambda: data2Dgrid(data_string), number=1000) # Benchmark the list comprehension version
# print(f"Using map: {time_map} seconds")
# print(f"Using list comprehension: {time_list_comp} seconds")
# """
