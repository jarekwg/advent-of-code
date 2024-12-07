class C(complex):
    """Complex class, but snapped to integers."""

    def __add__(self, other: complex) -> "C":
        return C(super().__add__(other))

    @property
    def real(self) -> int:
        return int(super().real)

    @property
    def imag(self) -> int:
        return int(super().imag)


original_obstacles: set[C] = set()
original_guardpos: C
original_startdir: int
DIRECTIONS = [C(-1j), C(1), C(1j), C(-1)]

for y, line in enumerate(open("6")):
    for x, c in enumerate(line):
        match c:
            case "#":
                original_obstacles.add(C(x + y * 1j))
            case "^":
                original_guardpos = C(x + y * 1j)
                original_startdir = 0

max_x, max_y = x, y


class StuckInLoop(Exception):
    pass


# def display(obstacles, patrolled):
#     for y in range(max_y + 1):
#         for x in range(max_x + 1):
#             pos = C(x + y * 1j)
#             if pos in obstacles:
#                 print("#", end="")
#             elif pos in patrolled:
#                 print("x", end="")
#             else:
#                 print(" ", end="")
#         print()
#     print()


def find_way_out(guardpos: C, guarddir: int, obstacles: set[C]) -> dict[C, set[int]]:
    patrolled: dict[C, set[int]] = dict()  # Position: set(Direction)
    while 0 <= guardpos.real <= max_x and 0 <= guardpos.imag <= max_y:
        while guardpos + DIRECTIONS[guarddir] in obstacles:
            guarddir = (guarddir + 1) % 4
        if guardpos in patrolled and guarddir in patrolled[guardpos]:
            raise StuckInLoop
        patrolled.setdefault(guardpos, set()).add(guarddir)
        guardpos += DIRECTIONS[guarddir]
    return patrolled


original_patrolled = find_way_out(
    original_guardpos, original_startdir, original_obstacles
)
loop_oppos: set[C] = set()

for pos in original_patrolled.keys():
    if pos != original_guardpos:
        try:
            find_way_out(
                original_guardpos,
                original_startdir,
                original_obstacles | {pos},
            )
        except StuckInLoop:
            loop_oppos.add(pos)

print(f"Part 1: {len(original_patrolled)}")
print(f"Part 2: {len(loop_oppos)}")
