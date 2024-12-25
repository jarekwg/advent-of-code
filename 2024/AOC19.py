import re
from functools import cache
from typing import Any

f = open("19")

PATTERNS = f.readline().strip().split(", ")
f.readline()
DESIGNS = f.read().splitlines()

pattern_re = re.compile("^(?:" + "|".join(PATTERNS) + ")+$")


pattern_tree: dict[str, Any] = {}
for pattern in PATTERNS:
    pos = pattern_tree
    while pattern:
        pos = pos.setdefault(pattern[0], {})
        pattern = pattern[1:]
    pos["$"] = None


@cache
def count_possible_towel_arrangements(design: str) -> int:
    if design == "":
        return 1
    pos = pattern_tree
    count = 0
    for i, c in enumerate(design):
        if c not in pos:
            return count
        pos = pos[c]
        if "$" in pos:
            count += count_possible_towel_arrangements(design[i + 1 :])
    return count


print("Part 1:", sum(bool(re.match(pattern_re, d)) for d in DESIGNS))
print("Part 2:", sum(map(count_possible_towel_arrangements, DESIGNS)))
