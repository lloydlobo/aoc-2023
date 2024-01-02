from utils import *


def show_visited(grid, instances):
    """Visualize visited cells in a grid."""
    # pad_k = 1
    pad_k = 1
    pad = max(len(str(cell)) for row in grid for cell in row) + pad_k  # space needed for padding

    # print column indices
    filler = " " * pad
    print(filler, end="")
    for i, _ in enumerate(grid[0]):
        print(f"{i:>{pad}}", end=f'{filler}')
    print()

    # print rows with visited cells marked
    for i, row in enumerate(grid):
        print(f"{i:>{pad}}", end=f'{filler}')
        for j, cell in enumerate(row):
            found = False
            for instance_id, (r, c, _dr, _dc) in instances:
                if (i, j) == (r, c):
                    print(f'{str(instance_id).rjust(pad, "0")}', end=f'{filler}')
                    found = True
                    break
            if not found:
                print(str(cell).rjust(pad), end=f'{filler}')
        print()


def solve(d, steps_taken, is_p2):
    start_sym, target_sym, garden_plot_sym, rock_sym = 'S', 'O', '.', '#'  # 'S' is also a GARDEN_PLOT
    directions = {'N': (-1, 0), 'W': (0, -1), 'S': (1, 0), 'E': (0, 1)}

    grid = [list(r.rstrip()) for r in d.splitlines()]

    n_rows, n_cols = len(grid), len(grid[0])
    # assert (n_rows, n_cols) == (11, 11)

    start_pos = next((r.index(start_sym), i) for i, r in enumerate(grid) if (start_sym) in r)
    # assert start_pos == (5, 5)

    in_bounds = lambda i_, j_: 0 <= i_ < n_rows and 0 <= j_ < n_cols

    # q = [(0, (*start_pos, *(0, 1)))]
    q = [(0, (*start_pos, *d)) for d in directions.values()]
    print(f'{q=}')
    seen = set()
    instances = []  # Store instances for each steps
    prevs = set()
    # for _, citem in q:
    #     prevs.add(citem)

    prev_cost_counter = 0
    cur_cost_counter = 0
    first_4 = 4

    q_limit, max_q = 0, (n_rows * n_cols) ** 4  # Prevent infinite loops
    while q and (q_limit := q_limit + 1) < max_q:
        ccost, c = q.pop(0)

        # if (ccost + 1) == 6:  # 6 steps == 16 plots covered. cost==0 is start_pos cost==5
        #     break
        (cr, cc, cdr, cdc) = c

        # todo: if c in seen is not allowing to travel back freely to prev positions
        #   this could allow to propogate and not traverse traditionally like in BFS
        if c[0:2] == start_pos:
            if first_4 > 0:
                first_4 -= 1
        if c in prevs and first_4 > 0:
            continue

        for i, (inst_id, *rest) in enumerate(instances):
            if inst_id + 1 == ccost:
                instances.pop(i)  # remove previous location history
                prevs.add(c)

        seen.add(c)
        instances.append((ccost, c))

        if cur_cost_counter != prev_cost_counter:
            filtered_instances = []
            for x, y in instances:
                if x != prev_cost_counter:
                    filtered_instances.append((x, y))
            if False:
                for x, _ in filtered_instances:
                    assert x == (prev_cost_counter - 1), f'Got {x}. Expected {prev_cost_counter}'
                    assert x == cur_cost_counter  # 6 steps -> x = 6
            show_visited(grid, filtered_instances)
            print(f'{prev_cost_counter,cur_cost_counter=}')  # if steps_taken == 6 => (7,6)
            if cur_cost_counter == 6:
                _garden_plots_reached = len(set([pos[0:2] for _, pos in filtered_instances]))
                # if we consider all possibilities, also based on direction
                # _garden_plots_reached = len(set([pos for _, pos in filtered_instances]))
                assert _garden_plots_reached == 16, f'Got {_garden_plots_reached}. Ecpected 16'
            if cur_cost_counter == steps_taken:
                garden_plots_reached = len(set([pos[0:2] for _, pos in filtered_instances]))
                return garden_plots_reached
            # clear_screen_ansi()
            cur_cost_counter += 1
            # time.sleep(0.85)

        for d, (dr, dc) in directions.items():
            nr, nc = cr + dr, cc + dc
            if not in_bounds(nr, nc): continue
            if (cur_plot := grid[nr][nc]) == rock_sym: continue
            assert cur_plot in {garden_plot_sym, start_sym, target_sym}
            nxt = ((ncost := ccost + 1), (nr, nc, dr, dc))
            q.append(nxt)
            # if nxt not in q:
            #     q.append(nxt)

        prev_cost_counter += 1 if ccost != prev_cost_counter else 0
        # pprint(dict(q=q))
        q = sorted(q)  # Prioritize lower-cost nodes

    return None


def visuzlize_visited(ccost, cur_cost_counter, grid, instances, prev_cost_counter):
    prev_cost_counter += 1 if ccost != prev_cost_counter else 0
    if cur_cost_counter != prev_cost_counter:
        time.sleep(0.5)
        show_visited(grid, [x[1][0:2] for x in instances])
        cur_cost_counter += 1
        clear_screen_ansi()


def part1(data: str):
    p1 = solve(data, steps_taken=6, is_p2=False)  # 16
    # p1 = solve(data, steps_taken=64, is_p2=False)
    print(f'{p1=}')  # 64 | ?


def part2(data):
    return
    p2 = solve(D, is_p2=False)
    print(f'{p2=}')  # ? | ?


check_test(part1, part2)
# check(part1, part2)


# ----------------------------------------------------------------------------------------------------------------------
