import cProfile

import numpy as np

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
    # print(p1)


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
    time, dist = [int(ljoins(ints(line.split(':')[1]))) for line in
                  D.splitlines()]
    accel = 1  # Each millisecond = 1 mm / s speed increase

    def __v1():
        # - d_release_inertia = v_last_accelerated_speed * t_remaining
        #                       (acc * t_hold)             (t - t_hold)
        ways = [hold_t for hold_t in range(0, time) if
                ((accel * hold_t) * (time - hold_t)) > dist]
        p2 = len(ways)  # Total ways
        # print(p2)

    def __v2():
        max_dist = [(accel * t_hold) * (time - t_hold) for t_hold in
                    range(time + 1)]
        p2 = sum([1 for t in range(time) if max_dist[t] > dist])
        # print(p2)

    def __v3():
        p2 = sum([1 for t_hold in range(time) if
                  (accel * t_hold) * (time - t_hold) > dist])
        # print(p2)

    def __v4():
        p2 = 0
        for t_hold in range(time):
            max_dist = (accel * t_hold) * (time - t_hold)
            if max_dist > dist:
                p2 += 1
        # print(p2)

    def __v5():
        """
        This version aims to optimize the calculation of valid hold times
        for winning boat races by leveraging NumPy for array operations.
        - `t_minus_t_hold`: Calculate the difference between the total race time
          and the current hold time for each possible hold time.
        - `t_win_holds`: Calculate the winning distance for each hold time using
          NumPy array operations.
        - `p2`: Count the number of hold times that result in a winning distance
          greater than the record distance.
        - Print the total count of valid hold times.
        Note:
        - The original code uses NumPy arrays for efficient vectorized operations.
        - This version is intended to be an optimized approach, but it may not
          perform well for very large numbers due to potential memory issues.
        Usage:
        - Call this function to print the total count of valid hold times for
          winning boat races based on the provided race duration and record distance.
        """
        np_arange = np.arange(time, dtype=np.int64)
        t_minus_t_hold = np.int64(time) - np_arange
        t_win_dist = (accel * np_arange) * t_minus_t_hold
        p2 = np.sum(t_win_dist > dist)  # Count the number of valid hold times
        # print(p2)

    prof = cProfile.Profile()
    prof.enable()
    __v1()
    prof.disable()
    prof.enable()
    __v2()
    prof.disable()
    prof.enable()
    __v3()
    prof.disable()
    prof.enable()
    __v4()
    prof.disable()
    prof.enable()
    __v5()
    prof.disable()
    prof.print_stats(sort='cumulative')
    pass  # endregion def part2(..):


# check_test(part1, part2)
check(part1, part2)

# testinput.txt
# """
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         1    0.018    0.018    0.019    0.019 day06.py:53(__v2)
#         1    0.017    0.017    0.017    0.017 day06.py:64(__v4)
#         1    0.014    0.014    0.014    0.014 day06.py:45(__v1)
#         1    0.013    0.013    0.014    0.014 day06.py:59(__v3)
#         1    0.001    0.001    0.001    0.001 day06.py:72(__v5)
# """

# input.txt
# """
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         1   26.533   26.533   27.039   27.039 day06.py:53(__v2)
#         1   15.379   15.379   15.394   15.394 day06.py:45(__v1)
#         1   14.699   14.699   14.699   14.699 day06.py:64(__v4)
#         1   14.092   14.092   14.433   14.433 day06.py:59(__v3)
#         1    1.502    1.502    2.492    2.492 day06.py:72(__v5)
# """

# testinput.txt + input.txt
# """
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         1   30.749   30.749   31.135   31.135 day06.py:54(__v2)
#         1   15.098   15.098   15.098   15.098 day06.py:45(__v1)
#         1   14.698   14.698   15.040   15.040 day06.py:60(__v3)
#         1   14.435   14.435   14.435   14.435 day06.py:65(__v4)
#         1    1.168    1.168    1.761    1.761 day06.py:73(__v5)
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         1   22.117   22.117   22.498   22.498 day06.py:54(__v2)
#         1   14.928   14.928   14.928   14.928 day06.py:45(__v1)
#         1   14.856   14.856   14.856   14.856 day06.py:65(__v4)
#         1   13.836   13.836   14.175   14.175 day06.py:60(__v3)
#         1    1.663    1.663    2.618    2.618 day06.py:73(__v5)
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         1   24.189   24.189   24.609   24.609 day06.py:54(__v2)
#         1   14.651   14.651   14.651   14.651 day06.py:65(__v4)
#         1   14.350   14.350   14.350   14.350 day06.py:45(__v1)
#         1   13.851   13.851   14.185   14.185 day06.py:60(__v3)
#         1    1.387    1.387    2.221    2.221 day06.py:73(__v5)
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         1   50.281   50.281   50.746   50.746 day06.py:53(__v2)
#         1   15.500   15.500   15.500   15.500 day06.py:45(__v1)
#         1   14.577   14.577   14.915   14.915 day06.py:59(__v3)
#         1   14.730   14.730   14.730   14.730 day06.py:64(__v4)
#         1    1.464    1.464    2.018    2.018 day06.py:72(__v5)
# """

"""
## LLM Summary:

**Problem:**

Three boat races with varying durations and record distances. The player wins by holding a button that accelerates the boat. The longer the button is held, the faster the boat goes, but it must be released before the race ends for the boat to move.

**Assumptions:**

* The boat starts from rest (initial velocity = 0).
* Holding the button increases speed at a constant rate of 1 mm/s per millisecond.
* The distance traveled is calculated using the displacement formula: s = ut + 1/2 * at^2.

**Solution:**

1. **Analyze each race:**
    * For each race, the code finds the minimum and maximum hold times that allow the boat to reach or exceed the record distance.
    * The code then counts the number of valid hold times within that range.
    * Finally, the number of valid hold times for each race is multiplied together to find the total number of ways to win all three races.

2. **Winning Distance Calculation:**
    * The code uses the displacement formula to calculate the winning distance for each possible hold time.
    * The total race time is split into two parts: the hold time and the remaining time after releasing the button.
    * The winning distance is calculated as the product of the hold time and the time remaining after release.
    * The code checks if the winning distance for a particular hold time is greater than the record distance. If it is, then that hold time is considered a valid option.

**Code:**

* The code is implemented in two functions: `part1` and `part2`.
* Both functions take the race data as input and have similar logic.
* `part1` uses explicit calculations for distance and the winning condition.
* `part2` uses a more concise approach by directly calculating the winning distance using the formula and comparing it to the record distance.
* Additional functions, `check_test` and `check`, are used for testing and validation.

**Key Points:**

* The code uses the concept of displacement and constant acceleration to calculate the winning distance based on the hold time.
* The code identifies valid hold times for each race that allow the boat to reach a distance exceeding the record.
* The total number of winning solutions is the product of the valid hold times across all races.

**Potential Improvements:**

* Supplement the explanation with diagrams or visualizations to illustrate the distance calculations.
* Explore optimization techniques to improve the code's efficiency for larger datasets.

**Additional Notes:**

* The provided code snippet includes profiling code to compare the performance of different approaches for calculating the winning distance.
* The code utilizes NumPy arrays for efficient vectorized operations in `part2`.
"""
