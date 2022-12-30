from dataclasses import dataclass
from math import nan


@dataclass
class Number:
    value: int
    prev: "Number | None"
    next: "Number | None"

    def remove(self) -> None:
        # a <-> self <-> b
        # a <-> b
        self.prev.next = self.next
        self.next.prev = self.prev

    def insert_after(self, target: "Number") -> None:
        # target <-> c
        # target <-> self <-> c
        self.prev = target
        self.next = target.next

        target.next.prev = self
        target.next = self

    def to_list(self) -> None:
        res = [self.value]
        cur = self.next
        while cur != self:
            res.append(cur.value)
            cur = cur.next
        return res

    def __repr__(self) -> str:
        return str(self.value)


def decrypt(mulitiplier: int, rounds: int) -> int:
    zero = None
    mixing_order = []
    cur = temp = Number(nan, None, None)
    for n in open("20").read().split("\n"):
        num = Number(int(n) * mulitiplier, cur, None)
        if num.value == 0:
            zero = num
        mixing_order.append(num)
        cur.next = num
        cur = num

    cur.next = temp.next
    temp.next.prev = cur
    del temp

    l = len(mixing_order)
    for _ in range(rounds):
        for n in mixing_order:
            v = n.value
            cur = n
            if v > 0:
                n.remove()
                for _ in range(v % (l - 1)):
                    cur = cur.next
                n.insert_after(cur)
            elif v < 0:
                n.remove()
                for _ in range(-v % (l - 1)):
                    cur = cur.prev
                n.insert_after(cur.prev)

    decrypted = zero.to_list()
    return sum([decrypted[1000 % l], decrypted[2000 % l], decrypted[3000 % l]])


print(f"Part 1: {decrypt(1, 1)}")
print(f"Part 1: {decrypt(811589153, 10)}")
