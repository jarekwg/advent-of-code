import re
from copy import deepcopy

input = open("5").read()


class defaultlist(list):
    def __init__(self, f):
        self._f = f

    def _prefill(self, index):
        while len(self) <= index:
            self.append(self._f())

    def __setitem__(self, index, value):
        self._prefill(index)
        super().__setitem__(index, value)

    def __getitem__(self, index):
        self._prefill(index)
        return super().__getitem__(index)


def parse_crates(crate_input: str) -> list[list[str]]:
    crates = defaultlist(list)
    for crate_line in reversed(crate_input.splitlines()):
        for i, _ in enumerate(re.findall("....", f" {crate_line}")):
            if _[2] != " ":
                crates[i].append(_[2])
    return crates


def process_instructions(
    instructions: list[str], crates: list[list[str]], crane_serial: str
) -> list[list[str]]:
    crates = deepcopy(crates)
    for instruction in instructions:
        match instruction.split(), crane_serial:
            case ["move", n, "from", source, "to", dest], "CrateMover 9000":
                for _ in range(int(n)):
                    crates[int(dest) - 1].append(crates[int(source) - 1].pop())
            case ["move", n, "from", source, "to", dest], "CrateMover 9001":
                crates[int(dest) - 1].extend(crates[int(source) - 1][-int(n):])
                del crates[int(source) - 1][-int(n):]
    return crates


crates = parse_crates(input[:input.index("\n 1")])
instructions = input[input.index("move"):].splitlines()

print(
    f"""Part 1: {"".join(map(lambda x: x[-1], process_instructions(instructions, crates, "CrateMover 9000")))}"""
)
print(
    f"""Part 2: {"".join(map(lambda x: x[-1], process_instructions(instructions, crates, "CrateMover 9001")))}"""
)
