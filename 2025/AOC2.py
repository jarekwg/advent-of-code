import re

id_ranges = open("2").read().split(",")

invalid_doubles_sum = 0
invalid_repeats_sum = 0
for id_range in id_ranges:
    start, end = map(int, id_range.split("-"))

    for id in range(start, end + 1):
        if re.match(r"^(\d+)\1$", str(id)):
            invalid_doubles_sum += id
        if re.match(r"^(\d+)\1+$", str(id)):
            invalid_repeats_sum += id

print(f"Part 1: {invalid_doubles_sum}")
print(f"Part 2: {invalid_repeats_sum}")
