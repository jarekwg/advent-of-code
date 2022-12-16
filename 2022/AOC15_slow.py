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

covered = 0
for x in range(
    min((s.pos.x - s.range) for s in sensors),
    max((s.pos.x + s.range) for s in sensors) + 1,
):
    p = Point(x, Y_OF_INTEREST)
    if p in beaconpoints:
        continue
    for s in sensors:
        if manhattan(p, s.pos) <= s.range:
            covered += 1
            break
print(f"Part 1: {covered}")

for s in sensors:
    for p in s.get_points_on_boundary():
        for s in sensors:
            if manhattan(p, s.pos) <= s.range:
                break
        else:
            print(f"Part 2: {p.x * 4_000_000 + p.y}")
            exit()
