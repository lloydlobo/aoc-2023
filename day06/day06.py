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
        ways = []
        for t_hold in range(1, t):
            # - Calculate the distance covered during button hold
            # - Calculate the distance covered after releasing the button
            # - _d_total = _s_button_hold + s_release_inertia
            _s_button_hold = (u * t_hold) + (0.5 * acc * (t_hold ** 2))
            v_last_accelerated_speed, t_remaining = acc * t_hold, t - t_hold
            s_release_inertia = v_last_accelerated_speed * t_remaining
            if s_release_inertia > d_record:
                ways.append(t_hold)
        p1 *= len(ways)
    pprint(p1)


def part2(data):
    """
    Example from before:
    Time:      7  15   30
    Distance:  9  40  200
    ...now instead means this:
    Time:      71530
    Distance:  940200
    """
    D = data.strip()
    time, dist = [ints(line.split(':')[1].strip()) for line in D.splitlines()]
    race_t = int(''.join(list(map(str, time))))
    race_record_d = int(''.join(list(map(str, dist))))
    _u = 0  # initial velocity
    acc = 1  # Each millisecond = 1 mm / s speed increase
    p2 = 1  # Total ways
    # - d_release_inertia = v_last_accelerated_speed * t_remaining
    #                       (acc * t_hold)             (t - t_hold)
    ways = [hold_t for hold_t in range(0, race_t) if
            ((acc * hold_t) * (race_t - hold_t)) > race_record_d]
    p2 *= len(ways)
    print(p2)


check_test(part1, part2)
check(part1, part2)

"""
LLM Summary:

**Problem (Time: 7 15 30, Distance: 9 40 200):**

Three boat races with varying durations and record distances. Win each race
by holding a button that accelerates the boat. Longer hold = faster boat,
but release before the race ends, otherwise boat won't move.

**Assumptions:**

- Boat starts from rest (initial velocity = 0).
- Holding increases speed at 1 mm/s per millisecond (constant acceleration).
- Calculate distance during button hold and remaining time.

**Solution:**

1. **Analyze each race:**
    - Find minimum/maximum hold times to beat the record.
    - Count valid hold times within that range.
    - Multiply valid hold times for each race.

2. **Winning Distance Calculation:**

    - Use displacement formula: s = ut + (1/2)at^2.
    - Split total race time: hold_time + (race_duration - hold_time).
    - Winning distance: s_winning = (hold_time) * (race_duration - hold_time).
    - Check if (hold_time * (race_duration - hold_time)) > d (record distance)
      to confirm if hold time allows beating the record.

**Code:**

- Two functions: `part1` and `part2`.
- Similar logic, take race data as input.
- `part1`: explicit calculations for distance and winning condition.
- `part2`: condensed calculation using winning distance equation.
- `check_test` and `check` functions for testing and validation.

**Key Points:**

- Code uses kinematics to calculate winning distance based on hold time.
- Find valid hold times for each race to cover a distance > record.
- Total ways to win = product of valid hold times for each race.

**Improvements:**

- Supplement explanation with diagrams for distance visualization.
- Optimize code for increased efficiency.
"""
