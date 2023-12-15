# day9.py
#
# --- Day 9: Mirage Maintenance ---

from utils import *

"""
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45

"""


def part1(data):
    D = data.strip()
    ldata = parse_data(D)
    diffs = [consec_diffs(lst=lst) for lst in ldata]
    p1 = solve(ldata, diffs)
    print(p1)  # 114 | 1953784198


def part2(data):
    if False:
        D = data.strip()
        ldata = parse_data(D)
        diffs = [consec_diffs(lst=lst) for lst in ldata]
        p2 = solve(ldata, diffs)
        print(p2)  # ? | ?


def consec_diffs(lst: list[int]):
    diffs: list[list[int]] = []
    while len(lst) > 1:
        diff = [lst[i + 1] - lst[i] for i in range(len(lst) - 1)]
        diffs.append(diff)
        lst = diff
    return diffs


def solve(ldata, diffs):
    """
    Analyze your OASIS report and extrapolate the next value for each history.
    What is the sum of these extrapolated values?
    """

    before_data = join_head_diffs(diffs, ldata)
    # pprint(('before_data:', before_data))
    stats = {}
    for idx, diff in enumerate(diffs):
        buf = []
        glvl = 0
        gdiff = 0
        for i, d in enumerate(diff):
            unq_diff = len(set(d))
            lvl = i + 1
            print(d)
            diffstasis = d[0] - d[1]
            gdiff = diffstasis
            glvl = lvl

            str_all_0 = [1 for iint in d if iint == 0]
            has_all_0s = (len(str_all_0) > 0 and all(str_all_0) == 1)
            is_valid = unq_diff == 1
            statval = dict(lvl=lvl, homeostasis=diffstasis if not is_valid else d[0], jstr=ljoinstr(d))

            if is_valid:
                buf.append(statval)
                # dict(stable_val=d_str[0], d_str=d_str, i=i)
                break
            # if has_all_0s:
            #     break

        statval = dict(lvl=glvl, homeostasis=gdiff, jstr=ljoinstr(diff))
        stats[idx] = buf[0] if buf else statval
        # stats[idx] = buf[0]

    # stats = {
    #     idx: [dict(lvl=(i + 1), homeostasis=ljoinstr(d)[0], jstr=ljoinstr(d))
    #           for i, d in enumerate(diff)
    #           if len(set(ljoinstr(d))) == 1][0]
    #     for idx, diff in enumerate(diffs)
    # }
    pprint(stats)
    # pprint((ldata, diffs))

    extrapolated_data = []
    derived_ancestors = []
    for ikey, (key, val) in enumerate(before_data.items()):
        assert ikey == key and 'Should have original iterable index/key'
        revval = copy.deepcopy(val)[::-1]
        cur_stat = stats[key]
        pprint(cur_stat)

        stable_val, stable_lvl_from_head = int(cur_stat['homeostasis']), cur_stat['lvl']
        if revval[0][0] != stable_val:
            print((revval[0], stable_val))
        assert revval[0][0] == stable_val and 'All ints at this level must be same'
        assert len(val) == (stable_lvl_from_head + 1) and 'After stable level ommited all 0s'

        prev = stable_val

        for i, v in enumerate(revval):
            cur = v
            # print(key, i, prev, v)
            if i == 0:
                assert cur[0] == prev == cur[-1]
                assert revval[i][0] == prev
                prev = cur[0]
                revval[i].append(prev)
            elif i < len(revval):
                assert v[-1] == revval[i][-1]
                exsum = v[-1] + prev
                revval[i].append(exsum)
                prev = revval[i][-1]
        extrapolated_data.append(revval)
        derived_ancestors.append(prev)

    # pprint(('extrapolated_data:', extrapolated_data))
    # pprint(('derived_ancestors:', derived_ancestors))

    return sum(derived_ancestors)


def join_head_diffs(diffs, ldata):
    ND = {}
    for i, ds in enumerate(diffs):
        nnlst = [ldata[i]]
        for d in ds:
            if not any(d) == 0:
                nnlst.append(d)
        ND[i] = nnlst
    return ND


def parse_data(data: str) -> Any:
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
# stats.print_stats(3)
"""
Fri Dec 15 13:24:19 2023    profile_stats_check
         20 function calls in 0.003 seconds
"""

"""
# LLM Summary

"""
