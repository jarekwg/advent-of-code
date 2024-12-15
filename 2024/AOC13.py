import re


def get_cost_of_all_prizes(with_conversion_error: bool) -> int:
    lines = open("13").read().splitlines()
    total = 0
    while True:
        line = lines.pop(0)
        Ax, Ay = re.match(r".*: X\+(\d+), Y\+(\d+)", line).groups()  # type: ignore[union-attr]
        Ax, Ay = int(Ax), int(Ay)
        line = lines.pop(0)
        Bx, By = re.match(r".*: X\+(\d+), Y\+(\d+)", line).groups()  # type: ignore[union-attr]
        Bx, By = int(Bx), int(By)
        line = lines.pop(0)
        Px, Py = re.match(r".*: X=(\d+), Y=(\d+)", line).groups()  # type: ignore[union-attr]
        Px, Py = (
            int(Px) + 10000000000000 * with_conversion_error,
            int(Py) + 10000000000000 * with_conversion_error,
        )
        nB = (Ax * Py - Ay * Px) / (Ax * By - Ay * Bx)
        nA = (Px - nB * Bx) / Ax
        if nA % 1 == 0 and nB % 1 == 0:
            total += int(3 * nA + nB)

        try:
            lines.pop(0)
        except IndexError:
            break
    return total


print(f"Part 1: {get_cost_of_all_prizes(with_conversion_error=False)}")
print(f"Part 2: {get_cost_of_all_prizes(with_conversion_error=True)}")
