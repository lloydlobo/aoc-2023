from utils import *


def show_visited(grid, instances):
    """Visualize visited cells in a grid."""
    indent = 0  # 1
    pad = max(len(str(cell)) for row in grid for cell in row) + indent  # space needed for padding

    # print column indices
    filler = " " * pad
    print(filler, end="")
    for i, _ in enumerate(grid[0]):
        print(f"{i:>{pad}}", end=f'{filler}')
    print()

    # print rows with visited cells marked
    total = 0
    for i, row in enumerate(grid):
        print(f"{i:>{pad}}", end=f'{filler}')
        for j, cell in enumerate(row):
            found = False
            for step, (r, c, _dr, _dc) in instances:
                if (i, j) == (r, c):
                    print(f'{str(step).rjust(pad, "0")}', end=f'{filler}')
                    total += 1
                    found = True
                    break
            if not found:
                print(str(cell).rjust(pad), end=f'{filler}')
        print()
    print(f'{total, len(instances), len(set(instances))=}')
    return total


def solve(d, steps_taken, is_p2):
    start_sym, rock_sym = 'S', '#'
    directions = {'N': (-1, 0), 'W': (0, -1), 'S': (1, 0), 'E': (0, 1)}

    grid = [list(r.rstrip()) for r in d.splitlines()]
    n_rows, n_cols = len(grid), len(grid[0])

    rock_positions = {(i, j) for i, r in enumerate(grid) for j, c in enumerate(r) if c == rock_sym}
    start_pos = next((r.index(start_sym), i) for i, r in enumerate(grid) if start_sym in r)

    q = [(0, (*start_pos, *d)) for d in directions.values()]
    instances, prev_cost_counter, cur_cost_counter = [], 0, 0

    distances = defaultdict(dict)

    q_limit, max_q = 0, (n_rows * n_cols) ** 4
    seen = set()

    while q and (q_limit := q_limit + 1) < max_q:
        ccost, c = heapq.heappop(q)
        instances.append((ccost, c))

        for i, (inst_id, _) in enumerate(instances):
            if inst_id < ccost:
                prev = instances.pop(i)
                seen.add(prev[1][:2])

        if cur_cost_counter == steps_taken and cur_cost_counter != prev_cost_counter:
            filtered_instances = [(x, y) for x, y in instances if x != prev_cost_counter]
            total = show_visited(grid, filtered_instances)
            len1 = len(set(pos[0:2] for _, pos in filtered_instances))

            all_nodes = set()
            for k, vals in distances.items():
                nodes = set()
                for vals_k, vals_v in vals.items():
                    if vals_v and steps_taken - 1 < vals_v[0] < steps_taken + 1:
                        nodes.add((vals_v[0], vals_v[1][:2]))
                if nodes:
                    all_nodes.update(nodes)

            len2 = len(all_nodes)
            pprint(dict(all_nodes=all_nodes, n_all_nodes=len2))
            print(f'{len1=}, {len2=}, {total=}')
            assert len1 == len2
            assert total == len1
            return len2

        if cur_cost_counter != prev_cost_counter:
            cur_cost_counter += 1
            if __DEBUG := not False:
                filtered_instances = [(x, y) for x, y in instances if x != prev_cost_counter]
                total = show_visited(grid, filtered_instances)
                print(f'{prev_cost_counter=}, {cur_cost_counter=}')
                pprint(dict(distances=distances))
        elif ccost != prev_cost_counter:
            prev_cost_counter += 1

        ngbrs = set()
        for d, (dr, dc) in directions.items():
            nr, nc = c[0] + dr, c[1] + dc
            if not (0 <= nr < n_rows and 0 <= nc < n_cols) or (nr, nc) in rock_positions:
                continue
            if nr == 0 or nr == n_rows - 1:
                continue
            nxt = (ccost + 1, (nr, nc, dr, dc))
            c_ = (c[0], c[1])
            if not (c_[0] == 0 or c_[0] == n_rows - 1):
                distances[c_][ccost, (dr, dc)] = nxt
            ngbrs.add(nxt)

        for n in ngbrs:
            if n[1][:2] not in seen:
                heapq.heappush(q, n)
                seen.add(n[1][:2])
        seen.clear()

    return None


# check_test(part1, part2)
# check(part1, part2)
def part1(data: str):
    p1 = solve(data, steps_taken=6, is_p2=False)  # 16 | 43
    p1 = solve(data, steps_taken=11, is_p2=False)
    # p1 = solve(data, steps_taken=16, is_p2=False)  # 64 | ?
    print(f'{p1=}')


def part2(data):
    return
    p2 = solve(data, steps_taken=6, is_p2=True)
    print(f'{p2=}')


check_test(part1, part2)
# check(part1, part2)  # if steps == 6 -> 114

"""
        dr, dc = d
        for ndr, ndc in [(-dc, dr), (dc, -dr)]:  # [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            ncost = cur_cost
            for dist in range(1, hi + 1):
                nr, nc = r + (ndr * dist), c + (ndc * dist)
                if not (0 <= nr < NROWS and 0 <= nc < NCOLS): continue
                ncost += grid[nr][nc]
                if dist < lo: continue
                # ------------------------------------------------------
                ngbr_node = (*(nr, nc), (ndr, ndc))
                if ncost < dists[ngbr_node]:
                    dists[ngbr_node] = ncost
                    predecessors[(r, c)] = None
                    predecessors[*ngbr_node[:2]] = cur_node[:2]
                    heapq.heappush(q, (ncost, ngbr_node))
"""
