import os


def check() -> int:
    assert (part1() == 55002)
    assert (part2() == 55093)
    return 0


def part2() -> int:
    """
    Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".
    Equipped with this new information, you now need to find the real first and last digit on each line. For example:
    two1nine
    eightwothree
    abcone2threexyz
    xtwone3four
    4nineeightseven2
    zoneight234
    7pqrstsixteen
    In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

    What is the sum of all of the calibration values?
    """
    # NOTE: data used is same as day1 part 1
    data: str
    with open(os.path.join('input', 'day1')) as infile:
        data = (infile.read()).strip()
    digits: list[str] = ['one', 'two', 'three', 'four', 'five', 'six', 'seven',
                         'eight', 'nine', ]
    total: int = 0
    for line in data.splitlines():
        first, last = None, None
        buf_first, buf_last = list(), list()
        for (f, l) in zip(line, line[::-1]):
            if first and last:
                break
            if first is None:
                if f.isdigit():
                    first = f
                if f.isalpha():
                    buf_first.append(f)
                    str_first = ''.join(buf_first)
                    for d in digits:
                        if d in str_first:
                            first = str(digits.index(d) + 1)
                            break
            if last is None:
                if l.isdigit():
                    last = l
                if l.isalpha():
                    buf_last.append(l)
                    str_last = ''.join(buf_last[::-1])
                    for d in digits:
                        if d in str_last:
                            last = str(digits.index(d) + 1)
                            break
        if first and last:
            total += int(f'{first}{last}')
    return total


def part1() -> int:
    """
    The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.
    For example:
    1abc2
    pqr3stu8vwx
    a1b2c3d4e5f
    treb7uchet
    In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

    Consider your entire calibration document. What is the sum of all of the calibration values?
    """
    data: str
    with open(os.path.join('input', 'day1')) as infile:
        data = (infile.read()).strip()
    total: int = 0
    for line in data.splitlines():
        first, last = None, None
        for (f, l) in zip(line, line[::-1]):
            if first and last:
                break
            if f.isdigit() and first is None:
                first = f
            if l.isdigit() and last is None:
                last = l
        if first and last:
            total += int(f'{first}{last}')
    return total
