from contextlib import suppress
from functools import reduce
from typing import Callable

reports = [list(map(int, r.split())) for r in open("2").readlines()]


class UnsafeReportError(Exception):
    def __init__(self, incompatible_levels: tuple[int, int]):
        self.incompatible_levels = incompatible_levels


def is_safe(tolerance_on: bool) -> Callable[[list[int]], bool]:
    def inner(report: list[int]) -> bool:
        def is_inc(a: int, b: int) -> int:
            if 1 <= report[b] - report[a] <= 3:
                return b

            raise UnsafeReportError((a, b))

        for levels in [
            list(range(len(report))),
            list(reversed(range(len(report)))),
        ]:
            try:
                reduce(is_inc, levels[1:], levels[0])
                return True
            except UnsafeReportError as e:
                if tolerance_on:
                    for i in e.incompatible_levels:
                        fixed_levels = (
                            levels[: levels.index(i)] + levels[levels.index(i) + 1 :]
                        )
                        with suppress(UnsafeReportError):
                            reduce(is_inc, fixed_levels[1:], fixed_levels[0])
                            return True
        return False

    return inner


print(f"Part 1: {sum(map(is_safe(tolerance_on=False), reports))}")
print(f"Part 2: {sum(map(is_safe(tolerance_on=True), reports))}")
