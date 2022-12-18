ORTHOGONAL_ADJACENCY_DELTAS = [
    (0, 0, 1),
    (0, 0, -1),
    (0, 1, 0),
    (0, -1, 0),
    (1, 0, 0),
    (-1, 0, 0),
]
DIAGONAL_ADJACENCY_DELTAS = ORTHOGONAL_ADJACENCY_DELTAS + [
    (0, 1, 1),
    (0, 1, -1),
    (0, -1, 1),
    (0, -1, -1),
    # -
    (1, 0, 1),
    (1, 0, -1),
    (-1, 0, 1),
    (-1, 0, -1),
    # -
    (1, 1, 0),
    (1, -1, 0),
    (-1, 1, 0),
    (-1, -1, 0),
    # -
    (1, 1, 1),
    (1, 1, -1),
    (1, -1, 1),
    (1, -1, -1),
    (-1, 1, 1),
    (-1, 1, -1),
    (-1, -1, 1),
    (-1, -1, -1),
]


class Coord(tuple):
    @staticmethod
    def from_string(coord_str: str) -> "Coord":
        return Coord(map(int, coord_str.split(",")))

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(map(sum, zip(self, other)))


class Bubble(set[Coord]):
    def __init__(self, parent_set):
        super().__init__()
        self.parent_set = parent_set

    def trace(self, cube_coord: Coord) -> set[Coord]:
        if cube_coord in self:
            return set()
        self.add(cube_coord)
        to_trace = set()
        for delta in ORTHOGONAL_ADJACENCY_DELTAS:
            c = cube_coord + Coord(delta)
            if c in self.parent_set:
                if c not in self:
                    to_trace.add(c)
        return to_trace


# Calculate all lava & air cube coords.
lava_cube_coords = set()
air_cube_coords = set()
for line in open("18").readlines():
    cube_coord = Coord.from_string(line.strip())
    if cube_coord in air_cube_coords:
        air_cube_coords.remove(cube_coord)
    for delta in DIAGONAL_ADJACENCY_DELTAS:
        c = cube_coord + Coord(delta)
        if c not in lava_cube_coords:
            air_cube_coords.add(c)
    lava_cube_coords.add(cube_coord)

# Group all air cubes into orthogonally connected regions, "bubbles".
air_cube_coords_to_review = set(air_cube_coords)
air_bubbles = []
while air_cube_coords_to_review:
    cur_bubble = Bubble(parent_set=air_cube_coords)
    to_trace = {next(iter(air_cube_coords_to_review))}
    while to_trace:
        next_to_trace = set()
        for c in to_trace:
            next_to_trace |= cur_bubble.trace(c)
        to_trace = next_to_trace

    air_cube_coords_to_review -= cur_bubble
    air_bubbles.append(cur_bubble)

# Total surface area
# Any orthogonal touching between a lava cube and an air cube contributes to this count.
total_surface = 0
for lava_cube_coord in lava_cube_coords:
    for delta in ORTHOGONAL_ADJACENCY_DELTAS:
        c = lava_cube_coord + Coord(delta)
        if c in air_cube_coords:
            total_surface += 1

# Total external surface area
# Our largest air bubble must _necessarily_ be the "outside" one.
# Any orthogonal touching between a lava cube and an air cube in this air bubble contributes to this count.
outside_air_bubble = max(air_bubbles, key=lambda bubble: len(bubble))
total_exterior_surface = 0
for lava_cube_coord in lava_cube_coords:
    for delta in ORTHOGONAL_ADJACENCY_DELTAS:
        c = lava_cube_coord + Coord(delta)
        if c in outside_air_bubble:
            total_exterior_surface += 1

print(f"Part 1: {total_surface}")
print(f"Part 2: {total_exterior_surface}")
