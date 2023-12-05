import os.path
from sys import exit


def main():
    assert (day1() == 55002)


def day1() -> int:
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


if __name__ == '__main__':
    exit(main())
