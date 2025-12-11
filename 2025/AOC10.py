import re
from collections import Counter
from functools import reduce
from operator import sub
from typing import Generator


def bits_to_int(bits: list[int]) -> int:
    value = 0
    for b in bits[::-1]:
        value = (value << 1) | b
    return value


def solve_line_part_1(
    target_indicator_lights: int,
    indicator_lights: int,
    avail_butttons: list[int],
    num_presses: int,
) -> int:
    if indicator_lights == target_indicator_lights:
        return num_presses
    if len(avail_butttons) == 0:
        return -1

    options = []
    # We press the next button in line
    if (
        res := solve_line_part_1(
            target_indicator_lights,
            indicator_lights ^ avail_butttons[0],
            avail_butttons[1:],
            num_presses + 1,
        )
    ) != -1:
        options.append(res)

    # We don't press it
    if (
        res := solve_line_part_1(
            target_indicator_lights, indicator_lights, avail_butttons[1:], num_presses
        )
    ) != -1:
        options.append(res)

    return min(options) if options else -1


def solve_part_1(line: str) -> int:
    indicator_lights_str, buttons_str, joltages_str = re.match(
        r"\[(?P<indicator_lights>[\.#]+)\] (?P<buttons>[^\{]+) \{(?P<joltages>[\d,]+)\}",
        line,
    ).groups()  # type: ignore
    # Convert everything to bit integers.
    buttons = [
        sum(2**i for i in map(int, s.strip("()").split(",")))
        for s in buttons_str.split()
    ]
    target_indicator_lights = bits_to_int(
        [1 if c == "#" else 0 for c in indicator_lights_str]
    )

    return solve_line_part_1(target_indicator_lights, 0, buttons, 0)


print(f"Part 1: {sum(solve_part_1(line) for line in open('10').read().splitlines())}")

######################################################################################


add_tuples = lambda a, b: tuple(map(sum, zip(a, b)))
sub_tuples = lambda a, b: tuple(map(sub, *(a, b)))
scale_button = lambda s, b: tuple(x * s for x in b.bits)


def split_into_buckets(k: int, n: int) -> Generator[tuple[int, ...], None, None]:
    """
    Yield all n-tuples of nonnegative integers summing to k.
    Order is lexicographic by first elements.
    """
    if n <= 0:
        return
    if n == 1:
        yield (k,)
        return

    for first in range(k + 1):
        for rest in split_into_buckets(k - first, n - 1):
            yield (first,) + rest


class Button:
    bits: tuple[int, ...]
    positions: tuple[int, ...]

    def __init__(self, positions: tuple[int, ...], size: int):
        self.bits = tuple(int(i in positions) for i in range(size))
        self.positions = positions

    def __repr__(self):
        return f"Button{self.positions}"


def solve_line_part_2(buttons: set[Button], target_joltage: tuple[int, ...]) -> int:
    if all(j == 0 for j in target_joltage):
        return 0
    if any(j < 0 for j in target_joltage):
        return -1
    if len(buttons) == 0:
        return -1

    # Determine "rarest" bits (ie bits that appear the least often on buttons).
    bit_counts = Counter(b for button in buttons for b in button.positions)
    rarest_bit = bit_counts.most_common()[-1][0]

    # Pick buttons that affect this bit.
    rarest_bit_buttons = {
        button for button in buttons if rarest_bit in button.positions
    }

    # Iterate over all the possible ways we can press these buttons.
    options = []
    for bucketing in split_into_buckets(
        target_joltage[rarest_bit], len(rarest_bit_buttons)
    ):
        joltages = list(map(scale_button, bucketing, rarest_bit_buttons))
        total_joltage = reduce(add_tuples, joltages)
        # And now when we recurse, we completely exclude the buttons we've just iterated.
        if (
            s := solve_line_part_2(
                buttons - rarest_bit_buttons, sub_tuples(target_joltage, total_joltage)
            )
        ) != -1:
            options.append(s + target_joltage[rarest_bit])
    return min(options) if options else -1


def solve_part_2(line: str) -> int:
    indicator_lights_str, buttons_str, joltages_str = re.match(
        r"\[(?P<indicator_lights>[\.#]+)\] (?P<buttons>[^\{]+) \{(?P<joltages>[\d,]+)\}",
        line,
    ).groups()  # type: ignore
    target_joltage = tuple(map(int, joltages_str.split(",")))
    buttons = {
        Button(tuple(map(int, s.strip("()").split(","))), len(target_joltage))
        for s in buttons_str.split()
    }
    print(buttons, target_joltage)
    print(Counter(p for button in buttons for p in button.positions))
    s = solve_line_part_2(buttons, target_joltage)
    print(s)
    return s


print(f"Part 2: {sum(solve_part_2(line) for line in open('10').read().splitlines())}")
