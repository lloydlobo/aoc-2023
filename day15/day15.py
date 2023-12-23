# day15.py

from utils import *


def simple_hash(s: str) -> int:
    cur: int = 0
    for c in s:
        cur += ord(c)
        cur *= 17
        cur %= 256
    return cur


assert simple_hash('HASH') == 52


# ----------------------------------------------------------------------------------------------------------------------

def solve(seqs: list[str], for_part2: bool = False):
    if not for_part2:
        return sum([simple_hash(s) for s in seqs])
    lbry: dict[int, list[str]]  # lbry = defaultdict(list, {i: [] for i in range(256)})
    lbry = {i: [] for i in range(256)}
    for seq in seqs:
        lbl: str = (seq.split('-', 1) if '-' in seq else seq.split('=', 1))[0]  # lbl, rest = re.split('[-=]', seq, 1)
        b_id: int = simple_hash(lbl)
        if '-' in seq:  # `-` del
            lbry[b_id] = [l for l in lbry[b_id] if not l.startswith(lbl)]  # faster than list.remove(value)
        else:  # `=` add/update
            found = False
            l: str
            for i, l in enumerate(lbry[b_id]):
                if l.startswith(lbl):
                    lbry[b_id][i] = seq
                    found = True
                    break
            if not found:
                lbry[b_id].append(seq)
    return sum(
        (b_id + 1) * (l_lst.index(l) + 1) * int(l[(l.index('=') + 1):])
        for b_id, l_lst in enumerate(lbry.values())
        if l_lst
        for l in l_lst
    )


# ----------------------------------------------------------------------------------------------------------------------

def part1(data):
    input_data = [data.split(',')][0]
    p1 = solve(input_data, for_part2=False)
    print(f'{p1=}')  # 1320 | 510273


def part2(data):
    input_data = [data.split(',')][0]
    p2 = solve(input_data, for_part2=True)
    print(f'{p2=}')  # 145 | 212449


# ----------------------------------------------------------------------------------------------------------------------

check_test(part1, part2)
check(part1, part2)


# ----------------------------------------------------------------------------------------------------------------------


def solve_v1(seqs, for_part2=False):
    if not for_part2:
        return sum([simple_hash(sequence) for i, sequence in enumerate(seqs)])
    library: dict[int, list[str]] = {i: [] for i in range(256)}
    for seq in seqs:
        if '=' in seq:
            label = seq[:seq.index('=')]
            box_id = simple_hash(label)
            found_duplicate = False
            for lens_index, lens in enumerate(library[box_id]):
                if lens.startswith(label):
                    library[box_id][lens_index], found_duplicate = seq, True
            if not found_duplicate:
                library[box_id].append(seq)
        elif '-' in seq:
            label = seq[:seq.index('-')]
            box_id = simple_hash(label)
            for lens in library[box_id]:
                if lens.startswith(label):
                    library[box_id].remove(lens)
    powers = []
    for box_id, lenses in list((i, x) for i, x in enumerate(library.values()) if x):
        for lens_idx, lens in enumerate(lenses):
            powers.append((box_id + 1) * (lenses.index(lens) + 1) * (int(lens[(lens.index('=') + 1):])))
    return sum(powers)


def solve_v2(seqs: list[str], for_part2: bool = False):
    if not for_part2:
        return sum([simple_hash(sequence) for i, sequence in enumerate(seqs)])
    lbry: dict[int, list[str]] = {i: [] for i in range(256)}

    for seq in seqs:
        if '-' in seq:  # del_cmd
            lbl = seq.split(sep='-')[0]
            b_id = simple_hash(lbl)
            lbry[b_id] = [l for l in lbry[b_id] if not l.startswith(lbl)]  # faster than list.remove(value)
        elif '=' in seq:  # add_cmd
            lbl = seq.split(sep='=')[0]
            b_id = simple_hash(lbl)
            found = False
            for i, l in enumerate(lbry[b_id]):
                if l.startswith(lbl):
                    lbry[b_id][i] = seq
                    found = True
                    break
            if not found:
                lbry[b_id].append(seq)
    return sum(
        (b_id + 1) * (l_lst.index(l) + 1) * int(l[(l.index('=') + 1):])
        for b_id, l_lst in enumerate(lbry.values())
        if l_lst
        for l in l_lst
    )


def solve_v3(seqs: list[str], for_part2: bool = False):
    if not for_part2:
        return sum([simple_hash(s) for s in seqs])
    lbry: OrderedDict[int, list[str]] = OrderedDict((i, []) for i in range(256))
    for seq in seqs:
        lbl: str = (seq.split('-', 1) if '-' in seq else seq.split('=', 1))[0]
        b_id: int = simple_hash(lbl)
        if '-' in seq:
            lbry[b_id] = [l for l in lbry[b_id] if not l.startswith(lbl)]
        else:
            found = False
            for i, l in enumerate(lbry[b_id]):
                if l.startswith(lbl):
                    lbry[b_id][i] = seq
                    found = True
                    break
            if not found:
                lbry[b_id].append(seq)
    return sum(
        (b_id + 1) * (l_lst.index(l) + 1) * int(l[(l.index('=') + 1):])
        for b_id, l_lst in lbry.items()
        if l_lst
        for l in l_lst
    )


# ----------------------------------------------------------------------------------------------------------------------

sample_data = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'
with open('input.txt') as file:
    sample_data = file.read().rstrip()

sample_seqs = sample_data.split(',')  # print(f'{sample_seqs=}')
time_v1 = timeit.timeit(lambda: solve_v1(sample_seqs, for_part2=True), number=100)
time_v2 = timeit.timeit(lambda: solve_v2(sample_seqs, for_part2=True), number=100)
time_v3 = timeit.timeit(lambda: solve_v3(sample_seqs, for_part2=True), number=100)
time_vcur = timeit.timeit(lambda: solve(sample_seqs, for_part2=True), number=100)

print(f'{time_v1=}\n{time_v2=}\n{time_v3=}\n{time_vcur=}')
"""
time_v1=0.7742957809969084
time_v2=0.7698641960014356
time_v3=0.7423599739995552
time_vcur=0.7429749139992055

time_v1=0.7550256770045962
time_v2=0.744722660005209
time_v3=0.7245874499931233

time_v1=0.7395110679935897
time_v2=1.2018284829973709
"""
