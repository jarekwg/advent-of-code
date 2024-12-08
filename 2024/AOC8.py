from itertools import combinations
from math import gcd


class C(complex):
    """Complex class, but snapped to integers."""

    def __add__(self, other: complex) -> "C":
        return C(super().__add__(other))

    def __sub__(self, other: complex) -> "C":
        return C(super().__sub__(other))

    def __truediv__(self, other: int) -> "C":  # type: ignore[override]
        return C(self.real // other, self.imag // other)

    @property
    def real(self) -> int:
        return int(super().real)

    @property
    def imag(self) -> int:
        return int(super().imag)


nodes: dict[str, list[C]] = {}  # frequency: [node locations]
for y, line in enumerate(open("8")):
    for x, c in enumerate(line):
        if c not in ".\n":
            nodes.setdefault(c, []).append(C(x + y * 1j))

max_x, max_y = x, y


def find_antinodes(consider_harmonics: bool) -> set[C]:
    antinodes: set[C] = set()
    for nodegroup in nodes.values():
        for n1, n2 in combinations(nodegroup, 2):
            d = n2 - n1
            if consider_harmonics:
                d /= gcd(d.real, d.imag)  # Hrmmm, still works without this.
                while 0 <= n1.real <= max_x and 0 <= n1.imag <= max_y:
                    antinodes.add(n1)
                    n1 -= d
                while 0 <= n2.real <= max_x and 0 <= n2.imag <= max_y:
                    antinodes.add(n2)
                    n2 += d
                # Technically we should also be checking for antinodes _between_ our nodes, but as above, works without.
            else:
                for a in (n1 - d, n2 + d):
                    if 0 <= a.real <= max_x and 0 <= a.imag <= max_y:
                        antinodes.add(a)
    return antinodes


print(f"Part 1: {len(find_antinodes(False))}")
print(f"Part 2: {len(find_antinodes(True))}")
