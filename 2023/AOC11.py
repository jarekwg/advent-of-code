from itertools import combinations, starmap
from operator import sub


class C(complex):
    # Complex class, but snapped to integers.
    def __sub__(self, other: complex) -> "C":
        return C(super().__sub__(other))

    def __abs__(self) -> int:
        # Manhattan distance today!
        return abs(self.real) + abs(self.imag)

    @property
    def real(self) -> int:
        return int(super().real)

    @property
    def imag(self) -> int:
        return int(super().imag)


# Read in galaxies.
galaxies: set[C] = set()
for y, line in enumerate(open("11")):
    for x, c in enumerate(line):
        if c == "#":
            galaxies.add(C(x + y * 1j))

# Read in positions of all expansions.
X_expansions = {x for x, line in enumerate(zip(*open("11"))) if "#" not in line}
Y_expansions = {y for y, line in enumerate(open("11")) if "#" not in line}


def dilate(galaxies: set[C], expansion: int) -> set[C]:
    return {
        C(
            (
                g.real
                + len({*filter(lambda p: p < g.real, X_expansions)}) * (expansion - 1)
            )
            + (
                g.imag
                + len({*filter(lambda p: p < g.imag, Y_expansions)}) * (expansion - 1)
            )
            * 1j
        )
        for g in galaxies
    }


def sum_lengths(galaxies: set[C]) -> int:
    return sum(map(abs, starmap(sub, combinations(galaxies, 2))))


print(f"Part 1: {sum_lengths(dilate(galaxies, 2))}")
print(f"Part 2: {sum_lengths(dilate(galaxies, 1000000))}")
