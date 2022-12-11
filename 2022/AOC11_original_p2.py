class Item:
    def __init__(self, val) -> None:
        self.mods = {
            2: 0,
            3: 0,
            5: 0,
            7: 0,
            11: 0,
            13: 0,
            17: 0,
            19: 0,
        }
        self.add(val)

    def multiply(self, val):
        for n, mod in self.mods.items():
            self.mods[n] = (mod * val) % n

    def add(self, val):
        for n, mod in self.mods.items():
            self.mods[n] = (mod + val) % n

    def square(self):
        for n, mod in self.mods.items():
            self.mods[n] = mod**2 % n


class Monkey:
    def __init__(self) -> None:
        self.items: list[Item] = []
        self.operation = None
        self.test = None
        self.target_monkey_if_test_true = None
        self.target_monkey_if_test_false = None
        self.n_inspected = 0

    def __repr__(self) -> str:
        return f"<Monkey with items {self.items}. {self.n_inspected=}"


def worry_adder(add_amt: int):
    return lambda x: x.add(add_amt)


def worry_multiplier(mult_amt: int):
    return lambda x: x.multiply(mult_amt)


monkeys = []
for line in open("11").readlines():
    match line.split():
        case ["Monkey", _]:
            monkeys.append(Monkey())
        case ["Starting", "items:", *item_worries]:
            monkeys[-1].items = [
                Item(int(item_worry.strip(","))) for item_worry in item_worries
            ]
        case ["Operation:", "new", "=", "old", "*", "old"]:
            monkeys[-1].operation = lambda x: x.square()
        case ["Operation:", "new", "=", "old", "*", mult_amt]:
            monkeys[-1].operation = worry_multiplier(int(mult_amt))
        case ["Operation:", "new", "=", "old", "+", add_amt]:
            monkeys[-1].operation = worry_adder(int(add_amt))
        case ["Test:", "divisible", "by", divisor]:
            monkeys[-1].test = int(divisor)
        case ["If", "true:", "throw", "to", "monkey", monkey_id]:
            monkeys[-1].target_monkey_if_test_true = int(monkey_id)
        case ["If", "false:", "throw", "to", "monkey", monkey_id]:
            monkeys[-1].target_monkey_if_test_false = int(monkey_id)
        case []:
            pass
        case _:
            raise Exception(f"Unhandled note: {line}")

for round in range(10000):
    print(round)
    for monkey in monkeys:
        while monkey.items:
            # Monkey picks up item.
            item = monkey.items.pop(0)
            monkey.n_inspected += 1
            # Monkey inspects.
            monkey.operation(item)
            # Monkey gets bored
            # worry_level //= 3
            if item.mods[monkey.test] == 0:
                monkeys[monkey.target_monkey_if_test_true].items.append(item)
            else:
                monkeys[monkey.target_monkey_if_test_false].items.append(item)

top_inspectors = sorted([monkey.n_inspected for monkey in monkeys])[-2:]
# print(f"Part 1: {top_inspectors[0] * top_inspectors[1]}")
print(f"Part 2: {top_inspectors[0] * top_inspectors[1]}")
