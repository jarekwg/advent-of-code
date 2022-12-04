elfloads = [sum(map(int, _.split("\n"))) for _ in open("1").read().strip().split("\n\n")]

print(f"Part 1: {max(elfloads)}")
print(f"Part 2: {sum(sorted(elfloads)[-3:])}")
