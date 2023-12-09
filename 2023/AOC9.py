from functools import reduce

lines = open("9").readlines()


def str_to_seq(s: str) -> list[int]:
    return [*map(int, s.split())]


def get_seq_diffs(seq: list[int]) -> list[int]:
    diffs = []

    def diff(a: int, b: int) -> int:
        diffs.append(b - a)
        return b

    reduce(diff, seq[1:], seq[0])
    return diffs


def get_next_in_sequence(seq: list[int]) -> int:
    if not any(seq):
        return 0
    return seq[-1] + get_next_in_sequence(get_seq_diffs(seq))


def get_prev_in_sequence(seq: list[int]) -> int:
    if not any(seq):
        return 0
    return seq[0] - get_prev_in_sequence(get_seq_diffs(seq))


print(f"Part 1: {sum(map(get_next_in_sequence, map(str_to_seq, lines)))}")
print(f"Part 2: {sum(map(get_prev_in_sequence, map(str_to_seq, lines)))}")
