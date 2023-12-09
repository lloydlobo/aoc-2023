from typing import List, Any

from utils import *


def part1(data) -> int:
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
    D: list[str] = list(data.splitlines())

    cards = {(r + 1): [[int(num) for num in
                        nums.split(': ', 1)[-1].replace(' ', ',').split(',') if
                        num] for nums in row.split('|')] for r, row in
             enumerate(D)}
    p1 = 0  # Total points

    for win_nums, cur_nums in cards.values():
        pts = 0

        for _ in range(len(set(win_nums) & set(cur_nums))):
            if pts == 0:  # First round
                pts += 1
            else:
                pts *= 2

        p1 += pts
    print(p1)  # star 1


def part2(data) -> int:
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
    D: list[str] = list(data.splitlines())

    # Init dict with default values
    p1 = defaultdict(lambda: 0.5)  # First win is 1pt. next is 2*cur point
    p2 = defaultdict(lambda: 0.0)  # Total cards you end up with including cur

    for cur_idx, row in enumerate(D):
        win_nums, card_nums = map(str.split, row.split('|'))
        common_nums: set[str] = set(win_nums) & set(card_nums)

        p2[cur_idx] += 1.0  # Initialize with 1.0 for each first win

        for offset in range(len(common_nums)):
            p1[cur_idx] *= 2  # Doubling points for each match
            p2[cur_idx + offset + 1] += p2[cur_idx]  # Update running total

    total_points_p1 = sum(map(int, p1.values()))
    total_cards_p2 = sum(map(int, p2.values()))
    print(total_points_p1, total_cards_p2)

    return total_cards_p2  # star 2


check_test(part1, part2)
check(part1, part2)

"""
# day2.py

--- Day 2: Cube Conundrum ---

https://adventofcode.com/2023/day/2

--- Part 1 ---

To determine which games would have been possible with the given cube
configuration (12 red, 13 green, 14 blue), you need to check if the revealed
subsets in each game are consistent with these counts. If a subset in a game
exceeds the specified cube counts, that game is not possible.

For example, in Game 1, if the bag contained 12 red, 13 green, and 14 blue
cubes, it would be possible because the revealed subsets don't exceed these
counts.

If you continue this analysis for each game, you'll find that games 1, 2,
and 5 are possible, while games 3 and 4 are not. The sum of the IDs of the
possible games (1 + 2 + 5) is 8.

--- Part 2 ---

To find the minimum set of cubes for each game, you need to determine the
fewest number of cubes of each color required to make the game possible. This
is calculated by multiplying the minimum counts of red, green, and blue cubes
together.

Let's calculate the power for each game based on the provided information:
1. Game 1: Minimum set (4 red, 2 green, 6 blue) => Power = 4 * 2 * 6 = 48
2. Game 2: Minimum set (1 red, 3 green, 4 blue) => Power = 1 * 3 * 4 = 12
3. Game 3: Minimum set (20 red, 13 green, 6 blue) => Power = 20 * 13 * 6 = 1560
4. Game 4: Minimum set (14 red, 3 green, 15 blue) => Power = 14 * 3 * 15 = 630
5. Game 5: Minimum set (6 red, 3 green, 2 blue) => Power = 6 * 3 * 2 = 36

Now, add up these powers: 48 + 12 + 1560 + 630 + 36 = 2286.
Therefore, the sum of the powers of the minimum sets of cubes for each game
is 2286.

For each game, find the minimum set of cubes that must have been present.
What is the sum of the power of these sets?
"""
