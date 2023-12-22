# day14.py

from utils import *


class TileKind(Enum):
    EMPTY_SPACE = '.'  # 0
    CUBE_ROCK = '#'  # 1
    ROUNDED_ROCK = 'O'  # 2


def find_tile_pos_grid(board, tile_kind):
    rows, cols = len(board), len(board[0])
    return [(i, j) for i in range(rows) for j in range(cols)
            if board[i][j] == tile_kind]  # all rocks in grid (x,y)


def find_tile_pos_row(board, row, tile_kind):
    cols = len(board[0])
    return [(row, col) for col in range(cols)
            if board[row][col] == tile_kind]  # all rocks in cur row (x,y)


def move_rock_north(board, row, col, step=1):
    """Swaps the rock at the position (row, col) with the space at (row - step, col)."""
    board[row][col], board[row - step][col] = board[row - step][col], board[row][col]


def move_rock_south(board, row, col, step=1):
    """Swaps the rock at the position (row, col) with the space at (row + step, col)."""
    board[row][col], board[row + step][col] = board[row + step][col], board[row][col]


def move_rock_west(board, row, col, step=1):
    """Swaps the rock at the position (row, col) with the space at (row, col - step)."""
    board[row][col], board[row][col - step] = board[row][col - step], board[row][col]


def move_rock_east(board, row, col, step=1):
    """Swaps the rock at the position (row, col) with the space at (row, col + step)."""
    board[row][col], board[row][col + step] = board[row][col + step], board[row][col]


def tilt_anti_clockwise(board, cycles):
    NR, NC = len(board), len(board[0])

    cycle = 0
    seen = set()
    seen_map = dict()
    repeating_grid = None
    repeating_key = None
    repeated_count = 0

    directions = ['north', 'west', 'south', 'east']
    for _ in range(cycles):
        for direction in directions:
            range_by_direction = range(NR) if direction in ['north', 'west'] else range(NR - 1, -1, -1)

            for row in range_by_direction:
                movables = find_tile_pos_row(board, row, TileKind.ROUNDED_ROCK.value)
                movables_ = movables if direction in ['north', 'west'] else reversed(movables)

                for x, y in movables_:
                    assert board[x][y] == TileKind.ROUNDED_ROCK.value

                    match direction:
                        case 'north':
                            while x > 0 and board[x - 1][y] == TileKind.EMPTY_SPACE.value:
                                move_rock_north(board, x, y)
                                x -= 1
                        case 'west':
                            while y > 0 and board[x][y - 1] == TileKind.EMPTY_SPACE.value:
                                move_rock_west(board, x, y)
                                y -= 1
                        case 'south':
                            nx = x + 1
                            while nx < NR and board[nx][y] == TileKind.EMPTY_SPACE.value:
                                move_rock_south(board, nx - 1, y)
                                nx += 1
                        case 'east':
                            ny = y + 1
                            while ny < NC and board[x][ny] == TileKind.EMPTY_SPACE.value:
                                move_rock_east(board, x, ny - 1)
                                ny += 1
                        case _:
                            raise ValueError('Unrecognized direction given to function')
            # dbg(direction)
            # dbg(board)

        cycle += 1

        seen_map[cycle] = copy.deepcopy(board)  # without copy: errors output as 69, instead of desired 64

        if str(board) in seen:
            repeating_grid = board
            repeating_key = cycle  # 10

            if repeated_count == 2:
                break
            repeated_count += 1

        seen.add(str(board))

    n_seen_map = len(seen_map)
    seen_key = next((k for k, v in seen_map.items() if v == repeating_grid), None)
    frequency_cycle = n_seen_map - seen_key
    equivalent_cycle = cycles % frequency_cycle

    return seen_map[equivalent_cycle]  # 64


def solve(board, for_part2=False):
    grid = copy.deepcopy(board)
    if for_part2:
        grid = tilt_anti_clockwise(board=copy.deepcopy(board), cycles=1_000_000_000)
        # return [r.count(TileKind.ROUNDED_ROCK.value) for r in grid]
    # else:
    if not for_part2:
        for row in range(len(grid)):
            movables = find_tile_pos_row(grid, row, TileKind.ROUNDED_ROCK.value)
            for x, y in movables:
                while x > 0 and grid[x - 1][y] == TileKind.EMPTY_SPACE.value:
                    move_rock_north(board=grid, row=x, col=y)
                    x -= 1

    return [r.count(TileKind.ROUNDED_ROCK.value) for r in grid]


def calculate_load(rock_counts):
    return sum((num_row + 1) * rock_count
               for num_row, rock_count in enumerate(reversed(rock_counts)))


# ----------------------------------------------------------------------------------------------------------------------

def dbg(x):
    pprint(x, width=120)


# ----------------------------------------------------------------------------------------------------------------------

def part1(data):
    """
    """
    grid = strtogrid(data)
    rock_counts = solve(grid, for_part2=False)
    p1 = calculate_load(rock_counts)
    print(f'{p1=}')  # 136 | 109638


def part2(data):
    """
    """
    grid = strtogrid(data)
    rock_counts = solve(grid, for_part2=True)
    p2 = calculate_load(rock_counts)
    print(f'{p2=}')  # 64 | ?


check_test(part1, part2)
check(part1, part2)
