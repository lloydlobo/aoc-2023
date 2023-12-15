# day9.py
#
# --- Day 9: Mirage Maintenance ---
from typing import List

from utils import *

"""
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""


def part1(data):
    D = data.strip()
    ldata: list[list[int]] = parse_data(D)
    diffs: list[list[list[int]]] = [consec_diffs(lst=lst) for lst in ldata]
    p1 = solve(ldata, diffs)
    print(p1)  # 114 | 1953784198


def part2(data):
    D = data.strip()
    d: list[list[int]] = parse_data(D)
    ldata = []
    for x in d:
        x.reverse()
        ldata.append(x)
    diffs: list[list[list[int]]] = [consec_diffs(lst=lst) for lst in ldata]
    p2 = solve(ldata, diffs)
    print(p2)  # 2 | 957


def consec_diffs(lst: list[int]) -> list[list[int]]:
    diffs = []
    while len(lst) > 1:
        diff = [lst[i + 1] - lst[i] for i in range(len(lst) - 1)]
        diffs.append(diff)
        lst = diff
    return diffs


def solve(ldata: list[list[int]], diffs: list[list[list[int]]]):
    """
    Analyze your OASIS report and extrapolate the next value for each history.
    What is the sum of these extrapolated values?
    """
    stats = {}

    # diff: list[list[int]]
    # idx: int
    for idx, diff in enumerate(diffs):
        stat_lst = []
        glvl, gdiff = 0, 0

        for i, d in enumerate(diff):
            diff_stasis, lvl = (d[0] - d[1]), (i + 1)
            gdiff, glvl = diff_stasis, lvl
            # str_all_0 = [1 for iint in d if iint == 0]
            # has_all_0s = (len(str_all_0) > 0 and all(str_all_0) == 1)
            is_valid: bool = len(set(d)) == 1
            statval = dict(lvl=lvl, jstr=ljoinstr(d), diff_stasis=(diff_stasis if not is_valid else d[0]))
            if is_valid:
                stat_lst.append(statval)
                break

        statval = dict(lvl=glvl, diff_stasis=gdiff, jstr=ljoinstr(diff))
        stats[idx] = stat_lst[0] if stat_lst else statval
    # pprint(stats)

    D_JOIN = join_head_diffs(diffs, ldata)
    derived_ancestors = []

    for ikey, (key, val) in enumerate(D_JOIN.items()):
        assert ikey == key and 'Should have original iterable index/key'
        revval = copy.deepcopy(val)[::-1]
        cur_stat = stats[key]
        stable_val, stable_lvl_from_head = int(cur_stat['diff_stasis']), cur_stat['lvl']
        assert revval[0][0] == stable_val and 'All ints at this level must be same'
        assert len(val) == (stable_lvl_from_head + 1) and 'After stable level ommited all 0s'
        prev = stable_val

        for i, v in enumerate(revval):
            cur = v

            if i == 0:
                assert cur[0] == prev == cur[-1]
                assert revval[i][0] == prev
                prev = cur[0]
                revval[i].append(prev)
            elif i < len(revval):
                assert v[-1] == revval[i][-1]
                nxt = v[-1] + prev
                revval[i].append(nxt)
                prev = nxt

        derived_ancestors.append(prev)

    # pprint(('derived_ancestors:', derived_ancestors))
    return sum(derived_ancestors)


def join_head_diffs(diffs, ldata):
    """
    def join_head_diffs(diffs, ldata):
        ND = {}
        for i, ds in enumerate(diffs):
            nnlst = [ldata[i]]
            nnlst.extend(d for d in ds if not any(d) == 0)
            ND[i] = nnlst
        return ND
    """
    ND = {}
    for i, ds in enumerate(diffs):
        nnlst = [ldata[i]]
        for d in ds:
            if not any(d) == 0:
                nnlst.append(d)
        ND[i] = nnlst
    return ND


def parse_data(data: str) -> list[list[int]]:
    """
    def parse_data(data: str) -> list[list[int]]:
        return [list(map(int, line.split())) for line in data.splitlines()]
    """
    lines: map[list[int]] = map(ints, data.splitlines())
    return list(lines)


profile_stats_test = 'profile_stats_check_test'
cProfile.run('check_test(part1, part2)', profile_stats_test)
stats = pstats.Stats(profile_stats_test).strip_dirs()
stats.sort_stats('cumulative')
# stats.print_stats(4)

"""
Fri Dec 15 13:24:19 2023    profile_stats_check_test
         20 function calls in 0.000 seconds
"""

profile_stats = 'profile_stats_check'
cProfile.run('check(part1, part2)', profile_stats)
stats = pstats.Stats(profile_stats)
stats.sort_stats('cumulative')
stats.print_stats(10)
"""
Fri Dec 15 19:04:03 2023    profile_stats_check
         249645 function calls (213406 primitive calls) in 0.192 seconds
"""

"""
# LLM Summary

"""
