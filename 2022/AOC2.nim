import math, sequtils, strutils, tables

let stratlines = readFile("2").splitlines

const res = [
    {
        "A X": 3 + 1,
        "B Y": 3 + 2,
        "C Z": 3 + 3,
        "A Y": 6 + 2,
        "B Z": 6 + 3,
        "C X": 6 + 1,
        "A Z": 0 + 3,
        "B X": 0 + 1,
        "C Y": 0 + 2,
    }.toTable,
    {
        "A X": 0 + 3,
        "B Y": 3 + 2,
        "C Z": 6 + 1,
        "A Y": 3 + 1,
        "B Z": 6 + 3,
        "C X": 0 + 2,
        "A Z": 6 + 2,
        "B X": 0 + 1,
        "C Y": 3 + 3,
    }.toTable,
]

echo "Part 1: ", stratlines.mapIt(res[0][it.strip]).sum
echo "Part 2: ", stratlines.mapIt(res[1][it.strip]).sum
