DATA = open("15").read()
WAREHOUSE_DATA, MOVEMENT_DATA = DATA.split("\n\n")
WAREHOUSE = [*map(list, WAREHOUSE_DATA.splitlines())]
WIDE_WAREHOUSE = [
    list(
        line.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.")
    )
    for line in WAREHOUSE_DATA.splitlines()
]
MOVEMENTS = MOVEMENT_DATA.replace("\n", "")
DIRS = {
    "<": (-1, 0),
    ">": (1, 0),
    "^": (0, -1),
    "v": (0, 1),
}


def can_move(warehouse: list[list[str]], x: int, y: int, dx: int, dy: int) -> bool:
    """Check if the object at location (x, y) can move to (x + dx, y + dy)."""
    # If there's a wall, return False (wall can't move).
    if warehouse[y][x] == "#":
        return False
    # If there's nothing, return True (nothing here, so something can step into it without issue).
    if warehouse[y][x] == ".":
        return True
    # If it's a large box moving vertically, check if the two cells it would move into can move.
    if dy != 0 and warehouse[y][x] in "[":
        return can_move(warehouse, x, y + dy, 0, dy) and can_move(
            warehouse, x + 1, y + dy, 0, dy
        )
    if dy != 0 and warehouse[y][x] in "]":
        return can_move(warehouse, x, y + dy, 0, dy) and can_move(
            warehouse, x - 1, y + dy, 0, dy
        )
    # If it's the robot, a small box, or a large box moving horizontally, it can only move if the next cell can move.
    return can_move(warehouse, x + dx, y + dy, dx, dy)


def do_move(warehouse, x: int, y: int, dx: int, dy: int) -> None:
    """Move the object at location (x, y) to (x + dx, y + dy)."""
    if dy != 0 and warehouse[y][x] == "[":
        do_move(warehouse, x, y + dy, 0, dy)
        do_move(warehouse, x + 1, y + dy, 0, dy)
        warehouse[y + dy][x] = "["
        warehouse[y + dy][x + 1] = "]"
        warehouse[y][x] = "."
        warehouse[y][x + 1] = "."
    elif dy != 0 and warehouse[y][x] == "]":
        do_move(warehouse, x, y + dy, 0, dy)
        do_move(warehouse, x - 1, y + dy, 0, dy)
        warehouse[y + dy][x] = "]"
        warehouse[y + dy][x - 1] = "["
        warehouse[y][x] = "."
        warehouse[y][x - 1] = "."
    elif warehouse[y][x] in "@O[]":
        do_move(warehouse, x + dx, y + dy, dx, dy)
        warehouse[y + dy][x + dx] = warehouse[y][x]
        warehouse[y][x] = "."


def move_all(warehouse: list[list[str]], movements) -> None:
    """Follow all the robot's movement instructions in the given warehouse."""
    # Get robot start pos.
    for y, row in enumerate(warehouse):
        if "@" in row:
            robot_pos = (row.index("@"), y)
            break

    for movement in movements:
        dx, dy = DIRS[movement]
        if can_move(warehouse, *robot_pos, dx, dy):
            do_move(warehouse, *robot_pos, dx, dy)
            # Update our knowledge of its position.
            robot_pos = (robot_pos[0] + dx, robot_pos[1] + dy)


def sum_of_box_GPS(warehouse: list[list[str]]) -> int:
    res = 0
    for y, row in enumerate(warehouse):
        for x, cell in enumerate(row):
            if cell in "O[":
                res += x + 100 * y
    return res


def move_all_and_score(warehouse: list[list[str]], movements: str) -> int:
    move_all(warehouse, movements)
    return sum_of_box_GPS(warehouse)


print(f"Part 1: {move_all_and_score(WAREHOUSE, MOVEMENTS)}")
print(f"Part 2: {move_all_and_score(WIDE_WAREHOUSE, MOVEMENTS)}")
