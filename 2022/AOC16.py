import re
from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations, permutations


@dataclass
class Valve:
    name: str
    flow_rate: int
    connecting_valves: list[str]

    def __hash__(self) -> str:
        return hash(self.name)


valves: dict[str, Valve] = {}

for line in open("16").readlines():
    valve_name, flow_rate, connecting_valves = re.match(
        r"Valve (\S\S) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z, ]*)", line
    ).groups()
    valves[valve_name] = Valve(
        valve_name, int(flow_rate), connecting_valves.split(", ")
    )


@dataclass
class Branch:
    my_valve: Valve
    ele_valve: Valve
    my_time_left: int
    ele_time_left: int
    score: int
    valves_left: set[Valve]

    @property
    def naive_best_case_score(self):
        score = self.score
        my_time_left = self.my_time_left
        ele_time_left = self.ele_time_left
        sorted_valve_flows = sorted([v.flow_rate for v in self.valves_left])
        while (my_time_left >= 2 or ele_time_left >= 2) and sorted_valve_flows:
            if my_time_left > ele_time_left:
                my_time_left -= 2
                score += my_time_left * sorted_valve_flows.pop()
            else:
                ele_time_left -= 2
                score += ele_time_left * sorted_valve_flows.pop()
        return score


@lru_cache
def time_to_reach_and_open_valve(valve1: Valve, valve2: Valve) -> int:
    painted: dict[str, int] = {}
    n = 0
    to_paint = [valve1]
    while valve2.name not in painted:
        next_to_paint = []
        for valve in to_paint:
            painted[valve.name] = n
            next_to_paint.extend(
                [
                    valves[cv_name]
                    for cv_name in valve.connecting_valves
                    if cv_name not in painted
                ]
            )
        to_paint = next_to_paint
        n += 1
    return painted[valve2.name] + 1  # Adding one, to account for time taken to open.


valves_with_nonzero_flow_rate = [
    valve for valve in valves.values() if valve.flow_rate != 0
]
top_score = 0


def relieve_pressure(train_elephant: bool) -> int:
    to_explore = [
        Branch(
            my_valve=valves["AA"],
            ele_valve=valves["AA"],
            my_time_left=26 if train_elephant else 30,
            ele_time_left=26 if train_elephant else 0,
            score=0,
            valves_left=set(valves_with_nonzero_flow_rate),
        )
    ]
    while to_explore:
        branch = to_explore.pop()
        if branch.naive_best_case_score < top_score:
            continue

        def add_branch(my_valve: Valve, ele_valve: Valve):
            my_time_left = (
                (
                    branch.my_time_left
                    - time_to_reach_and_open_valve(branch.my_valve, my_valve)
                )
                if my_valve != branch.my_valve
                else 0
            )
            ele_time_left = (
                (
                    branch.ele_time_left
                    - time_to_reach_and_open_valve(branch.ele_valve, ele_valve)
                )
                if ele_valve != branch.ele_valve
                else 0
            )
            next_branch = Branch(
                my_valve,
                ele_valve,
                my_time_left,
                ele_time_left,
                branch.score
                + my_time_left * my_valve.flow_rate
                + ele_time_left * ele_valve.flow_rate,
                valves_left=branch.valves_left - {my_valve, ele_valve},
            )
            to_explore.append(next_branch)
            global top_score
            if (new_score := next_branch.score) > top_score:
                top_score = new_score
                # print(f"-----------New top score {top_score}")

        if branch.my_valve == branch.ele_valve and train_elephant:
            for my_valve, ele_valve in combinations(branch.valves_left, 2):
                # We both move (doesn't matter who goes to which in the pair).
                add_branch(my_valve, ele_valve)
        else:
            if branch.my_time_left >= 2 and branch.ele_time_left >= 2:
                for my_valve, ele_valve in permutations(branch.valves_left, 2):
                    # We both move.
                    add_branch(my_valve, ele_valve)
            if branch.my_time_left >= 2:
                for valve in branch.valves_left:
                    # Elephant stays put.
                    add_branch(my_valve=valve, ele_valve=branch.ele_valve)
            if branch.ele_time_left >= 2:
                for valve in branch.valves_left:
                    # I stay put.
                    add_branch(my_valve=branch.my_valve, ele_valve=valve)

    return top_score


print(f"Part 1: {relieve_pressure(train_elephant=False)}")
print(f"Part 2: {relieve_pressure(train_elephant=True)}")
