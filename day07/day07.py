import cProfile
import numpy as np
from utils import *


def part1(data):
    """
    Evaluate hands based on strength:

    - Identify unique one-pair hand, 32T3K, and assign it rank 1.
    - Analyze two-pair hands, KK677 and KTJJT.
      Compare first cards; favor KK677 with a stronger second card (K vs. T).
      Assign rank 2 to KTJJT and rank 3 to KK677.
    - Examine three-of-a-kind hands, T55J5 and QQQJA.
      Prioritize QQQJA due to a stronger first card, resulting in rank 5 for QQQJA and rank 4 for T55J5.

    Calculate total winnings by summing the product of each hand's bid and its rank (765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5).
    Total winnings in this example amount to 6440.

    Determine the rank of each hand in the set and total winnings.
    """
    D = data.strip()
    rows = [line.strip().split(' ') for line in D.splitlines()]
    bids = {bid[0]: int(bid[1]) for bid in rows}
    pprint(bids)

    # Evaluate hands based on strength:
    #
    # In Camel Cards, receive a list of hands; goal is to order based on strength.
    # A hand comprises cards labeled A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2.
    # Relative card strength follows order, with A highest and 2 lowest.
    C = 'A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2'.split(', ')

    indexes = {
        bid: [C.index(bid[j]) for j, r in enumerate(bid) if bid[j] in C]
        for i, bid in enumerate([b for b in bids])
    }
    # pprint(indexes)

    # Assign each hand exactly one type. From strongest to weakest:
    #
    #     Five of a kind, all five cards with same label: AAAAA
    #     Four of a kind, four cards with same label, one card with different label: AA8AA
    #     Full house, three cards with same label, remaining two cards share different label: 23332
    #     Three of a kind, three cards with same label,
    #       remaining two cards different from any
    #       other card in the hand: TTT98
    #     Two pair, two cards share one label, two other cards share second label, remaining card has third label: 23432
    #     One pair, two cards share one label, other three cards with different label from pair and each other: A23A4
    #     High card, all cards' labels distinct: 23456

    # IDEA: use match case
    rules = {'1': 'AAAAA', '2': 'AA8AA', '3': '23332', '4': 'TTT98',
             '5': '23432', '6': 'A23A4', '7': '23456'}

    def count_similar(labels) -> int:
        ls = list(labels)
        unq_labels = set(ls)
        count = len(unq_labels)
        # print(f'{labels} {unq_labels} count: {count}')
        return count

    def get_hand_rank(labels: str):
        unique_labels = count_similar(labels)
        # print(unique_labels)
        if unique_labels == 1:
            return 1  # five of a kind
        elif unique_labels == 2:
            return 2  # four of a kind
        elif unique_labels == 3:
            # TODO: use Counter. If 2 pairs, it shouldn't return 3?
            return 3  # three of a kind
        elif unique_labels == 4:
            return 4  # pair
        else:
            return None  # todo

    pprint(rules)

    # 32T3K 765
    # T55J5 684
    # KK677 28
    # KTJJT 220
    # QQQJA 483
    p1 = 0  # sum_winnings = 0
    for bid, idxs in indexes.items():
        rank = get_hand_rank(bid)
        price = bids[bid]
        imul = price * rank
        print(bid, price, '* rank:', rank, '= $:', imul)
        # rank (765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5).
        p1 += imul

    # Total winnings in this example are 6440.
    print(p1)  # 7305


def part2(data):
    pass


check_test(part1, part2)
# check(part1, part2)
"""
{'32T3K': 765, 'KK677': 28, 'KTJJT': 220, 'QQQJA': 483, 'T55J5': 684}
{'1': 'AAAAA',
 '2': 'AA8AA',
 '3': '23332',
 '4': 'TTT98',
 '5': '23432',
 '6': 'A23A4',
 '7': '23456'}
32T3K 765 * rank: 4 = $: 3060
T55J5 684 * rank: 3 = $: 2052
KK677 28 * rank: 3 = $: 84
KTJJT 220 * rank: 3 = $: 660
QQQJA 483 * rank: 3 = $: 1449
7305
"""
