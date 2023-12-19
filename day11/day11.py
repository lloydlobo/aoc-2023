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
    # print(p2)  # 8410 | ?


def solve(data):
    U = Universe(data, '#', '.')
    univ = U.expand_universe()  # U.describe(universe)
    galaxy_positions = [(c, Position(i, j)) for i, r in enumerate(univ) for j, c in enumerate(r) if isinstance(c, int)]
    history, visited = defaultdict(int), set()
    for id1, cur in galaxy_positions:
        history[id1]  # history[id1] = 0
        for id2, other in galaxy_positions:
            compared: tuple[int, int] = tuple(sorted((id1, id2)))
            if (id1 != id2) and (compared not in visited):
                distance = U.manhattan_distance(cur.x, cur.y, other.x, other.y)
                history[id1] += distance
                visited.add(compared)
    return sum(history.values())  # sum min dist btw galaxies


def parse_data(data: str):
    return strtogrid(multiline_str=data)


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Universe:
    def __init__(self, grid, symbol_galaxy, symbol_empty):
        self.grid = grid
        self.grid_as_cols = gridtranspose(grid)
        self.symbol_galaxy = symbol_galaxy
        self.symbol_empty = symbol_empty
        self.n_rows = len(self.grid)
        self.n_cols = len(self.grid[0])

    def describe(self, grid=None, with_pos=False):
        cur = grid if grid else self.grid
        if not with_pos:
            pprint(cur, indent=8, compact=False, width=120, depth=2)
        else:
            for i, r in enumerate(cur):
                # for j, c in enumerate(r): print((i, j), c, end=' ')
                for j, c in enumerate(r): print(f'{i}_{j} {repr(c)}', end=' ')
                print()

    def count_rows(self, idx_row):
        return Counter(self.grid[idx_row])

    def count_transposed_cols(self, idx_col):
        return Counter(self.grid_as_cols[idx_col])

    def row_has_galaxy(self, idx_row):
        return self.symbol_galaxy in self.count_rows(idx_row)

    def col_has_galaxy(self, idx_col):
        return self.symbol_galaxy in self.count_transposed_cols(idx_col)

    def get_empty_row_col(self) -> dict[str, list]:
        idx_rows = [i for i in range(self.n_rows) if not self.row_has_galaxy(i)]
        idx_cols = [i for i in range(self.n_cols) if not self.col_has_galaxy(i)]
        return dict(idx_rows=idx_rows, idx_cols=idx_cols)

    def get_galaxy_positions(self):
        gs = []
        for i, r in enumerate(self.grid):
            for j, c in enumerate(r):
                if self.is_sym_galaxy(symbol=c):
                    # gpos=Position(i,j)
                    # print(gpos)
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
            for row in range(self.n_rows):
                grid_galaxy_id[row].insert(col + 1, self.symbol_empty)

        for row in reversed(zero_rows):  # Duplicate all 'zero rows' in place
            grid_galaxy_id.insert(row + 1, grid_galaxy_id[row][:])

        return grid_galaxy_id

    @staticmethod
    def manhattan_distance(x1, y1, x2, y2) -> int:
        return abs(x2 - x1) + abs(y2 - y1)


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
