class C(complex):
    """Complex class, but snapped to integers."""

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


DIRECTIONS = [C(1), C(-1), C(1j), C(-1j)]
CYCLE = 5

walkable: set[C] = set()
elfpositions: list[set[C]] = []


for y, line in enumerate(open("21")):
    for x, c in enumerate(line):
        if c in "S.":
            walkable.add(C(x + y * 1j))
            if c == "S":
                elfpositions.append({C(x + y * 1j)})

assert x == y
SIZE = x + 1


def print_elfpositions(elfpositions: set[C]) -> None:
    minx = -(-min(elfpositions, key=lambda p: p.real).real // SIZE) * SIZE
    maxx = max(elfpositions, key=lambda p: p.real).real // SIZE * SIZE
    miny = -(-min(elfpositions, key=lambda p: p.imag).imag // SIZE) * SIZE
    maxy = max(elfpositions, key=lambda p: p.imag).imag // SIZE * SIZE
    for y in range(-SIZE * CYCLE, SIZE * (CYCLE + 1)):
        for x in range(-SIZE * CYCLE, SIZE * (CYCLE + 1)):
            p = C(x + y * 1j)
            if p in elfpositions:
                if x >= maxx - SIZE and 0 <= y < SIZE:
                    print("E", end="")
                elif x < minx + SIZE and 0 <= y < SIZE:
                    print("W", end="")
                elif y < miny + SIZE and 0 <= x < SIZE:
                    print("N", end="")
                elif y >= maxy - SIZE and 0 <= x < SIZE:
                    print("S", end="")
                elif x >= SIZE and y < miny + SIZE:
                    print("L", end="")
                elif x >= SIZE and y >= maxy - SIZE:
                    print("F", end="")
                elif x < 0 and y >= maxy - SIZE:
                    print("7", end="")
                elif x < 0 and y < miny + SIZE:
                    print("J", end="")
                elif 0 <= x < SIZE and 0 <= y < SIZE:
                    print("C", end="")
                else:
                    print("O", end="")
            elif p % C(SIZE + SIZE * 1j) in walkable:
                print(".", end="")
            else:
                print("#", end="")
        print()
    print()


def get_bits(elfpositions: set[C]) -> tuple[int, int, int]:
    minx = -(-min(elfpositions, key=lambda p: p.real).real // SIZE) * SIZE
    maxx = max(elfpositions, key=lambda p: p.real).real // SIZE * SIZE
    miny = -(-min(elfpositions, key=lambda p: p.imag).imag // SIZE) * SIZE
    maxy = max(elfpositions, key=lambda p: p.imag).imag // SIZE * SIZE
    tips = 0
    triangles = 0
    centre = 0
    for y in range(-SIZE * CYCLE, SIZE * (CYCLE + 1)):
        for x in range(-SIZE * CYCLE, SIZE * (CYCLE + 1)):
            p = C(x + y * 1j)
            if p in elfpositions:
                if x >= maxx - SIZE and 0 <= y < SIZE:
                    tips += 1
                elif x < minx + SIZE and 0 <= y < SIZE:
                    tips += 1
                elif y < miny + SIZE and 0 <= x < SIZE:
                    tips += 1
                elif y >= maxy - SIZE and 0 <= x < SIZE:
                    tips += 1
                elif x >= SIZE and y < miny + SIZE:
                    triangles += 1
                elif x >= SIZE and y >= maxy - SIZE:
                    triangles += 1
                elif x < 0 and y >= maxy - SIZE:
                    triangles += 1
                elif x < 0 and y < miny + SIZE:
                    triangles += 1
                elif 0 <= x < SIZE and 0 <= y < SIZE:
                    centre += 1
    return tips, triangles, centre


for _ in range(100):
    cur_positions = elfpositions[-1]
    new_positions: set[C] = set()
    for p in cur_positions:
        for d in DIRECTIONS:
            if (p + d) % C(SIZE + SIZE * 1j) in walkable:
                new_positions.add(p + d)
    elfpositions.append(new_positions)
    # print_elfpositions(elfpositions[-1])
    # print(_ + 1, min(elfpositions[-1], key=lambda p: p.imag).imag)
    # input()
print_elfpositions(elfpositions[3 * SIZE + 1])
# print_elfpositions(elfpositions[4 * SIZE + 1])


def walkabout(n_steps: int) -> tuple[int, int]:
    tips, triangles, centre = get_bits(elfpositions[3 * SIZE + n_steps % SIZE])
    expansion = n_steps // SIZE - 1
    print(tips, triangles, centre, expansion)
    return (
        tips + triangles * expansion + centre * (expansion * 4 + 1),
        len(elfpositions[n_steps]),
    )


# print(f"Part 1: {walkabout(6)}")
print(f"Part 2: {walkabout(34)}")
print(f"Part 2: {walkabout(45)}")


# to get counts at step X
# first get counts at step 3 * SIZE + X % SIZE
# counts are 4 tips, 4 triangles, 1 full paint.
# expansion = miny // SIZE
# scaling is (4 tips) + (4 triangles) * expansion + (1 full paint) * (expansion * 4 + 1)
