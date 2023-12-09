import re

from utils import *


def part1(data):
    """ Time:      7  15   30\nDistance:  9  40  200 """
    D = data.strip()
    time, dist = [ints(line.split(':')[1].strip()) for line in D.splitlines()]
    races = {t: d for t, d in zip(time, dist)}
    u = 0  # initial velocity
    acc = 1  # Each millisecond = 1 mm / s speed increase
    p1 = 1  # Total ways
    for t, d_record in races.items():
        ways = []  # ways = {}
        for t_hold in range(1, t):
            # Calculate the distance covered during button hold
            _s_button_hold = (u * t_hold) + (0.5 * acc * (t_hold ** 2))
            # Calculate the distance covered after releasing the button
            v_last_accelerated_speed, t_remaining = acc * t_hold, t - t_hold
            s_release_inertia = v_last_accelerated_speed * t_remaining
            # _d_total = _s_button_hold + s_release_inertia
            if s_release_inertia > d_record:
                ways.append(t_hold)  # ways[t_hold] = 1
        p1 *= len(ways)  # p1 *= sum(ways.values())
    pprint(p1)


def part2(data):
    p2 = 0

    print(p2)


check_test(part1, part2)
check(part1, part2)

"""
Time:      7  15   30
Distance:  9  40  200

The problem describes three races with different durations and record
distances. The objective is to determine the number of ways you can beat the
record in each race and then multiply these numbers together.

Longer button hold at start == faster boat.
   - Each millisecond = 1 mm/s speed increase.

Calculate the number of ways to beat the record for each race:

1. **First Race (7 ms, 9 mm):**
   - Since the current record is 9 mm, you can win by holding the button for at
     least 2 ms (9 - 7) up to 5 ms (9 + 7).
   - So, there are 4 ways to beat the record (2, 3, 4, or 5 milliseconds).

2. **Second Race (15 ms, 40 mm):**
   - You need to hold the button for at least 25 ms (40 - 15) up to
     11 ms (40 + 15) to beat the record.
   - Therefore, there are 8 ways to beat the record (from 4 to 11 milliseconds).

3. **Third Race (30 ms, 200 mm):**
   - To beat the record, you should hold the button for at least
     170 ms (200 - 30) up to 190 ms (200 + 30).
   - There are 9 ways to beat the record (from 11 to 19 milliseconds).

Finally, you multiply the number of ways for each race together 4 * 8 * 9 = 288.
So, the answer is 288.

The winning distance is calculated based on basic kinematics for constant acceleration.
The formula for displacement (s) under constant acceleration (a) and initial velocity (u) is:
s = ut + (1/2)at^2

In the boat race problem:
- Initial velocity (u) is assumed to be zero as the boat starts from rest.
- Constant acceleration (a) is related to the acceleration due to holding the button.

The time (t) is split into two parts: hold_time and (race_duration - hold_time).
Therefore, the winning distance calculation becomes:
s_winning = (hold_time) * (race_duration - hold_time)

This represents the distance covered during the time the button is held plus
the distance covered during the remaining time after releasing the button.

The condition (hold_time * (race_duration - hold_time)) > race_distance
checks if the winning distance is greater than the current record distance for the race.
If true, it indicates that holding the button for that amount of time will result
in covering a distance greater than the current record.

The condition `(hold_t * (t - hold_t)) > d` checks if the
winning distance, calculated based on the button hold time, is greater
than the record distance for the race.

Time Split:

hold_time: This is the duration for which the button is held down.
      During this time, the boat is accelerating.
(race_duration - hold_time): This represents the remaining time
      after releasing the button.
The boat, having been accelerated during the hold_time, continues to move
forward during the remaining time due to its inertia.
"""
