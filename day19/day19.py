from utils import *

XMAS_RATINGS = ['x', 'm', 'a', 's']
START_W_NAME = 'in'


def solve(data, is_part2):
    global XMAS_RATINGS, START_W_NAME
    workflows, xmas_ratings = data
    W_KEYS = workflows.keys()
    pprint(dict(W_KEYS=W_KEYS, inpt=workflows, xmas=xmas_ratings))
    graphs = update_graph(START_W_NAME, workflows, xmas_ratings)
    pprint(dict(graphs=graphs))
    total = 0
    for k_xmas, v_graph in graphs.items():
        print(k_xmas)
        is_accepted = False
        for k, v in v_graph.items():
            print(k, '->', v)
            if 'A' == v:
                is_accepted = True
                break
            elif 'R' == v:
                is_accepted = False
                break
        if is_accepted:
            total += sum(ints(f'{k_xmas}'))

    # paths = traverse_graph(RATINGS, W_KEYS, cur_w_name, li, limit, paths, workflows, xmas_ratings)
    # print(paths)
    return total


def update_graph(START_W_NAME, workflows, xmas_ratings):
    """
    All parts begin in the workflow named in.
    In this example, the five listed parts go through the following workflows:

    {x=787,m=2655,a=1222,s=2876}: in -> qqz -> qs -> lnx -> A
    {x=1679,m=44,a=2067,s=496}: in -> px -> rfg -> gd -> R
    {x=2036,m=264,a=79,s=2244}: in -> qqz -> hdj -> pv -> A
    {x=2461,m=1339,a=466,s=291}: in -> px -> qkq -> crn -> R
    {x=2127,m=1623,a=2188,s=1013}: in -> px -> rfg -> A
    """
    # ------------------------------------------------
    # Parse and create graph.
    W = copy.deepcopy(workflows)
    cur_W = START_W_NAME
    graphs = {}
    # ------------------------------------------------
    for ratings in xmas_ratings:
        # print(ratings)
        # ------------------------------------------------
        # 1. start at node 'in'
        # 2. see if rule sequence item qualifies the comaprison at 'in' workflow
        graph = {}
        cur = 'in'
        graph[cur] = None
        iterations = 0
        found_end = False
        li, limit = 0, 11
        while True and (li := li + 1) < limit and not found_end:
            if cur not in W.keys():
                break
            cur_vals = W[cur]
            # print(cur, cur_vals)
            for val in cur_vals:
                is_last_rule = ':' not in val
                # print(f'\t{val,is_last_rule=}')
                if not is_last_rule:
                    condition, target = val.split(':')
                    char_xmas = condition[0]  # 's<1351'=>s
                    char_cmp = condition[1]
                    strnum_rule_rating = condition[2:]
                    assert strnum_rule_rating.isdigit()
                    assert char_cmp in {'<', '>'}
                    assert char_xmas in XMAS_RATINGS
                    xmas_rating = ratings[XMAS_RATINGS.index(char_xmas)][2:]
                    assert xmas_rating.isdigit()
                    a, b = int(xmas_rating), int(strnum_rule_rating)
                    cmp_ab = a < b if char_cmp == '<' else a > b
                    if cmp_ab:
                        graph[cur] = target
                        cur = target
                        break
                    print(f'\t\t{condition,target,xmas_rating,cmp_ab=}')
                else:
                    tmp = cur
                    graph[cur] = val
                    if val in W.keys():
                        cur = val
                    else:
                        graph[tmp] = val
                        found_end = True
                        # print('found_end', cur, tmp, val)
                    break
            # print(f'{cur,graph=}')  # cur='A'
            graphs[ratings] = graph
            # pprint(dict(graphs=graphs))
            # continue
            # continue
            # # ------------------------------------------------
            # # 3. ... assume 'qqz' qualifies comparison finally. set cur to 'qqz'
            # nxt = 'qqz'
            # if check_condition():
            #     graph[cur] = nxt
            # cur = nxt
            # iterations += 1
            # # ------------------------------------------------
            # # 4. ... ... assume 'qs' qualifies comparison finally. set cur to 'qs'
            # if iterations > 1:
            #     nxt = 'qs'
            #     graph[cur] = nxt
            #     cur = nxt
            #     iterations += 1
            #     # ------------------------------------------------
            #     if iterations > 2:
            #         nxt = 'lnx'
            #         graph[cur] = nxt
            #         cur = nxt
            #         iterations += 1
            #         # ------------------------------------------------
            #         # now 'm' cmp satisfies, but next node in rule is A
            #         if iterations > 2:
            #             if 'A' not in W.keys():
            #                 nxt = 'A'
            #                 graph[cur] = nxt
            #                 cur = nxt
            #                 iterations += 1
            #                 break
            #             else:
            #                 nxt = 'lnx'
            #                 graph[cur] = nxt
            #                 cur = nxt
            #                 iterations += 1

        graphs[ratings] = graph
        """
        {'W_KEYS': dict_keys(['px', 'pv', 'lnx', 'rfg', 'qs', 'qkq', 'crn', 'in', 'qqz', 'gd', 'hdj']),
         'inpt': {'crn': ('x>2662:A', 'R'),
                  'gd': ('a>3333:R', 'R'),
                  'hdj': ('m>838:A', 'pv'),
                  'in': ('s<1351:px', 'qqz'),
                  'lnx': ('m>1548:A', 'A'),
                  'pv': ('a>1716:R', 'A'),
                  'px': ('a<2006:qkq', 'm>2090:A', 'rfg'),
                  'qkq': ('x<1416:A', 'crn'),
                  'qqz': ('s>2770:qs', 'm<1801:hdj', 'R'),
                  'qs': ('s>3448:A', 'lnx'),
                  'rfg': ('s<537:gd', 'x>2440:R', 'A')},
         'xmas': [('x=787', 'm=2655', 'a=1222', 's=2876'),
                  ('x=1679', 'm=44', 'a=2067', 's=496'),
                  ('x=2036', 'm=264', 'a=79', 's=2244'),
                  ('x=2461', 'm=1339', 'a=466', 's=291'),
                  ('x=2127', 'm=1623', 'a=2188', 's=1013')]}
        ('x=787', 'm=2655', 'a=1222', 's=2876')
        in ('s<1351:px', 'qqz')
        qqz ('s>2770:qs', 'm<1801:hdj', 'R')
        nodes={'in': 'qqz', 'qqz': 'qs', 'qs': 'lnx', 'lnx': 'A'}
        p1=None
        """
        # break  # just solve for first set of ratings
    return graphs


def parse_input(data):
    workflows, seen = {}, set()
    xmas_ratings = []
    for r in data.rstrip().splitlines():
        if not r: continue
        if r[0] != '{':
            (k_wname, v_wrules) = r.split('{')
            assert k_wname not in seen
            seen.add(k_wname)
            rules = tuple(v_wrules[:-1].split(','))  # if elif else rules. max_len == 4
            assert 0 <= len(rules) <= 4
            workflows[k_wname] = rules  # remove trailing '}', split item separator
        else:  # remove enclosing '{' and '}', split items separators
            xmas_ratings.append(tuple(r.strip()[1:-1].split(',')))
    return workflows, xmas_ratings


def part1(data):
    D = parse_input(data)
    p1 = solve(D, False)
    print(f'{p1=}')  # 19114 | 575412


def part2(data):
    if _DEBUG_SOLVE := True:
        return
    D = parse_input(data)
    p2 = solve(D, False)
    print(f'{p2=}')


# Check tests and main execution
check_test(part1, part2)
check(part1, part2)

# ----------------------------------------------------

# def traverse_graph(RATINGS, W_KEYS, cur_w_name, paths, workflows, xmas_ratings):
#     li, limit = 0, 21
#     paths = []
#     while True and (li := li + 1) < limit:
#         for i, xmas in enumerate(xmas_ratings):
#             cur_rules = workflows[cur_w_name]
#             qualified = False
#             next = None
#             path = []
#             for irule, rule in enumerate(cur_rules):
#                 if len(rule) > 1 and (cmp := rule[1]) in {'<', '>'} and (rating := rule[0]) in RATINGS:
#                     cur_xmas_rating = int(xmas[_idx_rating := RATINGS.index(rating)][2:])
#                     num_rating_nxt_w = rule[2:].split(':')
#                     cur_rule_rating, nxt_w = int(num_rating_nxt_w[0]), num_rating_nxt_w[1]
#                     if qualified := cur_xmas_rating < cur_rule_rating if cmp == '<' else cur_xmas_rating > cur_rule_rating:
#                         # next = nxt_w
#                         # print(cur_w_name, irule, rule, cur_xmas_rating, qualified)
#                         if nxt_w in W_KEYS:  # rule.split(':')[1]
#                             path.append(nxt_w)
#                             cur_w_name = nxt_w  # update
#                             # break
#                 else:
#                     next = rule
#             if qualified:
#                 if next in W_KEYS:
#                     cur_w_name = next
#                 print(next, 'qualified')
#                 path.append(next)
#                 paths.append(path)
#                 # break
#     return paths
