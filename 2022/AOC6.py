import re


def get_pattern(n_unique: int):
    pattern = "(.)"
    part = r"(?!\1)(.)"
    for i in range(2, n_unique + 1):
        pattern += part
        part = part[:-4] + rf"|\{i})(.)"
    return pattern


input = open("6").read()
print(f"Part 1: {re.search(get_pattern(4), input).end()}")
print(f"Part 2: {re.search(get_pattern(14), input).end()}")
