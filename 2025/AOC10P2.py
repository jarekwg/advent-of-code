import re

import sympy as sp


def solve_free_symbols(
    solutions: list[sp.Expr], free_symbols: list[sp.Symbol], max_joltage: int
) -> int:
    if any(
        len(solution.free_symbols) == 0 and (solution < 0 or solution % 1 != 0)
        for solution in solutions
    ):
        return -1
    if len(free_symbols) == 0:
        return sum(solutions)

    options = []
    for i in range(max_joltage + 1):
        if (
            res := solve_free_symbols(
                [solution.subs(free_symbols[0], i) for solution in solutions],
                free_symbols[1:],
                max_joltage,
            )
        ) != -1:
            options.append(res)
    return min(options) if options else -1


def solve_min_button_presses(line: str) -> int:
    indicator_lights_str, buttons_str, joltages_str = re.match(
        r"\[(?P<indicator_lights>[\.#]+)\] (?P<buttons>[^\{]+) \{(?P<joltages>[\d,]+)\}",
        line,
    ).groups()  # type: ignore
    # Convert everything to bit integers.
    buttons = [tuple(map(int, s.strip("()").split(","))) for s in buttons_str.split()]
    target_joltages = list(map(int, joltages_str.split(",")))

    # Define unknowns (as many as there are buttons)
    xs = sp.symbols(f"x0:{len(buttons)}", integer=True, nonnegative=True)
    # Define equations
    equations = []
    for ji, joltage in enumerate(target_joltages):
        equations.append(
            sp.Eq(
                sum([int(ji in button) * xs[bi] for bi, button in enumerate(buttons)]),
                joltage,
            )
        )
    solutions = sp.solve(equations, xs)
    # Identify all combinations of free symbols that satisfy our equations, then pick the one w the smallest overall sum for the system.
    free_symbols = {solution for _ in solutions.values() for solution in _.free_symbols}
    res = solve_free_symbols(
        list(solutions.values()) + list(free_symbols),
        list(free_symbols),
        max(target_joltages),
    )
    print("----------------------------------")
    print(buttons, target_joltages)
    print(free_symbols, solutions)
    print(res)
    return res


print(
    f"Part 2: {sum(solve_min_button_presses(line) for line in open('10').read().splitlines())}"
)
