wordsearch = [l.strip() for l in open("4").readlines()]

L, W = len(wordsearch[0]), len(wordsearch)

SEQ = "XMAS"
DIRS1 = [(0, -1), (0, 1), (1, 0), (-1, 0), (-1, -1), (1, 1), (1, -1), (-1, 1)]
DIRS2 = [(1, 1, 1, -1), (1, -1, -1, -1), (-1, -1, -1, 1), (-1, 1, 1, 1)]

tot1 = tot2 = 0

for y, row in enumerate(wordsearch):
    for x, c in enumerate(row):
        if c == SEQ[0]:
            for dx, dy in DIRS1:
                tx, ty, pos = x, y, 0
                while 0 <= tx < W and 0 <= ty < L and wordsearch[ty][tx] == SEQ[pos]:
                    pos += 1
                    tx += dx
                    ty += dy
                    if pos == len(SEQ):
                        tot1 += 1
                        break
        if c == "A" and 0 < x < W - 1 and 0 < y < L - 1:
            for dx, dy, ex, ey in DIRS2:
                if all(
                    [
                        wordsearch[y + dy][x + dx] == "M",
                        wordsearch[y - dy][x - dx] == "S",
                        wordsearch[y + ey][x + ex] == "M",
                        wordsearch[y - ey][x - ex] == "S",
                    ]
                ):
                    tot2 += 1


print(f"Part 1: {tot1}")
print(f"Part 2: {tot2}")
