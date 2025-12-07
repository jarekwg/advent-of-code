from functools import cache

rows = [list(row) for row in open("7").read().splitlines()]

n_splits = 0

@cache
def trace_path(p: int, y: int) -> int:
    global n_splits
    if y == len(rows):
        return 1
    match rows[y][p]:
        case "^":
            n_splits += 1
            return trace_path(p-1, y+1) + trace_path(p+1, y+1)
        case _:
            return trace_path(p, y+1)


n_timelines = trace_path(rows[0].index("S"), 1)
print(f"Part 1: {n_splits}")
print(f"Part 2: {n_timelines}")