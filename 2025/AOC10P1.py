import re


def bits_to_int(bits: list[int]) -> int:
    value = 0
    for b in bits[::-1]:
        value = (value << 1) | b
    return value


def count_min_presses_to_target(
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
        res := count_min_presses_to_target(
            target_indicator_lights,
            indicator_lights ^ avail_butttons[0],
            avail_butttons[1:],
            num_presses + 1,
        )
    ) != -1:
        options.append(res)

    # We don't press it
    if (
        res := count_min_presses_to_target(
            target_indicator_lights, indicator_lights, avail_butttons[1:], num_presses
        )
    ) != -1:
        options.append(res)

    return min(options) if options else -1


def solve_min_button_presses(line: str) -> int:
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

    return count_min_presses_to_target(target_indicator_lights, 0, buttons, 0)


print(
    f"Part 1: {sum(solve_min_button_presses(line) for line in open('10').read().splitlines())}"
)
