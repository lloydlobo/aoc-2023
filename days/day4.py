import os
from collections import defaultdict
from typing import TextIO


def part1(infile: TextIO) -> int:
    """
    You've got a bunch of scratchcards with numbers on them. Each card has a
    set of winning numbers and a list of numbers you have. You need to find
    which of the numbers you have match the winning numbers on each card.

    For instance, if a card has numbers 41, 48, 83, 86, and 17 as winning
    numbers, and your numbers include 83, 86, 6, 31, 17, 9, 48, and 53,
    you've got four matches (48, 83, 17, and 86). So, that card is worth 8
    points (1 for the first match and doubled for the next three).

    For every match, the card gets a point. The first match is worth 1 point,
    and each subsequent match doubles the card's points. Add up the total
    points from all the scratchcards to find out their total value.
    """
    grid = list(infile)
    cards = {(r + 1): [[int(num) for num in
                        nums.split(': ', 1)[-1].replace(' ', ',').split(',') if
                        num] for nums in row.split('|')] for r, row in
             enumerate(grid)}
    total_pts = 0

    for win_nums, cur_nums in cards.values():
        pts = 0

        for _ in range(len(set(win_nums) & set(cur_nums))):
            if pts == 0:  # First round
                pts += 1
            else:
                pts *= 2

        total_pts += pts
    # print(total_pts)

    return total_pts  # star 1


def part2(infile: TextIO) -> int:
    """
    Winning means getting more cards equal to the number of matching numbers
    you have.

    Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
    Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
    Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
    Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
    Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11

    If card 10 has 5 matching numbers, you'd win cards 11, 12, 13, 14, and 15.
    Every new card you win follows the same rules. If card 10 wins 5 cards,
    those new cards (11 to 15) will win cards as well. You keep going until none
    of the new cards win any more. The total is how many cards you end up with,
    including the original set.

    In the given example, you start with 6 cards. As you win more,
    the numbers keep growing until you have 30 cards in total. The task is to
    calculate how many cards you end up with in total after following these
    rules for all the scratchcards.
    """
    grid: list[str] = list(infile)

    # Init dict with default values
    p1 = defaultdict(lambda: 0.5)  # First win is 1pt. next is 2*cur point
    p2 = defaultdict(lambda: 0.0)  # Total cards you end up with including cur

    for cur_idx, row in enumerate(grid):
        win_nums, card_nums = map(str.split, row.split('|'))
        common_nums: set[str] = set(win_nums) & set(card_nums)

        p2[cur_idx] += 1.0  # Initialize with 1.0 for each first win

        for offset in range(len(common_nums)):
            p1[cur_idx] *= 2  # Doubling points for each match
            p2[cur_idx + offset + 1] += p2[cur_idx]  # Update running total

    total_points_p1 = sum(map(int, p1.values()))
    total_cards_p2 = sum(map(int, p2.values()))
    # print(total_points_p1, total_cards_p2)

    return total_cards_p2  # star 2


def part2_old(infile: TextIO) -> int:
    grid: list[str] = list(infile)
    cards: dict = {
        (r + 1): [[int(num) for num in
                   nums.split(': ', 1)[-1].replace(' ', ',').split(',') if num]
                  for nums in row.split('|')] for r, row in enumerate(grid)}

    winners = {k: [] for k in cards.keys()}

    def collect_winners(arg_cards, arg_winners):
        for key, (win_nums, cur_nums) in arg_cards.items():
            matches = set(win_nums) & set(cur_nums)
            for i in range(1, (len(matches) + 1)):
                arg_winners[key].append(i + key)

    def count_winners(wnrs) -> int:
        return sum(len(val) for val in wnrs.values())

    def has_winners(wnrs) -> bool:
        print(wnrs)
        return count_winners(wnrs) != 0

    def construct_cards(arg_winners):
        new_cards = {}
        for key, val in arg_winners.items():
            for v in val:
                new_cards[v] = cards[v]
        return new_cards

    win_counter = 0
    winners_counters = []

    collect_winners(cards, winners)
    if has_winners(winners):
        win_counter += 1
        winners_counters.append(count_winners(winners))

    new_cards = construct_cards(winners)
    new_winners = {k: [] for k in cards.keys()}
    collect_winners(new_cards, new_winners)

    while True:
        if not has_winners(new_winners):
            break
        new_cards = construct_cards(new_winners)
        new_winners = {k: [] for k in cards.keys()}
        collect_winners(new_cards, new_winners)
        if count_winners(new_winners) == 0:
            break
        winners_counters.append(count_winners(new_winners))
        win_counter += 1
    print(win_counter, winners_counters)
    print(new_winners)
    total = count_winners(winners) + winners_counters[-1]
    print(total)

    # star 2
    return 0


def check() -> int:
    tmp_infile: TextIO
    infile: TextIO

    TMP_FILEPATH = os.path.join('days', 'tmp_day4')
    with open(TMP_FILEPATH) as tmp_infile:
        assert (part1(tmp_infile) == 13)
    with open(TMP_FILEPATH) as tmp_infile:
        assert (part2(tmp_infile) == 30)

    FILEPATH = os.path.join('input', 'day4')
    with open(FILEPATH) as infile:
        assert (part1(infile) == 22674)
    with open(FILEPATH) as infile:
        assert (part2(infile) == 5747443)

    return 0


"""
card_wins, card_have = map(str.split, row.split('|'))
matches = set(card_wins) & set(card_have)
print(matches, card_wins, card_have)
    {'48', '83', '17', '86'} ['Card', '1:', '41', '48', '83', '86', '17'] ['83', '86', '6', '31', '17', '9', '48', '53']
    {'61', '32'} ['Card', '2:', '13', '32', '20', '16', '61'] ['61', '30', '68', '82', '17', '32', '24', '19']
    {'21', '1'} ['Card', '3:', '1', '21', '53', '59', '44'] ['69', '82', '63', '72', '16', '21', '14', '1']
    {'84'} ['Card', '4:', '41', '92', '73', '84', '69'] ['59', '84', '76', '51', '58', '5', '54', '83']
    set() ['Card', '5:', '87', '83', '26', '28', '32'] ['88', '30', '70', '12', '93', '22', '82', '36']
    set() ['Card', '6:', '31', '18', '13', '56', '72'] ['74', '77', '10', '23', '35', '67', '36', '11']
    
p1 = 14
p2 = 30
"""
