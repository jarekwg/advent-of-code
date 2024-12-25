from enum import Enum
from functools import cache


class Keypad(Enum):
    NUM = 0
    DIR = 1


# NOTE: Sequence order doesn't matter here; we permute them later.
# NOTE: Could do some pathfinding trawling to construct this, but meh;
#       the fun of this challenge is in the combinatorial explosion.
SEQS = {
    Keypad.NUM: {
        "AA": "",
        "A0": "<",
        "A1": "^<<",
        "A2": "<^",
        "A3": "^",
        "A4": "^^<<",
        "A5": "<^^",
        "A6": "^^",
        "A7": "^^^<<",
        "A8": "<^^^",
        "A9": "^^^",
        "0A": ">",
        "00": "",
        "01": "^<",
        "02": "^",
        "03": ">^",
        "04": "^^<",
        "05": "^^",
        "06": "^^>",
        "07": "^^^<",
        "08": "^^^",
        "09": "^^^>",
        "1A": ">>v",
        "10": ">v",
        "11": "",
        "12": ">",
        "13": ">>",
        "14": "^",
        "15": ">^",
        "16": ">>^",
        "17": "^^",
        "18": "^^>",
        "19": ">>^^",
        "2A": "v>",
        "20": "v",
        "21": "<",
        "22": "",
        "23": ">",
        "24": "<^",
        "25": "^",
        "26": ">^",
        "27": "<^^",
        "28": "^^",
        "29": "^^>",
        "3A": "v",
        "30": "<v",
        "31": "<<",
        "32": "<",
        "33": "",
        "34": "<<^",
        "35": "<^",
        "36": "^",
        "37": "^^<<",
        "38": "<^^",
        "39": "^^",
        "4A": ">>vv",
        "40": ">vv",
        "41": "v",
        "42": "v>",
        "43": "v>>",
        "44": "",
        "45": ">",
        "46": ">>",
        "47": "^",
        "48": ">^",
        "49": ">>^",
        "5A": "vv>",
        "50": "vv",
        "51": "<v",
        "52": "v",
        "53": "v>",
        "54": "<",
        "55": "",
        "56": ">",
        "57": "<^",
        "58": "^",
        "59": ">^",
        "6A": "vv",
        "60": "<vv",
        "61": "<<v",
        "62": "<v",
        "63": "v",
        "64": "<<",
        "65": "<",
        "66": "",
        "67": "<<^",
        "68": "<^",
        "69": "^",
        "7A": ">>vvv",
        "70": ">vvv",
        "71": "vv",
        "72": "vv>",
        "73": "vv>>",
        "74": "v",
        "75": "v>",
        "76": "v>>",
        "77": "",
        "78": ">",
        "79": ">>",
        "8A": "vvv>",
        "80": "vvv",
        "81": "<vv",
        "82": "vv",
        "83": "vv>",
        "84": "<v",
        "85": "v",
        "86": "v>",
        "87": "<",
        "88": "",
        "89": ">",
        "9A": "vvv",
        "90": "<vvv",
        "91": "<<vv",
        "92": "<vv",
        "93": "vv",
        "94": "<<v",
        "95": "<v",
        "96": "v",
        "97": "<<",
        "98": "<",
        "99": "",
    },
    Keypad.DIR: {
        "AA": "",
        "A<": "v<<",
        "Av": "v<",
        "A>": "v",
        "A^": "<",
        "<A": ">>^",
        "<<": "",
        "<v": ">",
        "<>": ">>",
        "<^": ">^",
        "vA": ">^",
        "v<": "<",
        "vv": "",
        "v>": ">",
        "v^": "^",
        ">A": "^",
        "><": "<<",
        ">v": "<",
        ">>": "",
        ">^": "<^",
        "^A": ">",
        "^<": "v<",
        "^v": "v",
        "^>": "v>",
        "^^": "",
    },
}
ILLEGAL_SEQS = {
    Keypad.NUM: {
        "A1": "<<^",
        "A4": "<<^^",
        "A7": "<<^^^",
        "01": "<^",
        "04": "<^^",
        "07": "<^^^",
        "1A": "v>>",
        "10": "v>",
        "4A": "vv>>",
        "40": "vv>",
        "7A": "vvv>>",
        "70": "vvv>",
    },
    Keypad.DIR: {
        "A<": "<<v",
        "^<": "<v",
        "<^": "^>",
        "<A": "^>>",
    },
}


def reverse_str(s: str) -> str:
    return "".join(reversed(s))


def sorted_str(s: str) -> str:
    return "".join(sorted(s))


@cache
def get_min_keyseq_length(
    keyseq: str,
    depth: int,
    keypad: Keypad,
) -> int:
    if depth == 0:
        return len(keyseq)

    keyseq = "A" + keyseq

    length = 0
    for i in range(len(keyseq) - 1):
        from_to = keyseq[i : i + 2]

        # Generate ways to get from a to b (skipping illegal movements)
        seq_sorted = sorted_str(SEQS[keypad][from_to])
        seqs = {seq_sorted, reverse_str(seq_sorted)} - {
            ILLEGAL_SEQS[keypad].get(from_to, "WHERE IS THE HISTORIAN?!")
        }
        lengths = [
            get_min_keyseq_length(seq + "A", depth=depth - 1, keypad=Keypad.DIR)
            for seq in seqs
        ]
        length += min(lengths)

    return length


def solve_for_depth(depth: int) -> int:
    total = 0
    for keyseq in open("21").read().splitlines():
        num = int(keyseq[:-1])
        total += get_min_keyseq_length(keyseq, depth=depth + 1, keypad=Keypad.NUM) * num
    return total


print("Part 1:", solve_for_depth(2))
print("Part 2:", solve_for_depth(25))
