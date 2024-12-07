data = [line.split(": ") for line in open("7")]
equations = [(int(k), [*map(int, v.split(" "))]) for k, v in data]


def satisfiable(test_value: int, numbers: list[int], nce: bool) -> bool:
    if len(numbers) == 1:
        return numbers[0] == test_value

    # We get some neat shortcircuiting by processing backwards.
    n = numbers[-1]
    return (
        satisfiable(test_value - n, numbers[:-1], nce)
        or (test_value / n % 1 == 0 and satisfiable(test_value // n, numbers[:-1], nce))
        or (
            nce
            and str(test_value).endswith(str(n))
            and satisfiable((test_value - n) // 10 ** (len(str(n))), numbers[:-1], nce)
        )
    )


def calc_total_calibration(notice_concat_elephant: bool) -> int:
    return sum(
        test_value
        for test_value, numbers in equations
        if satisfiable(test_value, numbers, notice_concat_elephant)
    )


print(f"Part 1: {calc_total_calibration(False)}")
print(f"Part 2: {calc_total_calibration(True)}")
