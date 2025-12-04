def calc_joltage(n_batteries: int) -> int:
    total_joltage = 0
    for bank in open("3").read().splitlines():
        # Construct a "battery tracker" to record which batteries we're turning on.
        batteries = list(range(n_batteries))
        # Traverse the bank.
        for i in range(len(bank)):
            # Review each spot in battery tracker that may be eligible to turn this battery on.
            for j in range(min(n_batteries, i + 1)):
                if (
                    bank[i] > bank[batteries[j]]
                    and len(bank) - i >= n_batteries - j
                    and batteries[j] < i
                ):
                    # If we like it, we note this and all successive battery spots in our tracker.
                    batteries[j:]=range(i,i+n_batteries-j)

        # Calc resulting joltage.
        joltage = 0
        for i in range(n_batteries):
            joltage *= 10
            joltage += int(bank[batteries[i]])
        total_joltage += joltage
    return total_joltage


print(f"Part 1: {calc_joltage(2)}")
print(f"Part 2: {calc_joltage(12)}")
