# day7.py
#
# --- Day 7: Camel Cards ---

from utils import *


def part1(data):
    D = data.strip()
    card_rank_order = 'AKQJT98765432'[::-1]
    p1 = compute_winnings(D, card_rank_order, has_wild=False)
    # print(p1)  # 6440


def part2(data):
    D = data.strip()
    card_rank_order = 'AKQT98765432J'[::-1]  # 'J' are now jokers, but weakest individually
    p2 = compute_winnings(D, card_rank_order, has_wild=True)
    # print(p2)  # 5905


def compute_winnings(data: str, card_rank_order: str, has_wild: bool) -> int:
    hand: str
    bid: str
    hs: list[tuple[int, tuple[int, ...], int]]
    hs = [
        (
            strength_wild(hand) if (has_wild and 'J' in hand) else strength(hand),
            tuple(card_rank_order.index(c) for c in hand),
            int(bid),
        )
        for hand, bid in [line.split() for line in data.splitlines()]
    ]
    return sum((idx_rank * bid)
               for idx_rank, (_, _, bid) in enumerate(sorted(hs), start=1))


def strength(hand: str) -> int:
    """Since sample set has unique stats, a simple classification works"""
    match sorted(Counter(hand).values()):
        # @formatter:off
        case [5]:           return 6  # Five of a kind
        case [1, 4]:        return 5  # Four o a kind
        case [2, 3]:        return 4  # Full house
        case [1, 1, 3]:     return 3  # Three of a kind
        case [1, 2, 2]:     return 2  # Two pair
        case [1, 1, 1, 2]:  return 1  # One pair
        case _:             return 0  # High card
        # @formatter:on


def strength_wild(hand: str) -> int:
    replacements = [hand.replace('J', r) for r in sorted(set(hand))]
    strengths = [strength(r) for r in replacements]
    return max(strengths, default=0)


# cProfile.run(statement='check_test(part1, part2)', sort='cumulative')
cProfile.run(statement='check(part1, part2)', sort='cumulative')
"""
         54266 function calls (54254 primitive calls) in 0.056 seconds
         56266 function calls (56254 primitive calls) in 0.061 seconds
         57268 function calls (57256 primitive calls) in 0.060 seconds
         58928 function calls (58916 primitive calls) in 0.092 seconds
"""
