import re

lines = open("12").read().splitlines()


def CeebsSolvingException(Exception):
    pass


# Blocks always consume at least 7 squares.
# So let's first just check which of the regions can actually be satisfied.
fittable_areas = 0
for line in lines[30:]:
    width, length, presents = re.match(r"(\d+)x(\d+): ([\d\s]+)", line).groups()  # type: ignore
    area_available = int(width) * int(length)
    min_area_required = sum(int(p) for p in presents.split()) * 7
    max_area_required = sum(int(p) for p in presents.split()) * 9
    if area_available < min_area_required:
        # Definitely not fittable.
        continue
    if area_available >= max_area_required:
        # Definitely fittable.
        fittable_areas += 1
        continue

    # min needed fits, but max needed doesn't. We'd have to explore packing. Nah.
    raise CeebsSolvingException("Nah")

print(f"Part 1: {fittable_areas}")
