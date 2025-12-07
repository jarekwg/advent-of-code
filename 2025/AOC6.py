from math import prod

tokens = [line.split() for line in open("6").read().splitlines()]

grand_total = 0
for i, op in enumerate(tokens[-1]):
    match op:
        case "+":
            grand_total += sum(int(line[i]) for line in tokens[:-1])
        case "*":
            grand_total += prod(int(line[i]) for line in tokens[:-1])

print(f"Part 1: {grand_total}")

# --------------------

def get_digit(line: str, i: int) -> str:
    try:
        return str(int(line[i]))
    except (IndexError, ValueError):
        return ''

def get_num(i: int) -> int:
    return int("".join(get_digit(line, i) for line in lines[:-1]))

lines = open("6").read().splitlines()
pos = max(len(line) for line in lines) - 1
numbers = []
grand_total = 0
while pos >= 0:
    numbers.append(get_num(pos))
    match (lines[-1][pos] if pos < len(lines[-1]) else "") :
        case "+":
            grand_total += sum(numbers)
            numbers = []
            pos-=2
        case "*":
            grand_total += prod(numbers)
            numbers = []
            pos-=2
        case _:
            pos-=1

print(f"Part 2: {grand_total}")