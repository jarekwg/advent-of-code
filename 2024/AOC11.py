from functools import cache

stones = [*map(int, open("11").read().split())]


@cache
def count_stones_after_n_blinks(s: int, n: int) -> int:
    if n == 0:
        return 1
    if s == 0:
        return count_stones_after_n_blinks(1, n - 1)
    elif (l := len(str(s))) % 2 == 0:
        return count_stones_after_n_blinks(
            s // 10 ** (l // 2), n - 1
        ) + count_stones_after_n_blinks(s % 10 ** (l // 2), n - 1)
    else:
        return count_stones_after_n_blinks(s * 2024, n - 1)


print(f"Part 1: {sum(count_stones_after_n_blinks(stone, 25) for stone in stones)}")
print(f"Part 2: {sum(count_stones_after_n_blinks(stone, 75) for stone in stones)}")
