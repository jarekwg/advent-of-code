def turn_on_batteries(bank:str, n_batteries: int) -> str:
    if n_batteries == 1:
        return max(bank)
    return (m:=max(bank[:-n_batteries+1])) + turn_on_batteries(bank[bank.index(m)+1:], n_batteries-1)

def calc_joltage(n_batteries: int) -> int:
    return sum(int(turn_on_batteries(bank, n_batteries)) for bank in open("3").read().splitlines())

print(f"Part 1: {calc_joltage(2)}")
print(f"Part 2: {calc_joltage(12)}")
