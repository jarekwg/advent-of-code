from collections import defaultdict
from functools import reduce

AIR = "."
ROCK = "#"
SAND = "o"


class Point(tuple):
    def from_str(point_str: str) -> "Point":
        return Point(map(int, point_str.split(",")))

    @property
    def x(self) -> int:
        return self[0]

    @property
    def y(self) -> int:
        return self[1]


class Cave:
    def __init__(self, rock_lines: list[list[Point]]):
        self.state: dict[Point, str] = defaultdict(lambda: AIR)
        self.depth = 0
        for rock_line in rock_lines:
            reduce(self.draw_rock_between_points, rock_line)

    def draw_rock_at_point(self, p: Point) -> None:
        self.state[p] = ROCK
        self.depth = max(self.depth, p.y)

    def draw_rock_between_points(self, p1: Point, p2: Point) -> Point:
        self.draw_rock_at_point(p1)
        while p1 != p2:
            p1 = Point(
                (
                    p1.x + (p2.x - p1.x) // abs(p2.x - p1.x or 1),
                    p1.y + (p2.y - p1.y) // abs(p2.y - p1.y or 1),
                )
            )
            self.draw_rock_at_point(p1)

        # Return p2, so that this function can be used in a `reduce` call. :3
        return p2

    def next_sand_unit_comes_to_rest(self, floor: bool) -> bool:
        p = Point((500, 0))
        while True:
            if self.state[p] == SAND or not floor and p.y == self.depth:
                return False
            if floor and p.y == self.depth + 1:
                self.state[p] = SAND
                return True
            elif self.state[(p2 := Point((p.x, p.y + 1)))] == AIR:
                p = p2
            elif self.state[(p2 := Point((p.x - 1, p.y + 1)))] == AIR:
                p = p2
            elif self.state[(p2 := Point((p.x + 1, p.y + 1)))] == AIR:
                p = p2
            else:
                self.state[p] = SAND
                return True

    def pour_sand(self, floor: bool) -> int:
        units_released = 0
        while self.next_sand_unit_comes_to_rest(floor):
            units_released += 1
        return units_released


rock_lines = [
    [*map(Point.from_str, line.strip().split(" -> "))]
    for line in open("14").readlines()
]
cave = Cave(rock_lines)
units_until_abyss = cave.pour_sand(floor=False)
cave = Cave(rock_lines)
units_until_full = cave.pour_sand(floor=True)

print(f"Part 1: {units_until_abyss}")
print(f"Part 2: {units_until_full}")
