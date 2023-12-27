from utils import *


class Heading(Enum):
    N, W, S, E = (-1, 0), (0, -1), (1, 0), (0, 1)

    @classmethod
    def from_tuple(cls, drdc):
        for h in cls:
            if h.value == drdc:
                return h
        raise ValueError('Invalid tuple value for Heading enum')


class Position:
    def __init__(self, r, c, direction):
        self.r, self.c = r, c
        self.d = direction

    def coords(self):
        return (self.r, self.c)

    def heading(self):
        return self.d

    def astuple(self):
        return (self.r, self.c), (self.d.value[0], self.d.value[1])

    def peek_next_pos(self):
        return self.r + self.d.value[0], self.c + self.d.value[1]

    @staticmethod
    def is_valid(nr, nc, NR, NC):
        return 0 <= nr < NR and 0 <= nc < NC


def solve(grid: list[list[str]], is_part2: bool = False) -> tuple[int, int, int, int]:
    NR, NC = len(grid), len(grid[0])
    # -------------------------------------------------------------------------
    P: Position = Position(0, -1, Heading.E)
    q = deque([P])
    seen = set()
    # -------------------------------------------------------------------------
    while q:
        # ---------------------------------------------------------------------
        P = q.pop()
        # ---------------------------------------------------------------------
        (r, c), (dr, dc) = P.astuple()
        nr, nc = r + dr, c + dc  # P.peek_next_pos()
        # ---------------------------------------------------------------------
        if (nr, nc, dr, dc) in seen:
            continue
        if not Position.is_valid(nr, nc, NR, NC):
            continue
        # ---------------------------------------------------------------------
        seen.add((nr, nc, dr, dc))
        # ---------------------------------------------------------------------
        tile = grid[nr][nc]
        match tile:
            case '.':
                pass
            case '\\':
                dr, dc = dc, dr  # (0,1) E -> / (1,0) S
            case '/':
                dr, dc = -dc, -dr  # (0,1) E -> / (-1,0) N
            case '|':
                if dc:  # travelling horizontally
                    dr, dc = 1, 0  # signal original beam to head north
                q.append(Position(nr, nc, Heading.from_tuple((-1, 0))))  # Create new beam to head south
            case '-':
                if dr:  # travelling vertically
                    dr, dc = 0, -1  # signal original beam to head west
                q.append(Position(nr, nc, Heading.from_tuple((0, 1))))  # Create new beam to head east
            case _:
                raise ValueError(f'Unexpected tile/cell value: {tile}')
        # ---------------------------------------------------------------------
        q.append(Position(nr, nc, Heading.from_tuple((dr, dc))))
        # ---------------------------------------------------------------------
    return seen


def count_multiple_visited(seen: tuple[int, int, int, int]) -> int:
    return len(energized := {pos := s[:2] for s in seen})


def part1(data: str):
    D = [list(r.rstrip()) for r in data.rstrip().splitlines()]
    solved = solve(D)
    p1 = count_multiple_visited(solved)
    print(f'{p1=}')  # 46 | 7728


def part2(data: str):
    D = [list(r.rstrip()) for r in data.rstrip().splitlines()]
    solved = solve(D)
    p2 = count_multiple_visited(solved)
    print(f'{p2=}')  # 51 | ?


check_test(part1, part2)
check(part1, part2)
