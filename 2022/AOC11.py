class Monkey:
    def __init__(self) -> None:
        self.items: list[int] = []
        self.operation = None
        self.test = None
        self.target_monkey_if_test_true = None
        self.target_monkey_if_test_false = None
        self.n_inspected = 0

    def __repr__(self) -> str:
        return f"<Monkey with items {self.items}. {self.n_inspected=}"


def shenanigans(boredom_relief: bool, rounds: int) -> int:
    monkeys = []
    mod = 1
    for line in open("11").readlines():
        match line.split():
            case ["Monkey", _]:
                monkeys.append(Monkey())
            case ["Starting", "items:", *item_worries]:
                monkeys[-1].items = [
                    int(item_worry.strip(",")) for item_worry in item_worries
                ]
            case ["Operation:", "new", "=", "old", "*", "old"]:
                monkeys[-1].operation = lambda x: x**2
            case ["Operation:", "new", "=", "old", "*", mult_amt]:
                monkeys[-1].operation = lambda x, mult_amt=int(mult_amt): x * mult_amt
            case ["Operation:", "new", "=", "old", "+", add_amt]:
                monkeys[-1].operation = lambda x, add_amt=int(add_amt): x + add_amt
            case ["Test:", "divisible", "by", divisor]:
                monkeys[-1].test = int(divisor)
                mod *= int(divisor)
            case ["If", "true:", "throw", "to", "monkey", monkey_id]:
                monkeys[-1].target_monkey_if_test_true = int(monkey_id)
            case ["If", "false:", "throw", "to", "monkey", monkey_id]:
                monkeys[-1].target_monkey_if_test_false = int(monkey_id)
            case []:
                pass
            case _:
                raise Exception(f"Unhandled note: {line}")

    for round in range(rounds):
        for monkey in monkeys:
            while monkey.items:
                # Monkey picks up item.
                worry_level = monkey.items.pop(0)
                monkey.n_inspected += 1
                # Monkey inspects.
                worry_level = monkey.operation(worry_level)
                # Monkey gets bored.
                if boredom_relief:
                    worry_level //= 3
                # Sane integer storage.
                worry_level %= mod
                if worry_level % monkey.test == 0:
                    monkeys[monkey.target_monkey_if_test_true].items.append(worry_level)
                else:
                    monkeys[monkey.target_monkey_if_test_false].items.append(
                        worry_level
                    )

    top_inspectors = sorted([monkey.n_inspected for monkey in monkeys])[-2:]
    # Calc monkey business
    return top_inspectors[0] * top_inspectors[1]


print(f"Part 1: {shenanigans(boredom_relief=True, rounds=20)}")
print(f"Part 2: {shenanigans(boredom_relief=False, rounds=10000)}")
