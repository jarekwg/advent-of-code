DIRS = {
    (0, 1): "B",
    (1, 0): "R",
    (0, -1): "A",
    (-1, 0): "L",
}
ANOTHER_DIMENSION = 2**10


def group_by_adjacency_and_label(
    to_explore: dict[tuple[int, int], str],
) -> list[set[tuple[int, int]]]:
    # Take a dict of point tuples mapped to some labels and groups adjacent points with the same label.
    # NOTE: Consumes the incoming dict!
    groups = []
    while to_explore:
        start, label = to_explore.popitem()
        to_process = {start}
        group = set()
        while to_process:
            x, y = to_process.pop()
            for dx, dy in DIRS:
                check = (x + dx, y + dy)
                if to_explore.get(check, "?") == label:
                    to_explore.pop(check)
                    to_process.add(check)
            group.add((x, y))
        groups.append(group)
    return groups


def identify_region_perimeters(
    region: set[tuple[int, int]],
) -> dict[tuple[int, int], str]:
    # Given a region of plots, identify the horizontal and vertical perimeters.
    perimeters = {}
    for x, y in region:
        for (dx, dy), label in DIRS.items():
            if (x + dx, y + dy) not in region:
                offset = 0 if label in "BA" else ANOTHER_DIMENSION
                perimeters[(x + offset + (dx > 0), y + (dy > 0))] = label
    return perimeters


def calc_region_fencing_cost(region: set[tuple[int, int]]) -> int:
    # Determine region area and perimeter and return the product.
    A = len(region)
    P = len(identify_region_perimeters(region))
    return A * P


def calc_region_discounted_fencing_cost(region: set[tuple[int, int]]) -> int:
    # Similar to above, however this time straight sections of perimeter count as 1.
    A = len(region)
    P = len(group_by_adjacency_and_label(identify_region_perimeters(region)))
    return A * P


plots_to_explore = {
    (x, y): plant
    for y, line in enumerate(open("12"))
    for x, plant in enumerate(line.strip())
}

regions = group_by_adjacency_and_label(plots_to_explore)

print(f"Part 1: {sum(map(calc_region_fencing_cost, regions))}")
print(f"Part 2: {sum(map(calc_region_discounted_fencing_cost, regions))}")
