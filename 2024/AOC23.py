from itertools import combinations

connections: dict[str, set[str]] = {}
for node_to, node_from in [line.split("-") for line in open("23").read().splitlines()]:
    connections.setdefault(node_to, set()).add(node_from)
    connections.setdefault(node_from, set()).add(node_to)
    connections.setdefault(node_to, set()).add(node_to)  # Add self to connections


tot = 0
for a, b, c in combinations(connections.keys(), 3):
    if any([a.startswith("t"), b.startswith("t"), c.startswith("t")]):
        if b in connections[a] and c in connections[b] and a in connections[c]:
            tot += 1

print("Part 1:", tot)


def check_set(party: set[str]) -> bool:
    for node in party:
        if not connections[node] >= party:
            return False
    return True


def get_largest_subset(party: set[str]) -> set[str]:
    if check_set(party):
        return party
    largest_subset = set()
    for node in party:
        subset = party & connections[node]
        if len(subset) < len(party):
            subset = get_largest_subset(subset)
            if len(subset) > len(largest_subset):
                largest_subset = subset
    return largest_subset


largest_party = set()
for node, node_tos in connections.items():
    cur_set = {node, *node_tos}
    if len(cur_set) < len(largest_party):
        continue
    cur_set = get_largest_subset(cur_set)
    if len(cur_set) > len(largest_party):
        largest_party = cur_set


print("Part 2:", ",".join(sorted(largest_party)))
