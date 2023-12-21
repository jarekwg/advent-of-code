def get_horizontal_reflection(pattern: list[list[bool]], smudge: bool) -> int:
    if smudge:
        for y in range(len(pattern)):
            for x in range(len(pattern[0])):
                pattern[y][x] ^= True
                for i in range(1, len(pattern)):
                    j = min(i, len(pattern) - i)
                    if not (i - j <= y < i + j):
                        continue  # smudge must be _on_ the mirror!
                    if list(reversed(pattern[i - j : i])) == pattern[i : i + j]:
                        return i
                pattern[y][x] ^= True
    else:
        for i in range(1, len(pattern)):
            j = min(i, len(pattern) - i)
            if list(reversed(pattern[i - j : i])) == pattern[i : i + j]:
                return i
    return 0


def transpose(pattern: list[list[bool]]) -> list[list[bool]]:
    return list(map(list, zip(*pattern)))


def summarise_notes(smudge: bool) -> int:
    summary = 0
    for pattern_str in open("13").read().split("\n\n"):
        pattern = [[c == "#" for c in line] for line in pattern_str.split("\n")]
        summary += get_horizontal_reflection(
            pattern, smudge
        ) * 100 or get_horizontal_reflection(transpose(pattern), smudge)
    return summary


print(f"Part 1: {summarise_notes(smudge=False)}")
print(f"Part 2: {summarise_notes(smudge=True)}")
