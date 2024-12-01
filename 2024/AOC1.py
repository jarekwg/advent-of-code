from collections import Counter
from operator import sub

L, R = zip(*[map(int, l.split()) for l in open("1").readlines()])

R_counts = Counter(R)

print(f"Part 1: {sum(map(abs, map(sub, sorted(L), sorted(R))))}")
print(f"Part 2: {sum([l*R_counts[l] for l in L])}")
