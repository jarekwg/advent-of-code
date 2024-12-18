GRID_SIZE = 71
BYTES_FALLEN = 1024


corrupted: list[tuple[int, int]] = [
    tuple(map(int, line.split(","))) for line in open("18").read().splitlines()
]

obstacles = set(corrupted[:BYTES_FALLEN])


def shortest_path(obstacles: set[tuple[int, int]]) -> int | None:
    # Prep grid
    grid = [
        [0 if (x, y) not in obstacles else -1 for x in range(GRID_SIZE)]
        for y in range(GRID_SIZE)
    ]

    # Paint the grid
    cur = {(GRID_SIZE - 1, GRID_SIZE - 1)}
    steps = 0
    while cur:
        next = set()
        for x, y in cur:
            if grid[y][x] != 0:
                continue
            grid[y][x] = steps
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    next.add((nx, ny))
        cur = next
        steps += 1
    return grid[0][0]


print(f"Part 1: {shortest_path(obstacles)}")

# Many optimisations possible (eg only recalculating the path if an obstacle falls on our current shortest), but meh this is fine.
extra_falls = 0
while shortest_path(obstacles) != 0:
    extra_falls += 1
    obstacles = set(corrupted[: BYTES_FALLEN + extra_falls])

print(f"Part 2: {corrupted[BYTES_FALLEN + extra_falls - 1]}")
