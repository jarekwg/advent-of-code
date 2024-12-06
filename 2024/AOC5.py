ordering_data, update_data = open("5").read().split("\n\n")
ordering_rules: dict[int, set[int]] = {}
for k, v in (map(int, r.split("|")) for r in ordering_data.split("\n")):
    ordering_rules.setdefault(k, set()).add(v)
updates = [list(map(int, u.split(","))) for u in update_data.split("\n")]


def is_update_valid(update: list[int]) -> bool:
    """
    Test if a given update is valid, but also always fix the update in memory at the same time. >;)
    """
    cur_page = 0
    is_valid = True
    while cur_page < len(update):
        # If any of the earlier pages intersects with the current page's rules "must come after" rules, FAIL!
        if set(update[:cur_page]) & ordering_rules.get(update[cur_page], set()):
            is_valid = False
            # To fix, swap the current page with the previous and test again.
            update[cur_page - 1], update[cur_page] = (
                update[cur_page],
                update[cur_page - 1],
            )
            cur_page = 0
        cur_page += 1
    return is_valid


totals = [0, 0]
for update in updates:
    totals[not is_update_valid(update)] += update[len(update) // 2]

print(f"Part 1: {totals[0]}")
print(f"Part 2: {totals[1]}")
