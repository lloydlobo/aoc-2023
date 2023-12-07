from sys import exit

from days import day1, day2, day3


def main() -> int:
    assert (day3.check() == 0)
    assert (day2.check() == 0)
    assert (day1.check() == 0)
    return 0


if __name__ == '__main__':
    exit(main())
