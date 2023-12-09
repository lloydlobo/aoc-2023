from utils import *


def part1(data):
    """
    Take each seed value and simply follow it down the chain of transformations

    The algorithm iterates over each block, where each block represents a mapping between two categories (e.g., seed-to-soil, soil-to-fertilizer, etc.).
    For each seed in the list, the algorithm checks which range in the mapping corresponds to the seed, and it calculates the new seed value based on the mapping.
    """
    seeds, *maps = data.split('\n\n')
    seeds = list(map(int, seeds.split(':')[1].split()))
    history = []
    for m in maps:
        ranges = [list(map(int, row.split())) for row in m.splitlines()[1:]]
        locations = []
        for seed in seeds:
            found = False
            loc = seed
            for dst, src, rng in ranges:
                if loc in range(src, src + rng + 1):
                    offset = (loc - src)
                    locations.append(dst + offset)
                    found = True
                    break
            if not found:  # Keep unchanged, if seed doesn't match any range
                locations.append(loc)
        history.append(seeds)
        seeds = locations

    pprint(history)
    pprint(seeds)
    p1 = min(seeds)
    print(p1)


def part1x(data):
    """
    1. **Seeds and Block Information:**
       - `seeds: [79, 14, 55, 13] | block: 'seed-to-soil map:
            \\n50 98 2\\n52 50 48'`
       - The initial seeds and the current block being processed
            (seed-to-soil map) are printed.
    2. **Individual Seed Processing within the Block:**
       - For each seed within the block, the seed value and the updated
            `new_seeds` list are printed.
       - Example:
         - `seed: 79, new_seeds: [81]`
         - Indicates that for seed 79, the new value is 81 after applying
                the seed-to-soil map.
    3. **Final Seeds and Block Information:** - After processing all seeds
    within the block, the updated seeds and the next block information are
    printed.
    4. **Minimum Value:** - Finally, the minimum value among the updated
    seeds is printed as the result.
    Let's analyze one example to illustrate:
    - For the first block (seed-to-soil map):
      - Seed 79 is transformed to 81 using the formula `(seed - src + dst)`.
      - Seed 14 remains unchanged (no matching range).
      - Seed 55 is transformed to 57 using the same formula.
      - Seed 13 remains unchanged.
      - The updated seeds become [81, 14, 57, 13].

    This process is repeated for each block, updating the seeds based on the
    specified maps. The final minimum value among the seeds is then printed,
    which, in this case, is 35.
    """
    seeds, *data_blocks = data.split('\n\n')
    seeds = list(map(int, seeds.split(':')[1].split()))

    for block in data_blocks:
        pprint(f'seeds: {seeds} | block: {repr(block)} ')
        ranges = [list(map(int, row.split())) for row in block.splitlines()[1:]]
        new_seeds = []

        for seed in seeds:

            found = False

            for dst, src, rng_len in ranges:
                pprint(
                    f'        [{src}:{src + rng_len + 1}] (src,src+rng_len+1)')
                if seed in range(src, src + rng_len + 1):
                    new_seed = seed - src + dst
                    pprint(
                        f'            new_seed: {new_seed} <- {seed}-{src}+{dst} :(seed-src+dst)')
                    new_seeds.append(new_seed)
                    found = True
                    break

            if not found:  # Keep unchanged, if seed doesn't match any range
                new_seeds.append(seed)

            pprint(f'    seed: {seed}, new_seeds: {new_seeds}')

        seeds = new_seeds

    p1 = min(seeds)
    print(p1)


# NOTE:
#   Every type of seed, soil, fertilizer and so on is identified with a
#   number, but numbers are reused by each category - that is, soil 123 and
#   fertilizer 123 aren't necessarily related to each other.

class RowMap:
    def __init__(self, dst_rng_start, src_rng_start, rng_len):
        self.dst_rng_start = dst_rng_start
        self.src_rng_start = src_rng_start
        self.rng_len = rng_len

    def describe(self) -> str:
        return f'{self.dst_rng_start}, {self.src_rng_start}, {self.rng_len}'

    def print(self):
        print(self.describe())


def part1_old(data: str):
    D: list[str] = data.splitlines()
    seeds_to_plant: list[int] = ints(D[0])

    # list of maps which describe how to convert numbers from a source
    # category into numbers in a destination category.
    keys = ['seed-to-soil map:', 'soil-to-fertilizer map:',
            'fertilizer-to-water map:', 'water-to-light map:',
            'light-to-temperature map:', 'temperature-to-humidity map:',
            'humidity-to-location map:']

    # That is, the section that starts with seed-to-soil map: describes how
    # to convert a seed number (the source) to a soil number (the destination).
    map_src_dst = {}

    cur_buf = []
    cur_key: None | str = None

    # Each line within a map contains three numbers: the destination range
    # start, the source range start, and the range length.

    for r, row in enumerate(D[1:]):
        if any(row.startswith(key) for key in keys):
            if cur_key and cur_buf:
                map_src_dst[cur_key] = cur_buf.copy()  # Avoid reference issues
                cur_buf.clear()

            cur_key = keys[keys.index(row.strip())]
        elif row.strip():  # Non-empty line
            rmap = [int(val) for val in row.split()]
            cur_buf.append(RowMap(rmap[0], rmap[1], rmap[2]))

        if cur_key and cur_buf:  # Check if there is a last key and buffer
            map_src_dst[cur_key] = cur_buf.copy()

    pprint(seeds_to_plant)
    pprint(map_src_dst)

    # Any source numbers that aren't mapped correspond to the same
    # destination number. So, seed number 10 corresponds to soil number 10.

    for key, val in map_src_dst.items():
        print(key)
        for row_map in val:
            print('\t', row_map.describe())

    p1 = 0

    print(p1)


def part2(data: str):
    D: str = data.strip()

    p2 = 0

    print(p2)


check_test(part1, part2)
# check(part1, part2)

# - Gardener seeks help with water shortage and decoding the Island Island
# Almanac.
# - Almanac details seeds, soil, fertilizer, water, light, temperature,
# humidity, and location using numerical identifiers.
# - Maps illustrate conversions between categories, covering entire ranges of
# numbers.
# - Objective: Find the lowest location number for initial seeds (79, 14, 55,
# 13).
# - Convert each seed through categories until identifying the corresponding
# location number.
#
# - Example:
# Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature # 78,
#   humidity 78, location 82.
# Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42,
#   humidity 43, location 43.
# Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82,
#   humidity 82, location 86.
# Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34,
#   humidity 35, location 35.
#   - Seed 79 → Location 82
#   - Seed 14 → Location 43
#   - Seed 55 → Location 86
#   - Seed 13 → Location 35
#
# - Lowest location number: 35.

"""
Seeds and Block Information:
- seeds: [79, 14, 55, 13] | block: 'seed-to-soil map:\n50 98 2\n52 50 48'
Individual Seed Processing within the Block:
- seed: 79, new_seeds: [81]     [50:99] (src, src+rng_len+1)
- seed: 14, new_seeds: [81, 14] [52:55] (src, src+rng_len+1)
- seed: 55, new_seeds: [81, 14, 57] [50:99] (src, src+rng_len+1)
- seed: 13, new_seeds: [81, 14, 57, 13] [52:55] (src, src+rng_len+1)
Final Seeds and Block Information:
- Updated seeds: [81, 14, 57, 13]
- Next block: 'soil-to-fertilizer map:\n0 15 37\n37 52 2\n39 0 15'
...
Minimum Value:
- Result: 35

"seeds: [79, 14, 55, 13] | block: 'seed-to-soil map:\\n50 98 2\\n52 50 48' "
'    seed: 79, new_seeds: [81]'
'    seed: 14, new_seeds: [81, 14]'
'    seed: 55, new_seeds: [81, 14, 57]'
'    seed: 13, new_seeds: [81, 14, 57, 13]'
("seeds: [81, 14, 57, 13] | block: 'soil-to-fertilizer map:\\n0 15 37\\n37 52 "
 "2\\n39 0 15' ")
'    seed: 81, new_seeds: [81]'
'    seed: 14, new_seeds: [81, 53]'
'    seed: 57, new_seeds: [81, 53, 57]'
'    seed: 13, new_seeds: [81, 53, 57, 52]'
("seeds: [81, 53, 57, 52] | block: 'fertilizer-to-water map:\\n49 53 8\\n0 11 "
 "42\\n42 0 7\\n57 7 4' ")
'    seed: 81, new_seeds: [81]'
'    seed: 53, new_seeds: [81, 49]'
'    seed: 57, new_seeds: [81, 49, 53]'
'    seed: 52, new_seeds: [81, 49, 53, 41]'
"seeds: [81, 49, 53, 41] | block: 'water-to-light map:\\n88 18 7\\n18 25 70' "
'    seed: 81, new_seeds: [74]'
'    seed: 49, new_seeds: [74, 42]'
'    seed: 53, new_seeds: [74, 42, 46]'
'    seed: 41, new_seeds: [74, 42, 46, 34]'
("seeds: [74, 42, 46, 34] | block: 'light-to-temperature map:\\n45 77 23\\n81 "
 "45 19\\n68 64 13' ")
'    seed: 74, new_seeds: [78]'
'    seed: 42, new_seeds: [78, 42]'
'    seed: 46, new_seeds: [78, 42, 82]'
'    seed: 34, new_seeds: [78, 42, 82, 34]'
("seeds: [78, 42, 82, 34] | block: 'temperature-to-humidity map:\\n0 69 1\\n1 "
 "0 69' ")
'    seed: 78, new_seeds: [78]'
'    seed: 42, new_seeds: [78, 43]'
'    seed: 82, new_seeds: [78, 43, 82]'
'    seed: 34, new_seeds: [78, 43, 82, 35]'
("seeds: [78, 43, 82, 35] | block: 'humidity-to-location map:\\n60 56 37\\n56 "
 "93 4' ")
'    seed: 78, new_seeds: [82]'
'    seed: 43, new_seeds: [82, 43]'
'    seed: 82, new_seeds: [82, 43, 86]'
'    seed: 35, new_seeds: [82, 43, 86, 35]'
35
"""
