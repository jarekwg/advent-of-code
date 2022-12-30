import operator

from z3 import Real, Solver  # noqa

ops = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}


def monkeymath(iamhumn: bool) -> int:
    solver = Solver()
    for line in open("21").readlines():
        name, func = line.strip().split(": ")
        if iamhumn and name == "humn":
            continue
        match func.split():
            case [n]:
                solver.add(Real(name) == int(n))
            case [n1, op, n2]:
                if iamhumn and name == "root":
                    solver.add(Real(n1) == Real(n2))
                else:
                    solver.add(Real(name) == ops[op](Real(n1), Real(n2)))
    solver.check()
    return solver.model()[Real("humn" if iamhumn else "root")]


print(f"Part 1: {monkeymath(iamhumn=False)}")
print(f"Part 2: {monkeymath(iamhumn=True)}")
