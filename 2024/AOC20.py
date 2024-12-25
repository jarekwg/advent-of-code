from itertools import combinations, product

GRID: list[list[str | int]] = [
    list(row.replace("#", "█").replace(".", "░"))
    for row in open("20").read().splitlines()
]
START: tuple[int, int]
L, H = len(GRID[0]), len(GRID)
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
# Dicts for storing (x, y)->time, subdivided into 20x20 sections
PATH_BY_SECTIONS: list[list[dict[tuple[int, int], int]]] = [
    [{} for x in range(L // 20)] for y in range(H // 20)
]

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
        PATH_BY_SECTIONS[y // 20][x // 20][(x, y)] = i
        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < L and 0 <= ny < H and GRID[ny][nx] in {"S", "E", "░"}:
                next.append((nx, ny))
    cur = next
    i += 1


def display_grid(grid: list[list[str | int]]) -> None:
    # Display the grid, but quadruple the width, so that 4-digit numbers don't mess up the alignment
    for row in grid:
        print("".join("████" if c == "█" else f"{c:░>4}" for c in row))


# display_grid(GRID)


def count_cheats() -> tuple[int, int]:
    n_cheats_2 = 0
    n_cheats_20 = 0
    # Iterate over each section, running:
    # - combinations of all points within the section
    # - combinations of all points between this section and sections UR,R,DR,D
    for y, section_row in enumerate(PATH_BY_SECTIONS):
        for x, section in enumerate(section_row):
            # Points within the section
            for p1, p2 in combinations(section.keys(), 2):
                d = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
                if d <= 20:
                    time_saved = abs(section[p2] - section[p1]) - d
                    if time_saved >= 100:
                        n_cheats_20 += 1
                        if d <= 2:
                            n_cheats_2 += 1
            # Points between this section and adjacent sections
            for dx, dy in [(1, -1), (1, 0), (1, 1), (0, 1)]:
                if 0 <= x + dx < L // 20 and 0 <= y + dy < H // 20:
                    other_section = PATH_BY_SECTIONS[y + dy][x + dx]
                    for p1, p2 in product(section.keys(), other_section.keys()):
                        d = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
                        if d <= 20:
                            time_saved = abs(other_section[p2] - section[p1]) - d
                            if time_saved >= 100:
                                n_cheats_20 += 1
                                if d <= 2:
                                    n_cheats_2 += 1

    return n_cheats_2, n_cheats_20


c1, c2 = count_cheats()

print("Part 1", c1)
print("Part 2", c2)
