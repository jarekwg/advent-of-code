from typing import cast

d = open("5")

# Read in range info.
to_insert: set[tuple[int,int]] = set()
while (new:= d.readline().strip()) != '':
    to_insert.add(cast(tuple[int, int],tuple(map(int, new.split('-')))))

# Compress ranges into an ordered list of non-overlapping ranges.
ranges: list[tuple[int,int]] = []
while to_insert:
    ns, nf = to_insert.pop()
    for i, (s, f) in enumerate(ranges):
        if nf < s:
            ranges.insert(i, (ns, nf))
            break
        if ns <= f:
            # Overlap detected. Merge and throw back for reprocessing.
            to_insert.add((min(ns, s), max(nf, f)))
            ranges.pop(i)
            break
    else:
        ranges.append((ns, nf))


# Read in remaining data, checking whether it's in any of our ranges.
fresh_available_ingredients = 0
for new in d.read().splitlines():
    na = int(new)
    for s, f in ranges:
        if s <= na <= f:
            fresh_available_ingredients += 1
            break

print(f"Part 1: {fresh_available_ingredients}")
print(f"Part 2: {sum(r[1] - r[0] + 1 for r in ranges)}")