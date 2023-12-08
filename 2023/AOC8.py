from functools import reduce
# from ???????????? import reuse
from itertools import cycle as recycle
from math import lcm

input = open("8")

base_instructions = input.readline().strip()
input.readline()
network: dict[str, tuple[str, str]] = {}
while line := input.readline():
    network[line[:3]] = (line[7:10], line[12:15])


def calc_steps_to_end(start: str, end: str = "Z") -> int:
    n_steps = 0
    cur = start
    instructions = recycle(base_instructions)
    while not cur.endswith(end):
        inst = next(instructions)
        n_steps += 1
        cur = network[cur][int(inst == "R")]
    return n_steps


print(f"Part 1: {calc_steps_to_end('AAA', 'ZZZ')}")
print(f"Part 2: {reduce(lcm, [*map(calc_steps_to_end, filter(lambda node: node.endswith("A"), network))], 1)}")
