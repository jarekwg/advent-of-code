f = open("3")
res1, res2 = [], []


def foo():
    r = next(f).strip()
    res1.extend(set(r[: len(r) // 2]) & set(r[len(r) // 2 :]))
    return set(r)


def bar(c):
    return o if (o := ord(c) - 96) > 0 else o + 58


while True:
    try:
        res2.extend(foo() & foo() & foo())
    except StopIteration:
        break

print(f"Part 1: {sum(map(bar, res1))}")
print(f"Part 2: {sum(map(bar, res2))}")
