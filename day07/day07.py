from utils import *


def classify_rank(hand) -> int:
    """Since sample set has unique stats, a simple classification works"""
    hand_stats = sorted(Counter(hand).values())
    match hand_stats:
        # @formatter:off
        case [5]:           return 6  # Five of a kind
        case [1, 4]:        return 5  # Four o a kind
        case [2, 3]:        return 4  # Full house
        case [1, 1, 3]:     return 3  # Three of a kind
        case [1, 2, 2]:     return 2  # Two pair
        case [1, 1, 1, 2]:  return 1  # One pair
        case _:             return 0  # High card
        # @formatter:on


def compute_score(data, card_rank_order) -> int:
    hands = []
    for line in data.splitlines():
        hand, bid = line.split()
        rank_by_hand = classify_rank(hand)
        ranks_by_order = tuple(card_rank_order.index(c) for c in hand)
        hands.append((rank_by_hand, ranks_by_order, int(bid)))
    return sum(rank_index * bid
               for rank_index, (_, _, bid) in enumerate(sorted(hands), start=1))


def part1(data):
    D = data.strip()
    card_rank_order = 'AKQJT98765432'[::-1]
    p1 = compute_score(D, card_rank_order)
    print(p1)  # 6440


def part2(s):
    pass


cProfile.run('check_test(part1, part2)', sort='cumulative')
