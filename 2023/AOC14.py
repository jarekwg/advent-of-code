class C(complex):
    """Complex class, but snapped to integers."""

    # def __sub__(self, other: complex) -> "C":
    #     return C(super().__sub__(other))

    # def __abs__(self) -> int:
    #     # Manhattan distance today!
    #     return abs(self.real) + abs(self.imag)

    @property
    def real(self) -> int:
        return int(super().real)

    @property
    def imag(self) -> int:
        return int(super().imag)


platform: dict[C, str] = {}

for y, line in enumerate(open("14")):
    for x, c in enumerate(line):
        platform[C(x + y * 1j)] = c
