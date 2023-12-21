from functools import cache
from itertools import starmap


@cache
def count_possibilities(corrupted: str, checks: tuple[int, ...]) -> int:
    if not corrupted:
        return 0 if checks else 1
    if len(corrupted) < sum(checks) + len(checks) - 1:
        return 0  # Shortcircuit, as not possible to match anymore.
    if corrupted[0] == ".":
        return count_possibilities(corrupted[1:], checks)
    if checks:
        if len(corrupted) == checks[0] and len(checks) == 1:
            if corrupted.replace("?", "#") == "#" * checks[0]:
                return 1
        if len(corrupted) > checks[0]:
            if (
                corrupted[: checks[0]].replace("?", "#") == "#" * checks[0]
                and corrupted[checks[0]] in ".?"
            ):
                if corrupted[0] == "#":
                    return count_possibilities(corrupted[checks[0] + 1 :], checks[1:])
                else:
                    return count_possibilities(
                        corrupted[checks[0] + 1 :], checks[1:]
                    ) + count_possibilities(corrupted[1:], checks)
    if corrupted[0] == "?":
        return count_possibilities(corrupted[1:], checks)
    return 0


def line_to_tuple(line: str) -> tuple[str, tuple[int, ...]]:
    corrupted, checks_str = line.split()
    checks = tuple(map(int, checks_str.split(",")))
    return corrupted, checks


def quintuple(corrupted: str, checks: tuple[int, ...]) -> tuple[str, tuple[int, ...]]:
    return "?".join([corrupted] * 5), checks * 5


lines = open("12").readlines()

print(f"Part 1: {sum(starmap(count_possibilities, map(line_to_tuple, lines)))}")
print(
    f"Part 2: {sum(starmap(count_possibilities, starmap(quintuple, map(line_to_tuple, lines))))}"
)
