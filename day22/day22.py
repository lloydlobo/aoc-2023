from utils import *


# Function to parse the input data and extract brick coordinates
def parse_data_line(line):
    coords = line.split('~')
    start = list(map(int, coords[0].split(',')))
    end = list(map(int, coords[1].split(',')))
    return start, end


# ----------------------------------------------------------------------------------------------------------------------

def collect_cube_xyz(brck):
    cubes = brck.keys()
    xs, ys, zs = [], [], []

    for c in cubes:
        xs.append(c[0])
        ys.append(c[1])
        zs.append(c[2])

    return cubes, xs, ys, zs


def get_air_brcks(brcks, occupied_cubes):
    free_brcks = {}

    for line, brick in brcks.items():
        if all(c[2] not in {0, 1} and (c[0], c[1], c[2] - 1) not in occupied_cubes for c in brick.keys()):
            free_brcks[line] = True
        else:
            cubes, xs, ys, zs = collect_cube_xyz(brick)
            if not (all(i == xs[0] for i in xs) and all(i == ys[0] for i in ys)) or all(i == zs[0] for i in zs):
                continue

            btm_z_pos = min(cubes, key=lambda cube: cube[2])
            if btm_z_pos[2] in {0, 1}:
                continue

            occup_coords = set((pos[0], pos[1], pos[2]) for pos in occupied_cubes if
                               ((pos[0], pos[1], pos[2] - 1) not in occupied_cubes))
            # assert len(occup_coords) < len(occupied_cubes)  # 16, 20

            if (btm_z_pos[0], btm_z_pos[1], btm_z_pos[2] - 1) not in occup_coords:
                free_brcks[line] = True

    return free_brcks


def sift_bricks(air_instances, bricks):
    # assert all(air_instances.values())
    bcpy = copy.deepcopy(bricks)  # essential

    for instance, in_air in air_instances.items():
        bcpy[instance] = {
            (x, y, z - 1): True
            for (x, y, z) in bcpy[instance] if z > 1
        }

    return bcpy


@lru_cache(maxsize=None)
def collect_brick_from_cubes_coords(x1, x2, y1, y2, z1, z2):
    return {
        (x, y, z): True
        for z in range(min(z1, z2), max(z1, z2) + 1)
        for y in range(min(y1, y2), max(y1, y2) + 1)
        for x in range(min(x1, x2), max(x1, x2) + 1)
    }


def update_bricks(input_data):
    """A brick is a sequence of cubes. One cube without conjoined neighbours in xy plane is also a brick"""
    occupied_cubes = set()
    bricks = {}

    for line in input_data.splitlines():
        (x1, y1, z1), (x2, y2, z2) = parse_data_line(line)
        brick = collect_brick_from_cubes_coords(x1, x2, y1, y2, z1, z2)
        bricks[line] = brick
        occupied_cubes.update(brick)

    _dbg_initial_bricks = copy.deepcopy(bricks)

    prev = copy.deepcopy(bricks)
    li, limit = 0, min(400, len(bricks) * 2)
    n_bricks_mid = len(bricks) // 2

    while True and (li := li + 1) < limit:
        tmp, new_occupied_cubes = prev, set()

        for line, cubes in tmp.items():
            cubes_lst = list(cubes.keys())
            (x1, y1, z1), (x2, y2, z2) = cubes_lst[0], cubes_lst[-1]
            brick = collect_brick_from_cubes_coords(x1, x2, y1, y2, z1, z2)
            tmp[line] = brick
            new_occupied_cubes.update(brick)

        tmp = sift_bricks(get_air_brcks(tmp, new_occupied_cubes), tmp)
        n_after_air = len(get_air_brcks(tmp, new_occupied_cubes))
        print(f'{li, n_after_air =}')

        if n_after_air == 0 or li > limit:
            bricks, occupied_cubes = tmp, new_occupied_cubes
            break

        prev = tmp
        # ... end of while loop

    if _FLAG_FIXME := False:
        assert len(get_air_brcks(bricks, occupied_cubes)) == 0
    pprint(dict(bricks=bricks, li=li, initial_bricks=_dbg_initial_bricks), compact=True, width=120)  # after

    safe_bricks = set()

    counter = 0

    seen = set()

    for brick_id, brick_cubes in copy.deepcopy(bricks).items():
        counter += 1
        if brick_id in seen:
            continue
        temp_bricks = copy.deepcopy(bricks)
        temp_bricks.pop(brick_id)
        seen.add(brick_id)

        new_occupied_cubes = set()
        # new_occupied_cubes = set(pos for brick in temp_bricks.values() for pos in brick)

        for line, cubes in temp_bricks.items():
            cubes_lst = list(cubes.keys())
            start, end = cubes_lst[0], cubes_lst[-1]
            (x1, y1, z1), (x2, y2, z2) = start, end
            brick = collect_brick_from_cubes_coords(x1, x2, y1, y2, z1, z2)
            temp_bricks[line] = brick
            new_occupied_cubes.update(brick)

        air_instances_before = get_air_brcks(temp_bricks, new_occupied_cubes)
        temp_bricks = sift_bricks(air_instances_before, temp_bricks)
        air_instances_after = get_air_brcks(temp_bricks, new_occupied_cubes)
        n_after_air = len(air_instances_after)
        print(f'{counter,n_after_air,n_bricks_mid, brick_id = }')

        if n_after_air == 0 or counter > 400:
            safe_bricks.add(brick_id)

        if counter > 400:
            continue

    pprint(dict(safe_bricks=list(safe_bricks), original_bricks=list(bricks.keys())))
    """
    {'original_bricks': ['1,0,1~1,2,1',
                     '0,0,2~2,0,2',
                     '0,2,3~2,2,3',
                     '0,0,4~0,2,4',
                     '2,0,5~2,2,5',
                     '0,1,6~2,1,6',
                     '1,1,8~1,1,9'],
     'safe_bricks': ['0,0,4~0,2,4',
                     '0,0,2~2,0,2',
                     '0,2,3~2,2,3',
                     '1,1,8~1,1,9',
                     '2,0,5~2,2,5']}
    """
    n_safe_bricks = len(safe_bricks)
    if _FLAG_FIXME := False:
        assert n_safe_bricks == 5, f'Expected 5. Got {len(safe_bricks)}'

    return n_safe_bricks


# update_bricks(open('testinput.txt').read())

update_bricks(open('input.txt').read())


# ----------------------------------------------------------------------------------------------------------------------


def solve(data: str, is_part2: bool = False):
    """
    1,0,1~1,2,1
    0,0,2~2,0,2
    0,2,3~2,2,3
    0,0,4~0,2,4
    2,0,5~2,2,5
    0,1,6~2,1,6
    1,1,8~1,1,9

    A line like 2,2,2~2,2,2 means that both ends of the brick are at the same coordinate - in other words,
    that the brick is a single cube.

    Lines like 0,0,10~1,0,10 or 0,0,10~0,1,10 both represent bricks that are two cubes in volume, both oriented
    horizontally. The first brick extends in the x direction, while the second brick extends in the y direction.
    """
    bricks = {
        i: tuple(tuple(map(int, pos.split(','))) for pos in (line.rstrip().split('~')))
        for i, line in enumerate(data.splitlines())
    }
    n_bricks = len(bricks)
    assert n_bricks == 7
    pprint(bricks)

    def coords_to_lwh(coords1, coords2):
        (x1, y1, z1), (x2, y2, z2) = coords1, coords2
        l, w, h = abs(x2 - x1), abs(y2 - y1), abs(z2 - z1)
        return l, w, h

    pprint(dict(bricks=bricks))
    for k, brick in bricks.items():
        (x1, y1, z1), (x2, y2, z2) = brick
        lwh = coords_to_lwh((x1, y1, z1), (x2, y2, z2))
        lwhplus1 = tuple(val + 1 for val in lwh)
        lwh_plus1_prod = math.prod(lwhplus1)

        print(f'{k, brick, lwh, lwhplus1, lwh_plus1_prod}')
        """
        (0, ((1, 0, 1), (1, 2, 1)), (0, 2, 0), (1, 3, 1), 3)
        (1, ((0, 0, 2), (2, 0, 2)), (2, 0, 0), (3, 1, 1), 3)
        (2, ((0, 2, 3), (2, 2, 3)), (2, 0, 0), (3, 1, 1), 3)
        (3, ((0, 0, 4), (0, 2, 4)), (0, 2, 0), (1, 3, 1), 3)
        (4, ((2, 0, 5), (2, 2, 5)), (0, 2, 0), (1, 3, 1), 3)
        (5, ((0, 1, 6), (2, 1, 6)), (2, 0, 0), (3, 1, 1), 3)
        (6, ((1, 1, 8), (1, 1, 9)), (0, 0, 1), (1, 1, 2), 2)
        """
    grid = [[' ' for _ in range(3)] for _ in range(n_bricks)]

    show_brick_side(bricks, n_bricks, side=(0, 2))  # x,z
    show_brick_side(bricks, n_bricks, side=(1, 2))  # y,z
    # show_brick_side(bricks, n_bricks, side=(0, 1))  # x,y

    return None


def show_brick_side(bricks, n_bricks, side):
    col = 'x' if side[0] == 0 else ('y' if side[0] == 1 else 'z')
    row = 'z' if side[1] == 2 else ('y' if side[1] == 1 else 'x')
    print(f' {col} ')
    print(''.join([str(j) for j in range(0, 3)]))
    for i, brick in reversed(bricks.items()):
        b1, b2 = brick
        print(f'{b1[side[0]], b1[side[1]], b2[side[0]], b2[side[1]]}', end='')  # x=0 y=1 z=2
        print(f'  {str(i).rjust(1)}', end=(f'  {row}\n' if i == (n_bricks // 2) else '\n'))


def part1(data: str):
    p1 = solve(data)
    print(f'{p1 = }')  # 16 | 3660


def part2(data: str):
    p2 = solve(data, is_part2=True)  # 16733044 | ?
    print(f'{p2 = }')


# check_test(part1, part2)
# check(part1, part2)

def bench_solve():
    global data_string
    data_string = open('testinput.txt').read()
    time_v1 = timeit.timeit(lambda: solve(data_string), number=1000)
    print(f"Time for solve_v1: {time_v1} seconds")


if _FLAG_BENCH := False:
    bench_solve()

# ----------------------------------------------------------------------------------------------------------------------

import matplotlib.pyplot as plt  # from mpl_toolkits.mplot3d import Axes3D

# Read the data from your input
"""
Positions in between start and end:
    pos = (1, 1, 1)
    pos = (1, 0, 2)
    pos = (1, 2, 3)
    pos = (0, 1, 4)
    pos = (2, 1, 5)
    pos = (1, 1, 6)
    pos = None # since (1,1,8)->(1,1,9) is just 1 cube
"""
data = [
    "1,0,1~1,2,1",
    "0,0,2~2,0,2",
    "0,2,3~2,2,3",
    "0,0,4~0,2,4",
    "2,0,5~2,2,5",
    "0,1,6~2,1,6",
    "1,1,8~1,1,9"
]


def plot_3d_bricks(input_data):
    """
    The x, y, and z lists represent the coordinates of the five vertices of a rectangular prism (a brick) in 3D
    space. Each pair of values in x, y, and z corresponds to a vertex of the brick. The vertices are ordered in such
    a way that they form a closed loop, defining the edges of the rectangular prism.

    To clarify further, each list (e.g., x) contains the x-coordinates of the five vertices, and similarly for y and
    z. This is a mistake in the visualization of the brick and may not accurately represent the structure of a brick
    in 3D space. If you want to accurately represent the brick's structure, you should use the coordinates of the
    eight vertices of the brick.
    """
    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plot_properties = dict(color=None and 'g', marker='.', linestyle='-', linewidth=10 * 1.5)  # 'go--'

    # Plot each brick as a cuboid in 3D space
    for line in input_data:
        # Extracting the coordinates of each brick
        start, end = parse_data_line(line)  # vv  as a 5 vertex prism
        # Creating coordinates for plotting a line segment in 3D space
        x = [start[0], end[0]]
        y = [start[1], end[1]]
        z = [start[2], end[2]]
        ax.plot(x, y, z, **plot_properties)

    # Set labels for axes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # plt.gca().axis('equal')
    plt.savefig('day21_bricks_3d')
    plt.show(block=False)


def old_solve_last_part():
    # One by one pick a brick.
    # 1. Pseudo disintegrate a brick or Eliminate it for the current simulation.
    # 2. Figure out bricks that won't fall further down if the current brick is disintegrated
    disintegrated_bricks = set()
    q = deque((k, v) for k, v in copy.deepcopy(bricks).items())
    safe_bricks = []
    while q:
        bricks_cpy = copy.deepcopy(bricks)
        cur = q.pop()
        cur_id, cur_cubes = cur
        if cur_id not in disintegrated_bricks:
            assert cur_id in bricks_cpy, f'Expect to disintegrate a brick once. Repeated id for brick {cur_id}'
        disintegrated_bricks.add(cur_id)
        bricks_cpy: dict
        bricks_cpy.pop(cur_id)
        new_bricks = {}
        new_occupied_cubes = set()
        assert cur_id not in bricks_cpy
        for line in bricks_cpy.keys():
            assert line != cur_id
            (x1, y1, z1), (x2, y2, z2) = parse_data_line(line)
            brick = collect_brick_from_cubes_coords(x1, x2, y1, y2, z1, z2)
            new_bricks[line] = brick
            new_occupied_cubes.update(brick)
        assert cur_id not in new_bricks
        pprint(dict(disintegrated_brick=(cur), new_bricks=new_bricks))
        b_in_air_before = get_air_brcks(new_bricks, new_occupied_cubes)
        # pprint(b_in_air_before)
        # if len(b_in_air_before) == 0:
        #     safe_bricks.append(cur_id)
        sift_bricks(air_instances=(b_in_air_before), bricks=new_bricks)
        b_in_air_after = get_air_brcks(new_bricks, new_occupied_cubes)
        if len(b_in_air_after) == 0:
            safe_bricks.append(cur_id)
    pprint(dict(safe_bricks=safe_bricks, original_bricks=list(bricks.keys())))
    n_safe_bricks = len(safe_bricks)
    assert len(set(safe_bricks)) == n_safe_bricks
    assert n_safe_bricks == 5, f'Expected 5. Got {n_safe_bricks}'


def checker(data):
    occupied = {}
    bricks = {}
    for line in data.splitlines():
        parts = parse_data_line(line)
        lo, hi = parts
        brick = defaultdict(dict)
        for z in range(min(lo[2], hi[2]), max(lo[2], hi[2]) + 1):
            for y in range(min(lo[1], hi[1]), max(lo[1], hi[1]) + 1):
                for x in range(min(lo[0], hi[0]), max(lo[0], hi[0]) + 1):
                    occupied[(x, y, z)] = True
                    brick[line][(x, y, z)] = True
                    # brick[(tuple(lo), tuple(hi))][(x, y, z)] = True
                    # print(x, y, z)
        # print(parts)
        bricks[line] = brick
    # pprint(bricks)
    # pprint(occupied, width=350, compact=True)
    bricks_in_air = []
    for pos in occupied:
        x, y, z = pos
        if (x, y, z - 1) not in occupied:
            bricks_in_air.append(pos)
    brick_air_instances = {}
    for line, brick in bricks.items():
        print(brick, 'brick')
        in_air = True
        for k, v in brick.items():
            for pos in v.keys():
                x, y, z = pos
                if (x, y, z - 1) not in occupied:
                    continue
                in_air = False
                break
        if in_air:
            brick_air_instances[line] = True

    # pprint(bricks_in_air, width=80, compact=True)
    pprint(brick_air_instances)
    # print(brick_air_instances)


if _FLAG_DEBUG := False:
    checker(open('testinput.txt').read())


def plot_polar_positions(input_data):
    D = copy.deepcopy(input_data)
    obj_coords = {i: parse_data_line(line) for i, line in enumerate(D)}
    coords_values = [val for vals in obj_coords.values() for val in vals]

    sx, sy, sz = map(set, zip(*coords_values))
    xyz_ranges = [range(min(s), max(s) + 1) for s in [sx, sy, sz]]  # x: (min,max), y: (min,max), z: (min,max)

    world_coords = {(x, y, z): False for z in xyz_ranges[2] for y in xyz_ranges[1] for x in xyz_ranges[0]}

    count_given, count_derived = 0, 0

    seen = set()
    # pprint(world_coords, compact=True) # Before
    for xyzs in obj_coords.values():
        for xyz in xyzs:
            t = tuple(xyz)
            if t not in seen:
                world_coords[t] = True
                count_given += 1
            else:
                seen.add(t)

        assert len(xyzs) == 2
        (x1, y1, z1), (x2, y2, z2) = xyzs[0], xyzs[1]
        dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
        # Create ranges that go from x1 to x2, y1 to y2, and z1 to z2 (inclusive)
        ranges_btw_start_end = [range(abs(dx) + 1), range(abs(dy) + 1), range(abs(dz) + 1)]
        # Define a step for each coordinate
        step_x = 1 if dx >= 0 else -1
        step_y = 1 if dy >= 0 else -1
        step_z = 1 if dz >= 0 else -1

        for dir, dists in enumerate(ranges_btw_start_end):
            ncoords = []
            for dist in dists:  # if dists is range(1): i==dist will be 0
                nx, ny, nz = x1, y1, z1
                match dir:
                    case 0:
                        nx += dist * step_x
                    case 1:
                        ny += dist * step_y
                    case 2:
                        nz += dist * step_z
                ncoords.append((nx, ny, nz))
            for pos in ncoords:
                if pos in seen: continue
                if world_coords[pos]: continue
                print(f'{pos=}')
                world_coords[pos] = True
                seen.add(pos)
                count_derived += 1

    # pprint(world_coords, compact=True)  # After
    # print(f'{count_given,count_derived=}')  # (14,6)
    assert count_given == 14 and count_derived == 6
    # Visualize world_coords with a 3D scatter plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x, y, z = zip(*[pos for pos, occupied in world_coords.items() if occupied])
    ax.scatter(x, y, z, c='r', marker='o', label='Occupied Positions')

    # Scatter plot for unoccupied positions
    unoccupied_x, unoccupied_y, unoccupied_z = zip(*[pos for pos, occupied in world_coords.items() if not occupied])
    ax.scatter(unoccupied_x, unoccupied_y, unoccupied_z, c='g', marker='o', label='Unoccupied Positions')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()

    plt.savefig('day21_bricks_3d_scatter')
    plt.show()


def visualize(input_data):
    plot_3d_bricks(input_data)
    plot_polar_positions(input_data)


if __FLAG_DEBUG := False:
    visualize(data)
