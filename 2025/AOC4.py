grid = [list(l) for l in open("4").read().splitlines()]

X, Y = len(grid[0]), len(grid)

def is_roll(cell: str) -> bool:
    return cell == "@"

def is_accessible(x, y) -> bool:
    n_roll_neighbours = 0
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
        if 0 <= x + dx < X and 0 <= y + dy < Y:
            if is_roll(grid[y + dy][x + dx]):
                n_roll_neighbours += 1
    return n_roll_neighbours < 4

def remove_rolls() -> tuple[int, list[list[str]]]:
    """Returns the number of rolls removed and the new grid."""
    tot_moveable = 0
    new_grid = [list(row) for row in grid]
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if is_roll(cell) and is_accessible(x, y):
                new_grid[y][x] = "."
                tot_moveable += 1
    return tot_moveable, new_grid

removed_array = []
while (res := remove_rolls())[0] > 0:
    removed, new_grid = res
    removed_array.append(removed)
    grid = new_grid

print(f"Part 1: {removed_array[0]}")
print(f"Part 2: {sum(removed_array)}")