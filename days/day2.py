# day2.py

"""
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

import os
from typing import Any


def check() -> int:
    assert (part1() == 2685)
    assert (part2() == 83707)
    return 0


def part1() -> int:
    data: str
    with open(os.path.join('input', 'day2')) as infile:
        data = (infile.read()).strip()

    # Given cube configuration (12 red, 13 green, 14 blue)
    win_config = dict(red=12, green=13, blue=14)
    colors = ['red', 'green', 'blue', ]

    games: dict[int, list[Any]] = dict()
    win_ids: list[int] = list()

    # Parse input text and clean it up
    for line in data.splitlines():
        idx, cfg_str = map(str.strip, line.split(':'))
        game_id = int(idx.replace('Game ', ''))
        games[game_id] = []
        for g in cfg_str.split(';'):
            game_arr: list[str] = list(map(str.strip, g.split(',')))
            rgb = dict(red=None, green=None, blue=None)
            for color in colors:
                for game_color in game_arr:
                    if color in game_color:
                        rgb[color] = int(game_color.replace(color, '').strip())
            games[game_id].append(rgb)

    # Visit each game and play it
    for key, val in games.items():
        is_valid = True

        for v in val:
            for c in colors:
                v_val = v.get(c)
                if v_val and v_val > win_config[c]:
                    is_valid = False
                    break
            if not is_valid:
                break

        if is_valid:
            win_ids.append(key)

    return sum(win_ids)


def part2() -> int:
    # NOTE: data used is same as part 1
    data: str
    with open(os.path.join('input', 'day2')) as infile:
        data = (infile.read()).strip()

    # Given cube configuration (12 red, 13 green, 14 blue)
    colors: list[str] = ['red', 'green', 'blue', ]

    games: dict[int, list[Any]] = dict()
    req_games: dict[int, dict[str, int]] = dict()

    # Parse input text and clean it up
    for line in data.splitlines():
        idx, cfg_str = map(str.strip, line.split(':'))
        game_id = int(idx.replace('Game ', ''))
        games[game_id] = []
        for g in cfg_str.split(';'):
            game_arr: list[str] = list(map(str.strip, g.split(',')))
            rgb = dict(red=None, green=None, blue=None)
            for color in colors:
                for game_color in game_arr:
                    if color in game_color:
                        rgb[color] = int(game_color.replace(color, '').strip())
            games[game_id].append(rgb)

    # For all winning game keys, find max num of rgb in each set.
    for key, val in games.items():
        max_rgb = dict(red=0, green=0, blue=0)
        for v in val:
            for c in colors:
                v_val = v.get(c)
                if v_val and (max_rgb.get(c) < v_val):
                    max_rgb[c] = v_val
        req_games[key] = max_rgb

    result = 0
    for _, v in req_games.items():
        cur = 1
        for c in colors:
            cur *= v[c]
        result += cur

    return result
