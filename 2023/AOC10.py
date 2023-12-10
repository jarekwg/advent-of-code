grid = []  # y, x -- 0,0 is top left
for i, line in enumerate(open("10")):
    grid.append(line.strip())
    if "S" in line:
        S = line.index("S") + i * 1j


def visualise(tiles: set[complex], notation: str) -> None:
    for y in range(0, len(grid) * 10, 5):
        for x in range(0, len(grid[0]) * 10, 5):
            p = x / 10 + y / 10 * 1j
            if p in tiles:
                print(notation, end="")
            else:
                print(".", end="")
        print()
    print()


def get_tile(p: complex) -> str | None:
    try:
        return grid[int(p.imag)][int(p.real)]
    except IndexError:
        return None


# Set up loop with first two tiles (note we're taking halfsteps in grid instead of full steps, to aid in solving p2 later.)
loop = [S]
if get_tile(S + 1) in ["J", "-", "7"]:
    loop.extend([S + 0.5, S + 1])
elif get_tile(S + 1j) in ["J", "|", "L"]:
    loop.extend([S + 0.5j, S + 1j])
else:
    loop.extend([S - 0.5, S - 1])

# Follow the loop around to know its length.
while (p := loop[-1]) != S:
    match get_tile(p):
        case "|":
            if p - 1j == loop[-3]:
                loop.extend([p + 0.5j, p + 1j])
            else:
                loop.extend([p - 0.5j, p - 1j])
        case "-":
            if p - 1 == loop[-3]:
                loop.extend([p + 0.5, p + 1])
            else:
                loop.extend([p - 0.5, p - 1])
        case "L":
            if p - 1j == loop[-3]:
                loop.extend([p + 0.5, p + 1])
            else:
                loop.extend([p - 0.5j, p - 1j])
        case "J":
            if p - 1j == loop[-3]:
                loop.extend([p - 0.5, p - 1])
            else:
                loop.extend([p - 0.5j, p - 1j])
        case "7":
            if p - 1 == loop[-3]:
                loop.extend([p + 0.5j, p + 1j])
            else:
                loop.extend([p - 0.5, p - 1])
        case "F":
            if p + 1 == loop[-3]:
                loop.extend([p + 0.5j, p + 1j])
            else:
                loop.extend([p + 0.5, p + 1])


print(f"Part 1: {len(loop) // 2}")

# We're going to paint all non-loop tiles which are outside the loop. Whatever is left is our tiles of interest.
# First, determine unpaintend tiles, adding an extra border around the edges, so that all the outside tiles stay connected.
loop_tiles = set(loop)
all_tiles = set()
for y in range(-10, (len(grid) + 1) * 10, 5):
    for x in range(-10, (len(grid[0]) + 1) * 10, 5):
        all_tiles.add(x / 10 + y / 10 * 1j)

unpainted_tiles = all_tiles - loop_tiles

# visualise(loop_tiles, "X")

# Now paint all the tiles outside the loop.
# Thanks to taking half-steps, our inner and outer regions will be completely contiguous.
tiles_outside_loop: set[complex] = set()
to_paint: set[complex] = {-1 - 1j}
while to_paint:
    cur = to_paint.pop()
    tiles_outside_loop.add(cur)
    unpainted_tiles.remove(cur)
    if (p := cur + -0.5j) in unpainted_tiles and p not in tiles_outside_loop:
        to_paint.add(p)
    if (p := cur + -0.5) in unpainted_tiles and p not in tiles_outside_loop:
        to_paint.add(p)
    if (p := cur + 0.5) in unpainted_tiles and p not in tiles_outside_loop:
        to_paint.add(p)
    if (p := cur + 0.5j) in unpainted_tiles and p not in tiles_outside_loop:
        to_paint.add(p)


tiles_inside_loop = all_tiles - loop_tiles - tiles_outside_loop

# visualise(tiles_outside_loop, "O")
# visualise(tiles_inside_loop, "I")

# Soln is count of all whole-numbered points inside loop.
print(
    f"Part 2: {len([*filter(lambda p: p.real % 1 == 0 and p.imag % 1 == 0, tiles_inside_loop)])}"
)
