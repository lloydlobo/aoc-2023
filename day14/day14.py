from utils import *


class TileKind(Enum):
    EMPTY = '.'
    BARRIER = '#'
    MOVABLE = 'O'


class Direction(Enum):
    NORTH = 'north'
    WEST = 'west'
    SOUTH = 'south'
    EAST = 'east'


class TiltingGrid:
    def __init__(self, board):
        self.grid = copy.deepcopy(board)
        self.directions = [Direction.NORTH, Direction.WEST, Direction.SOUTH, Direction.EAST]
        self.NR, self.NC = len(self.grid), len(self.grid[0])

    def find_tile_pos_row(self, row, tile_kind):
        return [(row, col) for col in range(self.NC) if self.grid[row][col] == tile_kind]

    def find_tile_pos_grid(self, tile_kind):
        return [(i, j) for i in range(self.NR) for j in range(self.NC)
                if self.grid[i][j] == tile_kind]

    def tilt_north(self, r, c, step=1):
        self.grid[r][c], self.grid[r - step][c] = self.grid[r - step][c], self.grid[r][c]

    def tilt_south(self, r, c, step=1):
        self.grid[r][c], self.grid[r + step][c] = self.grid[r + step][c], self.grid[r][c]

    def tilt_west(self, r, c, step=1):
        self.grid[r][c], self.grid[r][c - step] = self.grid[r][c - step], self.grid[r][c]

    def tilt_east(self, r, c, step=1):
        self.grid[r][c], self.grid[r][c + step] = self.grid[r][c + step], self.grid[r][c]

    def mutate_movable_to_direction(self, direction: Direction, x: int, y: int, step=1):
        dst = TileKind.EMPTY.value
        match direction:
            case Direction.NORTH:
                while x > 0 and self.grid[x - 1][y] == dst:
                    self.tilt_north(x, y, step)
                    x -= 1
            case Direction.WEST:
                while y > 0 and self.grid[x][y - 1] == dst:
                    self.tilt_west(x, y, step)
                    y -= 1
            case Direction.SOUTH:
                nx = x + 1
                while nx < self.NR and self.grid[nx][y] == dst:
                    self.tilt_south(nx - 1, y, step)
                    nx += 1
            case Direction.EAST:
                ny = y + 1
                while ny < self.NC and self.grid[x][ny] == dst:
                    self.tilt_east(x, ny - 1, step)
                    ny += 1
            case _:
                raise ValueError(f'Unrecognized direction {repr(direction)}')

    def tilt(self, cycles, clockwise=False):
        """
        NOTE: The trick it seems was to let it iterate for longer repeation of matching patterns.
               When the length of the seen set stabilized, it's a safe bet to return the
               expected tilted grid after rolling grid 1_000_000_000 times (or 1_000_000_000 * 4 cycles.)
               {'cycle_stats': {0: {'cycle': 143, 'cycle_len': 143, 'seen_len': 142},
                                ...
                                150: {'cycle': 293, 'cycle_len': 293, 'seen_len': 142}}}
               equivalent_cycle=160
        """
        D = self.directions if not clockwise else self.directions[::-1]
        ds_north_west = [Direction.NORTH, Direction.WEST]
        seen, seen_map = set(), dict()
        rep_grid, rep_key = None, None
        n_expected_cycle = 150
        cycle_stats = dict()
        cycle, rep_count = 0, 0
        for _ in range(cycles):
            for d in D:
                for row in range(self.NR) if d in ds_north_west else range(self.NR - 1, -1, -1):
                    movables = self.find_tile_pos_row(row, TileKind.MOVABLE.value)
                    for x, y in movables if d in ds_north_west else reversed(movables):
                        self.mutate_movable_to_direction(d, x, y)
            cycle += 1
            seen_map[cycle] = copy.deepcopy(self.grid)
            if str(self.grid) in seen:
                rep_grid, rep_key = self.grid, cycle
                cycle_stats[rep_count] = dict(cycle_len=len(seen_map), cycle=cycle, seen_len=len(seen))
                if rep_count >= n_expected_cycle:
                    break  # Loop at least twice to see if it is a legitimate repeating cycle
                rep_count += 1
            seen.add(f'{self.grid}')
        seen_key = next((k for k, v in seen_map.items() if v == rep_grid), None)
        frequency_cycle = len(seen_map) - seen_key
        equivalent_cycle = (cycles // 4 % frequency_cycle)
        # pprint(dict(cycle_stats=cycle_stats))
        # print(f'{equivalent_cycle=}')
        return seen_map[equivalent_cycle]


# ----------------------------------------------------------------------------------------------------------------------

def solve(tg: TiltingGrid, for_part2=False):
    if for_part2:  # Each cycle roll the grid 4 times (N W S E)
        grid = tg.tilt(cycles=(1_000_000_000 * 4), clockwise=False)
        return [r.count(TileKind.MOVABLE.value) for r in grid]

    for row in range(len(tg.grid)):
        movables = tg.find_tile_pos_row(row, TileKind.MOVABLE.value)
        for x, y in movables:
            while x > 0 and tg.grid[x - 1][y] == TileKind.EMPTY.value:
                tg.tilt_north(x, y)
                x -= 1
    return [r.count(TileKind.MOVABLE.value) for r in tg.grid]


def calculate_load(rock_counts):
    return sum((num_row + 1) * rock_count
               for num_row, rock_count in enumerate(reversed(rock_counts)))


# ----------------------------------------------------------------------------------------------------------------------


def part1(data):
    grid = strtogrid(copy.deepcopy(data))
    tg = TiltingGrid(grid)
    rock_counts = solve(tg, for_part2=False)
    p1 = calculate_load(rock_counts)
    print(f'{p1=}')  # 136 | 109638


def part2(data):
    grid = strtogrid(copy.deepcopy(data))
    tg = TiltingGrid(grid)
    rock_counts = solve(tg, for_part2=True)
    p2 = calculate_load(rock_counts)
    print(f'{p2=}')  # 64 | 102657


# ----------------------------------------------------------------------------------------------------------------------

check_test(part1, part2)
check(part1, part2)
