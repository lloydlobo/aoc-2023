import math
from collections import defaultdict

import matplotlib.pyplot as plt
import networkx as nx

from utils import *


def data_to_graph_parts(data: str):
    mods = {}
    flips, conjs = defaultdict(int), defaultdict(dict)  # '%', '&'

    for line in data.splitlines():
        src, _, *dsts = line.replace(',', '').split()
        k, s = (src[0], src[1:]) if src[0] in '%&' else ('', src)
        mods[s] = k, dsts

        for dst in dsts:
            conjs[dst][s] = 0  # off initially

    return mods, flips, conjs


def solve(mods, flips, conjs, is_p2):
    res = None
    bc = 'broadcaster'
    assert mods.get(bc) is not None

    btns = 0
    counts = [0, 0]  # counts[0]: low; counts[1]: high
    btns_limit, max_btns = 0, 3000

    while True and (btns_limit := btns_limit + 1) < max_btns:
        if btns == 1_000:
            res = math.prod(counts)
            if is_p2:
                break

        btns += 1
        q = [(None, bc, 0)]  # prev_mod, cur_mod, pulse_in
        q_limit, max_q = 0, 3000

        while q and ((q_limit := q_limit + 1) < max_q):
            prev_mod, cur_mod, pulse_in = q.pop(0)
            assert prev_mod is None if cur_mod == bc else True
            assert pulse_in in {0, 1}

            counts[pulse_in] += 1

            if cur_mod not in mods:
                continue

            cur_mod_kind, nxts = mods[cur_mod]

            match (cur_mod_kind, pulse_in):  # input pulse from prev_mod to cur_mod
                case ('', _):
                    pulse_out = pulse_in
                case ('%', 0):
                    flips[cur_mod] = not flips[cur_mod]  # flip and record on/off state
                    pulse_out = flips[cur_mod]
                case ('&', _):
                    conjs[cur_mod][prev_mod] = pulse_in  # record pulse_in from prev_mod -> cur_mod mapping
                    pulse_out = not all(conjs[cur_mod].values())  # if all([pulse_type,..]) -> opposite(pulse_type)
                case (_, _):
                    continue

            assert pulse_out in {0, 1}

            for nxt in nxts:
                q.append((cur_mod, nxt, pulse_out))

    return res


def part1(data):
    p1 = solve(*data_to_graph_parts(data), is_p2=False)
    print(f'{p1=}')  # 11687500 | 788081152


def part2(data):
    p2 = solve(*data_to_graph_parts(data), is_p2=True)
    print(f'{p2=}')


check_test(part1, part2)
check(part1, part2)


# ----------------------------------------------------------------------------------------------------------------------

def solve_v2(data, is_part2: bool):
    """Ported from @4HbQ https://www.reddit.com/r/adventofcode/comments/18mmfxb/comment/ke5m940/"""

    result = None
    modules = {}
    flips = defaultdict(int)
    conjs = defaultdict(dict)
    rx = None
    G = nx.Graph()

    for line in data.splitlines():
        msrc, _, *mdsts = line.replace(',', '').split()
        mtype, msrc = (msrc[0], msrc[1:]) if msrc[0] in '%&' else ('', msrc)
        modules[msrc] = mtype, mdsts
        G.add_node(msrc, module_type=mtype, color=('yellow' if mtype == '' else 'pink' if mtype == '%' else 'orange'))
        for mdst in mdsts:
            conjs[mdst][msrc] = 0
            G.add_edge(msrc, mdst)
            if is_part2 and mdst == 'rx':
                rx = msrc

    # plot_graph(G)
    # pprint(dict(nodes=G.nodes, edges=G.edges))
    # pprint(dict(modules=modules, conjs=conjs))

    rx_ins = {i: 0 for i in conjs[rx]} if is_part2 else None
    # print(f'{rx,rx_ins=}') rx, rx_ins = ('xm', {'ft': 0, 'jz': 0, 'sv': 0, 'ng': 0})

    presses = 0
    counts = [0, 0]
    li_1, limit_1 = 0, 2002

    while True and (li_1 := li_1 + 1) < limit_1:
        if presses == 1_000:
            result = math.prod(counts)
            if not is_part2:
                break
        presses += 1
        if is_part2 and all(rx_ins.values()):
            result = math.prod(rx_ins.values())
            break

        q = [(None, 'broadcaster', 0)]  # src, module, low(0)|high(1)
        li_2, limit_2 = 0, 1001

        while q and (li_2 := li_2 + 1) < limit_2:
            src, mod, pulse_in = q.pop(0)
            counts[pulse_in] += 1

            if mod not in modules:
                continue

            mod_type, mod_nxts = modules[mod]

            match mod_type, pulse_in:
                case '', _:
                    pulse_out = pulse_in
                case '%', 0:  # flipfop with low pulse
                    pulse_out = flips[mod] = not flips[mod]
                case '&', _:  # conjunction
                    conjs[mod][src] = pulse_in
                    pulse_out = not all(conjs[mod].values())
                    if is_part2 and 'rx' in mod_nxts:
                        pass  # unimplemented
                case _, _:
                    continue

            for _nxt_mod in mod_nxts:
                q.append((mod, _nxt_mod, pulse_out))

    return result


# def solve_v1(graph, is_part2: bool):
# """Ported from @david3x3x3x https://www.reddit.com/r/adventofcode/comments/18mmfxb/comment/ke5sgxs/"""
#     NUM_BUTTON_PUSHES = 1000
#     res = []
#
#     for m in graph['broadcaster']:
#         nxt = [m]
#         num = 0
#         n_num = 0
#
#         while nxt:
#             m_nxt = nxt[0]
#             g = graph['%' + m_nxt]
#             num |= (len(g) == 2 or '%' + g[0] not in graph) << n_num
#             n_num += 1
#             nxt = [nxt_ for nxt_ in graph['%' + m_nxt] if '%' + nxt_ in graph]
#
#         res.append(num)
#
#     return math.lcm(*res)
#


def plot_graph(G):
    # force-directed representation of the network treating edges as springs holding nodes close, while treating
    # nodes as repelling objects
    k = 1 / (len(G.nodes.keys()) ** 0.5)  # optimal distance between nodes
    gpos = nx.fruchterman_reingold_layout(G, k=(1.618 * k))  # gpos = nx.spring_layout(G)

    # arrow_styles = ['->', '-[', '-|>', '->,head_width=0.4,head_length=0.5', 'fancy', 'wedge,tail_width=0.7']
    nx.draw(G, gpos, with_labels=True, node_size=300,
            node_color=[v.get('color', 'skyblue') for k, v in G.nodes.items()],
            font_size=10, font_color='black', font_weight='bold', edge_color='gray', linewidths=0.5,
            arrows=True, arrowsize=10, arrowstyle='-|>', connectionstyle="arc3,rad=0.1")

    legend_labels = {'FlipFlop': 'pink', 'Conjunction': 'orange', 'Broadcaster': 'yellow', 'Output': 'skyblue'}
    legend_handles = [plt.Line2D([0], [0], marker='o', color='w', label=label, markerfacecolor=color, markersize=10)
                      for label, color in legend_labels.items()]

    plt.legend(handles=legend_handles, title="Module Colors", loc="upper left")

    plt.show()  # ascii_art = nx.generate_network_text(G, with_labels=True, ascii_only=True)  # for x in ascii_art: #     print(x)


def parse_data(data: str):
    graph = {(parts := line.rstrip().split(' -> '))[0]: parts[1].split(', ') for line in data.splitlines()}
    return graph
