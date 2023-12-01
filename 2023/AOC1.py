import re

lines = open("1").read().split("\n")

digit_map = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}
for i in range(1, 10):
    digit_map[str(i)] = i


def get_digit(line: str, allow_spelled=False, from_right: bool = False) -> int:
    """Fetch first digit encountered in string.
    allow_spelled: consider digits that have been spelled out
    from_right: search from the back
    """
    op = lambda x: "".join(reversed(x)) if from_right else x
    pattern = "|".join(
        map(op, filter(lambda k: len(k) < 2 + 10 * allow_spelled, digit_map))
    )
    return digit_map[op(re.search(pattern, op(line)).group())]


def get_line_number(line, allow_spelled: bool):
    return get_digit(line, allow_spelled) * 10 + get_digit(line, allow_spelled, True)


def get_sum(allow_spelled: bool) -> int:
    return sum(get_line_number(line, allow_spelled) for line in lines)


print(f"Part 1: {get_sum(allow_spelled=False)}")
print(f"Part 2: {get_sum(allow_spelled=True)}")
