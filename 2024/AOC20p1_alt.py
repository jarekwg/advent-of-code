from typing import cast

GRID: list[list[str | int]] = [
    list(row.replace("#", "█").replace(".", "░"))
    for row in open("20").read().splitlines()
]
START: tuple[int, int]
L, H = len(GRID[0]), len(GRID)
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# Identify the start point (END is irrelevant)
for y, row in enumerate(GRID):
    if "S" in row:
        START = (row.index("S"), y)
        break

# Flood the the grid.
cur = [START]
i = 0
while cur:
    next = []
    for x, y in cur:
        GRID[y][x] = i
        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < L and 0 <= ny < H and GRID[ny][nx] in {"S", "E", "░"}:
                next.append((nx, ny))
    cur = next
    i += 1

# Identify walls where phasing would save time.
CHEATS_SAVING_100PS = 0
for y, row in enumerate(GRID):
    for x, c in enumerate(row):
        if c == "█":
            connectable_times = set()
            for dx, dy in DIRS:
                nx, ny = x + dx, y + dy
                if 0 <= nx < L and 0 <= ny < H and GRID[ny][nx] != "█":
                    connectable_times.add(cast(int, GRID[ny][nx]))
            if len(connectable_times) > 1:
                time_saved = max(connectable_times) - min(connectable_times) - 2
                if time_saved >= 100:
                    CHEATS_SAVING_100PS += 1


def display_grid(grid: list[list[str | int]]) -> None:
    # Display the grid, but quadruple the width, so that 4-digit numbers don't mess up the alignment
    for row in grid:
        print("".join("████" if c == "█" else f"{c:░>4}" for c in row))


# display_grid(GRID)

print("Part 1", CHEATS_SAVING_100PS)
