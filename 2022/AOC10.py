class CRT:
    def __init__(self):
        self.X = [1]

    def cycle(self, v: int) -> None:
        print(
            "#" if abs((len(self.X) - 1) % 40 - self.X[-1]) < 2 else ".",
            end="" if len(self.X) % 40 else "\n",
        )
        self.X.append(self.X[-1] + v)


crt = CRT()
for line in open("10").readlines():
    match line.split():
        case ["noop"]:
            crt.cycle(0)
        case ["addx", v]:
            crt.cycle(0)
            crt.cycle(int(v))

print(f"Part 1: {sum(crt.X[i - 1] * i for i in range(20, 221, 40))}")
print("Part 2: (see above)")
