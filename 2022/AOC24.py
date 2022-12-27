MOVEMENT_DELTAS = {
    "<": -1,
    ">": 1,
    "^": -1j,
    "v": 1j,
    "_": 0,  # stay put
}


class C(complex):
    # Our own version of Python's `complex`, so that we can do some funky modding.
    # (And so that Im and Re return integers..)
    def __add__(self, other: complex) -> "C":
        return C(super().__add__(other))

    def __mod__(self, other: complex) -> "C":
        return C(self.real % other.real + (self.imag % other.imag) * 1j)

    @property
    def real(self) -> int:
        return int(super().real)

    @property
    def imag(self) -> int:
        return int(super().imag)


class Valley:
    blizzards = dict[C, list[str]]
    dimensions: C
    expediton = list[set[C]]
    targets: list[C]
    target_times = list[int]

    def __init__(self, input: list[str]) -> None:
        self.blizzards = {}
        for y, row in enumerate(input):
            for x, v in enumerate(row):
                if v in MOVEMENT_DELTAS:
                    self.blizzards.setdefault(C(x - 1 + (y - 1) * 1j), []).append(v)
        self.dimensions = C(x - 1 + (y - 1) * 1j)
        self.expedition = [{C(-1j)}]
        # Three targets: Finish line, then back to start for elf snacks, then finish again.
        self.targets = [self.dimensions - 1, C(-1j), self.dimensions - 1]
        self.target_times = []

    def draw(self) -> None:
        print(len(self.expedition) - 1, self.expedition[-1])
        print(
            ("#." if C(-1j) in self.expedition else "#E") + "#" * self.dimensions.real
        )
        for y in range(self.dimensions.imag):
            row = ""
            for x in range(self.dimensions.real):
                pos = C(x + y * 1j)
                row += (
                    b[0]
                    if len(
                        b := self.blizzards.get(
                            pos, "E" if pos in self.expedition[-1] else "."
                        )
                    )
                    == 1
                    else str(len(b))
                )
            print(f"#{row}#")
        print(
            "#" * self.dimensions.real
            + (".#" if self.dimensions - 1 not in self.expedition[-1] else "E#")
        )

    def tick(self) -> None:
        new_blizzards = {}
        for pos, blizzards in self.blizzards.items():
            for blizzard in blizzards:
                new_pos = pos + MOVEMENT_DELTAS[blizzard]
                new_blizzards.setdefault(new_pos % self.dimensions, []).append(blizzard)
        self.blizzards = new_blizzards
        self.paint_expedition()

    def paint_expedition(self) -> None:
        new_positions = set()
        # For each possible location the explorer might be at on this tick:
        for pos in self.expedition[-1]:
            # For each direction they may move (inc staying put):
            for delta in MOVEMENT_DELTAS.values():
                # If the potential new location is not occupied by a blizzard:
                if (new_pos := pos + delta) not in self.blizzards:
                    # If explorer has reached the target, ditch all other options, focus on next target.
                    if new_pos == self.targets[0]:
                        self.target_times.append(len(self.expedition))
                        self.expedition.append({self.targets.pop(0)})
                        return
                    # If explorer is at the start or finish, that's OK, record.
                    if new_pos in [C(-1j), self.dimensions - 1]:
                        new_positions.add(new_pos)
                    # Otherwise, if explorer's still on the grid, record.
                    elif (
                        0 <= new_pos.real < self.dimensions.real
                        and 0 <= new_pos.imag < self.dimensions.imag
                    ):
                        new_positions.add(new_pos)
        self.expedition.append(new_positions)


valley = Valley(open("24").readlines())
# valley.draw()
while valley.targets:
    valley.tick()
    # valley.draw()
    # input()

print(f"Part 1: {valley.target_times[0]}")
print(f"Part 2: {valley.target_times[-1]}")
