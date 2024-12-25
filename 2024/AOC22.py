from collections import defaultdict


def gen_next_secret_number(secret_number: int) -> int:
    secret_number = (secret_number ^ (secret_number << 6)) % 2**24
    secret_number = (secret_number ^ (secret_number >> 5)) % 2**24
    secret_number = (secret_number ^ (secret_number << 11)) % 2**24
    return secret_number


sum_of_final_secret_numbers = 0
winnings_by_sequence: dict[tuple[int, ...], int] = defaultdict(int)
for secret_number in map(int, open("22").read().splitlines()):
    seen_sequences = set()
    diffs = [0]
    for i in range(2000):
        next_secret_number = gen_next_secret_number(secret_number)
        diffs.append(next_secret_number % 10 - secret_number % 10)
        secret_number = next_secret_number
        if len(diffs) >= 4:
            sequence = tuple(diffs[-4:])
            if sequence not in seen_sequences:
                seen_sequences.add(sequence)
                winnings_by_sequence[sequence] += secret_number % 10

    sum_of_final_secret_numbers += secret_number


print("Part 1:", sum_of_final_secret_numbers)
print("Part 2:", max(winnings_by_sequence.values()))
