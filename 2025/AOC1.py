DIR_MAP = {
    "R": 1,
    "L": -1,
}

pos = 50
n_0_visits = 0
n_0_crossings = 0

for turn in open("1").read().splitlines():
    dir, clicks = turn[0], int(turn[1:])

    prev = pos
    pos += clicks * DIR_MAP[dir]

    # Count how many times we've moved to a different multiple of 100.
    n_0_crossings += abs(pos // 100 - prev // 100)

    # Add a correction if we're going in L direction and starting or finishing on 0.
    if prev > pos:
        if pos % 100 == 0:
            n_0_crossings += 1
        if prev % 100 == 0:
            n_0_crossings -= 1

    # TBH we don't really need to be modding the number, but keeps things from getting too big..
    pos %= 100

    # Count direct landings on 0.
    if pos == 0:
        n_0_visits += 1


print(f"Part 1: {n_0_visits}")
print(f"Part 2: {n_0_crossings}")
