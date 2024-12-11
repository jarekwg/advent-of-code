topo_map = open("10").read().splitlines()

H, W = len(topo_map), len(topo_map[0])

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def count_reachable_nines(startpoints: set[tuple[int, int]], unique_paths: bool) -> int:
    counted = 0
    if startpoints == set():
        return 0
    nextpoints = set()
    for startpoint in startpoints:
        x, y = startpoint
        height = int(topo_map[y][x])
        if height == 9:
            counted += 1
        else:
            for dx, dy in DIRS:
                if 0 <= x + dx < W and 0 <= y + dy < H:
                    if int(topo_map[y + dy][x + dx]) == height + 1:
                        if unique_paths:
                            counted += count_reachable_nines(
                                {(x + dx, y + dy)}, unique_paths
                            )
                        else:
                            nextpoints.add((x + dx, y + dy))
    if not unique_paths:
        counted += count_reachable_nines(nextpoints, unique_paths)
    return counted


def evaluate_trailheads(unique_paths: bool) -> int:
    total = 0
    for y, row in enumerate(topo_map):
        for x, height in enumerate(row):
            if int(height) == 0:
                total += count_reachable_nines({(x, y)}, unique_paths)
    return total


print(f"Part 1: {evaluate_trailheads(False)}")
print(f"Part 2: {evaluate_trailheads(True)}")
