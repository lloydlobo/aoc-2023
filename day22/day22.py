from utils import *


class Brick:
    def __init__(self, sxyz: Tuple[int, int, int], exyz: Tuple[int, int, int], brick_id: int):
        self.sx, self.sy, self.sz = sxyz
        self.ex, self.ey, self.ez = exyz
        self._id = brick_id

    @property
    @lru_cache(None)
    def range_xy(self):
        return [
            (x, y)
            for x in range(self.sx, self.ex + 1)
            for y in range(self.sy, self.ey + 1)
        ]

    @property
    @lru_cache(None)
    def z_height(self):
        return (self.ez - self.sz) + 1

    @property
    def as_start(self):
        return self.sx, self.sy, self.sz

    @property
    def as_end(self):
        return self.ex, self.ey, self.ez

    def describe(self):
        return dict(_id=self._id, start=self.as_start, end=self.as_end, range_xy=self.range_xy,
                    z_height=self.z_height)

    @lru_cache(None)
    def __lt__(self, other: Union['Brick', Any]):
        return self.z_height < other.z_height

    @lru_cache(None)
    def __gt__(self, other: Union['Brick', Any]):
        return self.z_height > other.z_height

    @staticmethod
    def print_list(lst: List[Union['Brick', Any]]):
        pprint([brick.describe() for brick in lst], compact=True, width=111)


def solve(data: str, is_part2=False):
    """Thanks to many suggestions fram /r/adventofcode megathread participants"""
    TCoords = Tuple[int, int, int]
    TBrick = Tuple[TCoords, ...]

    bricks: List[TBrick] = [
        tuple(tuple(map(int, xyz.split(','))) for xyz in line.rstrip().split('~'))
        for line in data.rstrip().splitlines()
    ]

    brick_objects: list[Brick] = [Brick(start, end, i) for i, (start, end) in enumerate(bricks)]
    brick_objects.sort()
    n_bricks = len(brick_objects)
    assert all(isinstance(b, Brick) for b in brick_objects)
    assert all(b.z_height >= 1 for b in brick_objects)

    # Brick.print_list(brick_objects)

    def is_solid(brcset, x, y, z):
        return z == 0 or (x, y, z) in brcset

    def brcfall(brck_objects: list[Brick]):
        assert all(b.z_height >= 1 for b in brck_objects)
        fell = False
        new_brcks: List[Brick] = []
        brckset: set[TCoords] = {(x, y, b.ez) for b in brck_objects for x, y in b.range_xy}
        for b in brck_objects:
            supports = any(is_solid(brckset, x, y, (b.sz - 1)) for x, y in b.range_xy)
            if not supports:
                fell = True
                new_brcks.append(Brick((b.sx, b.sy, b.sz - 1), (b.ex, b.ey, b.ez - 1), b._id))
            else:
                new_brcks.append(b)
        return fell, new_brcks

    assert all(isinstance(b, Brick) for b in brick_objects)
    assert all(b.z_height >= 1 for b in brick_objects)
    fell = True
    initial_fell_count = 0

    while fell:
        initial_fell_count += 1
        fell, brick_objects = brcfall(brck_objects=brick_objects)
        brick_objects.sort()

    assert all(isinstance(b, Brick) for b in brick_objects)
    assert all(b.z_height >= 1 for b in brick_objects)
    assert initial_fell_count == 5 if n_bricks == 7 else True
    # Brick.print_list(brick_objects)

    pprint(dict(initial_fell_count=initial_fell_count))

    # intersect `&`, exclusion `^`
    brick_objcpy = copy.deepcopy(brick_objects)
    assert all(isinstance(b, Brick) for b in brick_objcpy)
    assert all(b.z_height >= 1 for b in brick_objcpy)
    # Brick.print_list(brick_objcpy)

    # ------------------------------------------------------------------------------------------------------------------
    # record safe bricks

    safe_bricks_count = 0
    print(f'{n_bricks =}')

    for i, b_disintegrated in enumerate(brick_objcpy):
        tmp = copy.deepcopy(brick_objcpy)
        assert tmp.pop(i)._id == b_disintegrated._id

        tmp_fell, tmp_fell_count = True, 0

        while tmp_fell:
            tmp_fell_count += 1  # including disintegrated
            tmp_fell, tmp = brcfall(brck_objects=tmp)
            tmp.sort()

        if tmp_fell_count == 1:
            safe_bricks_count += 1
        # pprint(dict(brick=b_disintegrated.describe(), safe_bricks_count=safe_bricks_count))

    assert ((safe_bricks_count == 5) if (initial_fell_count == 5 and n_bricks == 7) else True)
    pprint(dict(initial_fell_count=initial_fell_count, safe_bricks_count=safe_bricks_count, n_bricks=n_bricks))

    return safe_bricks_count


def part1(data: str):
    p1 = solve(data)  # {'initial_fell_count': 189, 'n_bricks': 1370, 'safe_bricks_count': 463}
    print(f'{p1 = }')  # 5 | 463


def part2(data: str):
    return
    p2 = solve(data, True)
    print(f'{p2 = }')


check_test(part1, part2)
check(part1, part2)
