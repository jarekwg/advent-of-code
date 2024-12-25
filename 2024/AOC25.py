from collections import Counter
from itertools import product
from typing import cast

schematics = open("25").read().split("\n\n")

Key = tuple[int, int, int, int, int]
Lock = tuple[int, int, int, int, int]

KEYS: list[Key] = []
LOCKS: list[Lock] = []


def parse_schematic(schematic: str) -> None:
    lines = schematic.splitlines()
    res = tuple(Counter(column)["#"] - 1 for column in zip(*lines))
    if lines[0] == "#" * 5:
        LOCKS.append(cast(Lock, res))
    else:
        KEYS.append(cast(Key, res))


for schematic in schematics:
    parse_schematic(schematic)


def is_valid_combo(key: Key, lock: Lock) -> bool:
    return all(key[i] + lock[i] <= 5 for i in range(5))


print("Part 1:", sum(is_valid_combo(key, lock) for key, lock in product(KEYS, LOCKS)))
