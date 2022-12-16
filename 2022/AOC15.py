from dataclasses import dataclass

Y_OF_INTEREST = 2_000_000

RANGE_OF_INTEREST = 4_000_000


@dataclass
class Point:
    x: int
    y: int

    def __eq__(self, other: "Point") -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


@dataclass
class Line:
    """y=mx+c, with finite ends. `m` omitted because it's always ±1, and we don't care for it here."""

    c: int
    x1: int
    x2: int


@dataclass
class Bracket:
    x: int
    opening: bool

    def __gt__(self, other: "Bracket") -> bool:
        return self.x > other.x


@dataclass
class Sensor:
    pos: Point
    range: int

    def get_points_on_boundary(self) -> set[Point]:
        points = set()
        x, y = self.pos.x, self.pos.y - self.range - 1
        while y != self.pos.y:
            x, y = x + 1, y + 1
            if 0 <= x <= RANGE_OF_INTEREST and 0 <= y <= RANGE_OF_INTEREST:
                points.add(Point(x, y))
        while x != self.pos.x:
            x, y = x - 1, y + 1
            if 0 <= x <= RANGE_OF_INTEREST and 0 <= y <= RANGE_OF_INTEREST:
                points.add(Point(x, y))
        while y != self.pos.y:
            x, y = x - 1, y - 1
            if 0 <= x <= RANGE_OF_INTEREST and 0 <= y <= RANGE_OF_INTEREST:
                points.add(Point(x, y))
        while x != self.pos.x:
            x, y = x + 1, y - 1
            if 0 <= x <= RANGE_OF_INTEREST and 0 <= y <= RANGE_OF_INTEREST:
                points.add(Point(x, y))
        return points


def manhattan(p1: Point, p2: Point) -> int:
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


# Parse input data.
sensors = []
beaconpoints = set()
for line in open("15").readlines():
    match line.replace("=", " ").replace(",", "").replace(":", "").split():
        case [
            "Sensor",
            "at",
            "x",
            sx,
            "y",
            sy,
            "closest",
            "beacon",
            "is",
            "at",
            "x",
            bx,
            "y",
            by,
        ]:
            beaconpoints.add(
                bp := Point(int(bx), int(by)),
            )
            sensors.append(
                Sensor(
                    sp := Point(int(sx), int(sy)),
                    manhattan(sp, bp),
                )
            )


def get_sensor_boundary_lines(
    outside: bool,
) -> tuple[list[Line], list[Line], list[Line], list[Line]]:
    # Sensors have a diamond-shaped boundary -- track this as 4 separate lines,
    # top-left, top-right, bottom-left, bottom-right.
    # If `outside` is True, return lines just outside the boundaries.
    TL: list[Line] = []
    TR: list[Line] = []
    BL: list[Line] = []
    BR: list[Line] = []
    for s in sensors:
        xL = s.pos.x - s.range - outside
        xR = s.pos.x + s.range + outside
        xT = xB = s.pos.x
        yL = yR = s.pos.y
        yT = s.pos.y + s.range + outside
        yB = s.pos.y - s.range - outside
        TL.append(Line((yL + yT - xL - xT) // 2, xL, xT))
        TR.append(Line((yR + yT + xR + xT) // 2, xT, xR))
        BL.append(Line((yL + yB + xL + xB) // 2, xL, xB))
        BR.append(Line((yR + yB - xR - xB) // 2, xB, xR))
    return TL, TR, BL, BR


# Part 1: How many points along y=2_000_000 do not contain a Beacon?
TL, TR, BL, BR = get_sensor_boundary_lines(outside=False)
# Determine x value of all lines that cross y=2_000_000, and whether
# it corresponds to the start or end of a range.
brackets: list[Bracket] = []
for line in TL:
    x = Y_OF_INTEREST - line.c
    if line.x1 <= x <= line.x2:
        brackets.append(Bracket(x, True))
for line in TR:
    x = line.c - Y_OF_INTEREST
    if line.x1 <= x <= line.x2:
        brackets.append(Bracket(x, False))
for line in BL:
    x = line.c - Y_OF_INTEREST
    if line.x1 <= x <= line.x2:
        brackets.append(Bracket(x, True))
for line in BR:
    x = Y_OF_INTEREST - line.c
    if line.x1 <= x <= line.x2:
        brackets.append(Bracket(x, False))

points_without_beacon = 0
opening_x = None
depth = 0
for bracket in sorted(brackets):
    if bracket.opening:
        depth += 1
        if depth == 1:
            opening_x = bracket.x
    else:
        depth -= 1
        if depth == 0:
            points_without_beacon += bracket.x - opening_x + 1
            # Subtract any beacons along this stretch.
            for beaconpoint in beaconpoints:
                if (
                    beaconpoint.y == Y_OF_INTEREST
                    and opening_x <= beaconpoint.x <= bracket.x
                ):
                    points_without_beacon -= 1
print(f"Part 1: {points_without_beacon}")

# Part 2: Where's the hidden beacon?
TL, TR, BL, BR = get_sensor_boundary_lines(outside=True)
# Aim is then to identify all points P, where at least one line from each list runs through P.
TLTR_intersections: list[Point] = []
for line1 in TL:
    for line2 in TR:
        P = Point((line2.c - line1.c) // 2, (line1.c + line2.c) // 2)
        if max(line1.x1, line2.x1) <= P.x <= min(line1.x2, line2.x2):
            for line3 in BL:
                if P.y + P.x == line3.c and line3.x1 <= P.x <= line3.x2:
                    for line4 in BR:
                        if P.y - P.x == line4.c and line4.x1 <= P.x <= line4.x2:
                            # OOH Final test! Is this point outside sensor range for all sensors?
                            for s in sensors:
                                if manhattan(P, s.pos) <= s.range:
                                    break
                            else:
                                print(f"Part 2: {P.x * 4_000_000 + P.y}")
                                exit()
