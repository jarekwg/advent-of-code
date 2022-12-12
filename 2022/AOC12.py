def printmap(map_: list[list[str]]) -> None:
    print(
        "\n".join(
            ["".join("." if x.isnumeric() else x for x in latline) for latline in map_]
        )
    )


def shortest_hike(start_elevation: str):
    heightmap: list[list[str]] = [
        list(latline.strip()) for latline in open("12").readlines()
    ]

    # Determine starting location(s) and end location.
    to_paint = []
    for y, latline in enumerate(heightmap):
        for x, elevation in enumerate(latline):
            if elevation == "E":
                end = (x, y)
            elif elevation == start_elevation:
                to_paint.append(((x, y), "a"))

    # Paint the land.
    def paint(
        loc: tuple[int, int], prev_elevation: str, n: int
    ) -> list[tuple[tuple[int, int], str]]:
        if not (0 <= loc[0] < len(heightmap[0]) and 0 <= loc[1] < len(heightmap)):
            # Let's stay on the grid.
            return []
        elevation = heightmap[loc[1]][loc[0]].replace("S", "a").replace("E", "z")
        if elevation.isnumeric():
            # Already been here, abort.
            return []
        elif ord(elevation) - ord(prev_elevation) > 1:
            # Too steep! Avoid getting out climbing gear.
            return []
        # Paint the location.
        heightmap[loc[1]][loc[0]] = str(n)
        # Explore where to paint next.
        next_to_paint = []
        for delta in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            next_loc = (loc[0] + delta[0], loc[1] + delta[1])
            next_to_paint.append((next_loc, elevation))
        return next_to_paint

    n = 0
    while heightmap[end[1]][end[0]] == "E":
        # printmap(heightmap)
        # input()
        next_to_paint = []
        for loc, prev_elevation in to_paint:
            next_to_paint.extend(paint(loc, prev_elevation, n))
        to_paint = next_to_paint
        n += 1
    return heightmap[end[1]][end[0]]


print(f"Part 1: {shortest_hike('S')}")
print(f"Part 2: {shortest_hike('a')}")
