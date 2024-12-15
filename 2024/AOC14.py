import re
from math import prod


class C(complex):
    """Complex class, but snapped to integers."""

    def __add__(self, other: complex) -> "C":
        return C(super().__add__(other))

    def __mod__(self, other: complex) -> "C":
        return C(self.real % other.real + (self.imag % other.imag) * 1j)

    def cycle(self) -> int:
        return self.real * self.imag

    @property
    def real(self) -> int:
        return int(super().real)

    @property
    def imag(self) -> int:
        return int(super().imag)


def _get_robots() -> list[dict[str, C]]:
    # Parse file to identify robot start positions and velocities
    robots = []
    for line in open("14").read().splitlines():
        px, py, vx, vy = re.match(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", line).groups()  # type: ignore[union-attr]
        robots.append(
            {
                "pos": C(int(px), int(py)),
                "vel": C(int(vx), int(vy)),
            }
        )
    return robots


TEST_SPACE_DIMS = C(11 + 7 * 1j)
PROD_SPACE_DIMS = C(101 + 103 * 1j)


def predict_safety_factor_after_n_seconds(n: int, dims: C) -> int:
    robots = _get_robots()

    # Skip superfluous cycles
    n %= dims.cycle()
    # Move robots
    while n:
        for robot in robots:
            robot["pos"] = (robot["pos"] + robot["vel"]) % dims
        n -= 1

    # Count robots in each quadrant
    quads = [0, 0, 0, 0]  # UL, UR, LL, LR
    for robot in robots:
        if robot["pos"].real < dims.real // 2:
            if robot["pos"].imag < dims.imag // 2:
                quads[0] += 1
            elif robot["pos"].imag > dims.imag // 2:
                quads[1] += 1
        elif robot["pos"].real > dims.real // 2:
            if robot["pos"].imag < dims.imag // 2:
                quads[2] += 1
            elif robot["pos"].imag > dims.imag // 2:
                quads[3] += 1
    return prod(quads)


def find_secs_to_easter_egg(dims: C) -> int:
    robots = _get_robots()

    def _display() -> None:
        positions = {robot["pos"] for robot in robots}
        for y in range(dims.imag):
            for x in range(dims.real):
                print("#" if C(x, y) in positions else ".", end="")
            print()

    # Prep times of interest (when strange concentrations occur..)
    h_times = [72]  # First time we see the horizontal concentration
    v_times = [93]  # First time we see the vertical concentration
    while h_times[-1] < dims.cycle() and v_times[-1] < dims.cycle():
        h_times.append(h_times[-1] + dims.imag)
        v_times.append(v_times[-1] + dims.real)
    times_of_interest = set(h_times + v_times)

    # Move robots
    secs = 0
    while secs < dims.cycle():
        for robot in robots:
            robot["pos"] = (robot["pos"] + robot["vel"]) % dims
        secs += 1
        if secs in times_of_interest:
            print(secs)
            _display()
            input()

    return secs


print(f"Part 1: {predict_safety_factor_after_n_seconds(100, PROD_SPACE_DIMS)}")
# For this second part, just keep iterating until you see the tree..
print(f"Part 2: {find_secs_to_easter_egg(PROD_SPACE_DIMS)}")
