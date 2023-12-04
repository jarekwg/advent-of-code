import re
from collections import defaultdict

lines = open("4").readlines()


def get_card_matches(card_str: str) -> tuple[int, int]:
    card_info = re.match(
        r"Card\s+(?P<card_no>\d+):(?P<winning_numbers>(?:\s+\d+)+)\s+\|(?P<picked_numbers>(?:\s+\d+)+)",
        card_str.strip(),
    ).groupdict()
    winning_numbers = set(card_info["winning_numbers"].split())
    picked_numbers = set(card_info["picked_numbers"].split())
    return int(card_info["card_no"]), len(winning_numbers & picked_numbers)


card_counts: dict[int, int] = defaultdict(lambda: 1)


def get_points_for_matches(card_matches: tuple[int, int]) -> int:
    card_no, matches = card_matches
    increment = card_counts[
        card_no
    ]  # Note that this has to happen outside the loop, to lock in the value in the defaultdict
    for i in range(matches):
        card_counts[card_no + i + 1] += increment
    return 2**matches // 2


print(f"Part 1: {sum(map(get_points_for_matches, map(get_card_matches, lines)))}")
print(f"Part 2: {sum(card_counts.values())}")
