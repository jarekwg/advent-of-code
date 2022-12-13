import json


def listify(v: int | list) -> list:
    return v if isinstance(v, list) else [v]


def compare_values(v1: int | list, v2: int | list) -> bool | None:
    if isinstance(v1, int) and isinstance(v2, int):
        return None if v1 == v2 else v1 < v2
    return compare_lists(listify(v1), listify(v2))


def compare_lists(l1: list, l2: list) -> bool | None:
    for L, R in zip(l1, l2):
        if (res := compare_values(L, R)) is None:
            continue
        return res
    return None if len(l1) == len(l2) else len(l1) < len(l2)


class Packet(list):
    def __lt__(self, other: "Packet") -> bool:
        return compare_lists(self, other)


packet_pairs = [
    [*map(json.loads, x.split("\n"))] for x in open("13").read().split("\n\n")
]
packets = [*map(json.loads, open("13").read().replace("\n\n", "\n").split("\n"))]
divider_packets = [[[2]], [[6]]]
sorted_packets = sorted(packets + divider_packets, key=lambda packet: Packet(packet))

print(
    f"Part 1: {sum(i + 1 for i, packet_pair in enumerate(packet_pairs) if compare_lists(*packet_pair))}"
)
print(
    f"Part 2: {(sorted_packets.index(divider_packets[0]) + 1) * (sorted_packets.index(divider_packets[1]) + 1)}"
)
