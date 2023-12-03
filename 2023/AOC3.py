import re
from collections import defaultdict
from math import prod

lines = open("3").readlines()

part_numbers_and_positions = []
symbol_positions = set()
star_positions = set()

for i, line in enumerate(lines):
    for part in re.finditer(r"\d+", line):
        part_numbers_and_positions.append((int(part.group()), i, part.span()))
    for symbol in re.finditer(r"[^\d.\n]", line):
        symbol_positions.add((i, symbol.start()))
    for star in re.finditer(r"\*", line):
        star_positions.add((i, star.start()))


def get_adjacencies(pos: tuple[int, int]) -> list[tuple[int, int]]:
    return [
        (pos[0] - 1, pos[1] - 1),
        (pos[0], pos[1] - 1),
        (pos[0] + 1, pos[1] - 1),
        (pos[0] - 1, pos[1]),
        (pos[0] + 1, pos[1]),
        (pos[0] - 1, pos[1] + 1),
        (pos[0], pos[1] + 1),
        (pos[0] + 1, pos[1] + 1),
    ]


def get_part_number_if_legit(part_info: tuple[int, int, tuple[int, int]]) -> int:
    part_no, line_no, span = part_info
    for col_no in range(*span):
        for pos in get_adjacencies((line_no, col_no)):
            if pos in symbol_positions:
                return part_no
    return 0


def get_part_stars(line_no: int, span: tuple[int, int]) -> set[tuple[int, int]]:
    stars = set()
    for col_no in range(*span):
        for pos in get_adjacencies((line_no, col_no)):
            if pos in star_positions:
                stars.add(pos)
    return stars


stars_with_parts = defaultdict(list)
for part_no, line_no, span in part_numbers_and_positions:
    for star_pos in get_part_stars(line_no, span):
        stars_with_parts[star_pos].append(part_no)


print(f"Part 1: {sum(map(get_part_number_if_legit, part_numbers_and_positions))}")
print(
    f"Part 2: {sum(map(prod, filter(lambda part_numbers: len(part_numbers) == 2, stars_with_parts.values())))}"
)
