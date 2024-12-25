from typing import Callable, Literal, cast

INPUT_DATA, GATE_DATA = open("24").read().split("\n\n")

INPUT_WIRES: dict[str, Literal[0, 1]] = {}
GATE_WIRES: dict[str, Callable[[], Literal[0, 1]]] = {}

DEBUG: dict[str, tuple[str, str, str]] = {}

GATE_ALIASES: dict[str, str] = {}  # Conveniece naming to aid debugging
SWAPS: dict[str, str] = {}  # Swaps to apply to "fix" the calculator

for line in INPUT_DATA.splitlines():
    name, value = line.split(": ")
    INPUT_WIRES[name] = cast(Literal[0, 1], int(value))


def get_wire_value(name: str) -> Literal[0, 1]:
    return INPUT_WIRES[name] if name in INPUT_WIRES else GATE_WIRES[name]()


def getval(a_name, b_name, operator) -> Callable[[], Literal[0, 1]]:
    def inner():
        a = get_wire_value(a_name)
        b = get_wire_value(b_name)
        if operator == "AND":
            return a & b
        if operator == "OR":
            return a | b
        if operator == "XOR":
            return a ^ b

    return inner


# We're going to try and "fix" the calculator by applying some aliases to the gates
# until we identify where the connections are wrong.
gates_to_review = []
for line in GATE_DATA.splitlines():
    a, op, b, _, name = line.split(" ")
    gates_to_review.append((a, op, b, name))

"""
Notation:

# x & y ops
zna = xn AND yn
znx = xn XOR yn

# base cases
z00 = z00x
z00r = z00a

# recursive cases
zne = znx AND z(n-1)r
znr = zna OR zne
zn = znx XOR z(n-1)r
"""

while gates_to_review:
    orig_a, op, orig_b, name = gates_to_review.pop(0)
    # print("BEFORE", orig_a, op, orig_b, name)
    a, b = orig_a, orig_b
    a, b = SWAPS.get(a, a), SWAPS.get(b, b)  # Apply any known swaps
    a, b = GATE_ALIASES.get(a, a), GATE_ALIASES.get(b, b)  # Apply identified aliases
    a, b = sorted((a, b))  # Sort to make it easier to match patterns
    # print("AFTER", a, op, b, name)

    # If operating on x & y pair, easy mapping.
    if (a[0], op, b[0]) == ("x", "AND", "y") and a[1:] == b[1:]:
        GATE_ALIASES[name] = f"z{a[1:]}a"
    elif (a[0], op, b[0]) == ("x", "XOR", "y") and a[1:] == b[1:]:
        GATE_ALIASES[name] = f"z{a[1:]}x"

    # Z mappings (will gradually reveal themselves as we iterate)
    elif (a, op, b) == ("z00a", "AND", "z01x"):  # base case (z00r == z00a)
        GATE_ALIASES[name] = "z01e"
    elif (a, op, b) == (
        "z00a",
        "XOR",
        "z01x",
    ) and name == "z01":  # base case (z00r == z00a)
        pass
    elif ((a[0], a[-1]), op, (b[0], b[-1])) == (
        ("z", "r"),
        "AND",
        ("z", "x"),
    ) and int(a[1:-1]) + 1 == int(b[1:-1]):
        GATE_ALIASES[name] = f"z{b[1:-1]}e"
    elif ((a[0], a[-1]), op, (b[0], b[-1])) == (
        ("z", "a"),
        "OR",
        ("z", "e"),
    ) and a[1:-1] == b[1:-1]:
        GATE_ALIASES[name] = f"z{a[1:-1]}r"
    elif ((a[0], a[-1]), op, (b[0], b[-1])) == (
        ("z", "r"),
        "XOR",
        ("z", "x"),
    ) and int(a[1:-1]) + 1 == int(b[1:-1]):
        expected_name = f"z{b[1:-1]}"
        if name == expected_name:
            continue
        elif expected_name in GATE_ALIASES:
            # print("------SWAP", name, expected_name)
            GATE_ALIASES[name] = expected_name
            SWAPS[name] = expected_name
            SWAPS[expected_name] = name
        else:
            # Try again later
            gates_to_review.append((orig_a, op, orig_b, name))
    elif a[0] == b[0] == "z" and len(a) == len(b):
        # We've got a combo of wires coming into our gate that we weren't expecting..
        # Let's try and figure out which needs swapping based on the operation.
        if op in (
            "AND",
            "XOR",
        ):  # These can be handled together, as they have the same RHS
            # Here we expect one of:
            # - zne = znx AND z(n-1)r
            # - zn = znx XOR z(n-1)r
            if a[-1] == "r" or b[-1] == "r":
                if a[-1] != "r":
                    a, b = b, a
                # a is the good one, so b needs to be swapped.
                expected_b = f"z{int(a[1:-1])+1:0<2}x"
                # Dealias the expected_name
                reverse_aliases = {v: k for k, v in GATE_ALIASES.items()}
                r_b, r_expected_b = (
                    reverse_aliases.get(b, b),
                    reverse_aliases.get(expected_b, expected_b),
                )
                # print("------SWAP", r_b, r_expected_b)
                GATE_ALIASES[name] = f"z{int(a[1:-1])+1:0<2}" + (
                    "e" if op == "AND" else ""
                )
                SWAPS[r_b] = r_expected_b
                SWAPS[r_expected_b] = r_b
            else:
                # TODO: Fill this in if the sample data requires it
                print("Unrecognised gate (TODO)", a, op, b, name)
                breakpoint()
        else:
            # TODO: Fill this in if the sample data requires it
            print("Unrecognised gate (TODO)", a, op, b, name)
            breakpoint()
    else:
        # Couldn't find a good name, try again later
        gates_to_review.append((orig_a, op, orig_b, name))


# Now link them up, using more sensible names
for line in GATE_DATA.splitlines():
    a, op, b, _, name = line.split(" ")
    # ==============================
    # Uncomment this section to apply our swaps and "fix" the calculator
    # Also applies aliases to wires to make them make more sense
    # ==============================
    # a, b = SWAPS.get(a, a), SWAPS.get(b, b)
    # a, b, name = (
    #     GATE_ALIASES.get(a, a),
    #     GATE_ALIASES.get(b, b),
    #     GATE_ALIASES.get(name, name),
    # )
    # ==============================
    GATE_WIRES[name] = getval(a, b, op)
    DEBUG[name] = a, op, b
    # Also re-add base cases (that we remapped earlier).
    if name == "z00x":
        GATE_WIRES["z00"] = getval(a, b, op)
        DEBUG["z00"] = a, op, b
    if name == "z44r":
        GATE_WIRES["z45"] = getval(a, b, op)
        DEBUG["z45"] = a, op, b


def getZ(i: int) -> Literal[0, 1]:
    return get_wire_value(f"z{i:0>2}")


def calc_output() -> int:
    return sum(getZ(i) << i for i in range(46))


print("Part 1:", calc_output())
print("Part 2:", ",".join(sorted(SWAPS.keys())))
