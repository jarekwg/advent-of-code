stratlines = open("2").readlines()

res = [
    {
        "A X": 3 + 1,
        "B Y": 3 + 2,
        "C Z": 3 + 3,
        "A Y": 6 + 2,
        "B Z": 6 + 3,
        "C X": 6 + 1,
        "A Z": 0 + 3,
        "B X": 0 + 1,
        "C Y": 0 + 2,
    },
    {
        "A X": 0 + 3,
        "B Y": 3 + 2,
        "C Z": 6 + 1,
        "A Y": 3 + 1,
        "B Z": 6 + 3,
        "C X": 0 + 2,
        "A Z": 6 + 2,
        "B X": 0 + 1,
        "C Y": 3 + 3,
    },
]


def score(part):
    return lambda round: res[part][round.strip()]


print(f"Part 1: {sum(map(score(0), stratlines))}")
print(f"Part 2: {sum(map(score(1), stratlines))}")
