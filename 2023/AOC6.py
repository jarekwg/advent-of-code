from math import prod, sqrt

T_str, D_str = open("6").readlines()

TD_pairs = list(zip(map(int, T_str.split()[1:]), map(int, D_str.split()[1:])))
T_combined = int(T_str.replace(" ", "").split(":")[1])
D_combined = int(D_str.replace(" ", "").split(":")[1])


def get_n_wins(TD_pair: tuple[int, int]) -> int:
    T, D = TD_pair
    h_lower = (T - sqrt(T * T - 4 * D)) // 2
    h_upper = (T + sqrt(T * T - 4 * D)) // 2
    return int(h_upper - h_lower)


print(f"Part 1: {prod(map(get_n_wins, TD_pairs))}")
print(f"Part 2: {get_n_wins((T_combined, D_combined))}")
