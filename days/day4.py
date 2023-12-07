import os
from typing import TextIO

TMP_FILEPATH = os.path.join('days', 'tmp_day4')
FILEPATH = os.path.join('input', 'day4')


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

    return total_pts


def part2(infile: TextIO) -> int:
    grid = list(infile)
    return 0


def check() -> int:
    tmp_infile: TextIO
    infile: TextIO

    with open(TMP_FILEPATH) as tmp_infile:
        assert (part1(tmp_infile) == 13)
        assert (part2(tmp_infile) == 0)

    with open(FILEPATH) as infile:
        assert (part1(infile) == 22674)
    #     assert (part2(infile) == 0)

    return 0
