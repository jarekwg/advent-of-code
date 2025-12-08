from dataclasses import dataclass
from math import prod


@dataclass(frozen=True)
class JunctionBox:
    x: int
    y: int
    z: int

    def dist_to(self, other: 'JunctionBox') -> int:
        return (self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2

# Prep JunctionBoxes
jbs = [JunctionBox(*map(int, line.split(","))) for line in open("8").read().splitlines()]

# Calc all distances O(n^2) and sort by distance.
distances = []
jbs_to_iterate = jbs.copy()
while jbs_to_iterate:
    jb = jbs_to_iterate.pop(0)
    distances.extend([(jb.dist_to(other), jb, other) for other in jbs_to_iterate])

distances = sorted(distances, key=lambda x: x[0])

# Set up mappings (linked both ways for easier merging)
jbs_to_circuits = {jb: i for i, jb in enumerate(jbs)}
circuits_to_jbs: dict[int, set[JunctionBox]] = {}
for jb, circuit in jbs_to_circuits.items():
    circuits_to_jbs.setdefault(circuit, set()).add(jb)


class FoundPart2Solution(Exception):
    def __init__(self, value: int):
        self.value = value
        super().__init__(f"Part 2: {value}")


def merge_circuits(jb1: JunctionBox, jb2: JunctionBox):
    if jbs_to_circuits[jb1] == jbs_to_circuits[jb2]:
        return
    circuit_to_merge = jbs_to_circuits[jb2]
    for jb in circuits_to_jbs[circuit_to_merge]:
        jbs_to_circuits[jb] = jbs_to_circuits[jb1]
        circuits_to_jbs[jbs_to_circuits[jb1]].add(jb)
    del circuits_to_jbs[circuit_to_merge]
    if len(circuits_to_jbs) == 1:
        raise FoundPart2Solution(jb1.x * jb2.x)

# Merge first 1000 closest jbs for part 1.
for _, jb1, jb2 in distances[:1000]:
    merge_circuits(jb1, jb2)

print(f"Part 1: {prod(sorted(map(len, circuits_to_jbs.values()))[-3:])}")

# Merge remaining jbs until we have one circuit.
try:
    for _, jb1, jb2 in distances:
        merge_circuits(jb1, jb2)
except FoundPart2Solution as e:
    print(e)