# day14.py

from utils import *


class TileKind(Enum):
    EMPTY_SPACE = '.'  # 0
    CUBE_ROCK = '#'  # 1
    ROUNDED_ROCK = 'O'  # 2


def solve(grid, for_part2=False):
    def find_movables(board, row, tile_kind):
        return [(row, col) for col in range(len(board[0])) if board[row][col] == tile_kind]

    def move_rock_up(board, row, col):
        board[row][col], board[row - 1][col] = board[row - 1][col], board[row][col]

    for row in range(len(grid)):
        movables = find_movables(grid, row, TileKind.ROUNDED_ROCK.value)
        for r, c in movables:
            while r > 0 and grid[r - 1][c] == TileKind.EMPTY_SPACE.value:
                move_rock_up(grid, r, c)
                r -= 1
    rock_counts = [row.count(TileKind.ROUNDED_ROCK.value) for row in grid]
    return rock_counts


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
    rock_counts = solve(grid)
    p1 = calculate_load(rock_counts)
    print(f'{p1=}')  # 136 | 109638


def part2(data):
    """
    """
    if False:
        grid = strtogrid(data)
        p2 = solve(grid, True)
        print(p2)  # ? | ?


check_test(part1, part2)
check(part1, part2)
