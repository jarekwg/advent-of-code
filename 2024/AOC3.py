import re
from itertools import starmap
from operator import mul

corrupted_memory = open("3").read()


def follow_instructions(memory: str, naive: bool) -> int:
    if not naive:
        memory = re.sub(r"don't\(\).*?(?:do\(\)|$)", "💩", memory, flags=re.DOTALL)
    return sum(
        starmap(
            mul,
            (map(int, op.split(",")) for op in re.findall(r"mul\((\d+,\d+)\)", memory)),
        )
    )


print(f"Part 1: {follow_instructions(corrupted_memory, naive=True)}")
print(f"Part 2: {follow_instructions(corrupted_memory, naive=False)}")
