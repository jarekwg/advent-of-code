import math, sequtils, strutils

proc fullOverlap(p: seq[seq[int]]): bool =
    let a = p[0]
    let b = p[1]
    return (a[0] >= b[0]) and (a[1] <= b[1]) or (b[0] >= a[0]) and (b[1] <= a[1])

proc partialOverlap(p: seq[seq[int]]): bool =
    let a = p[0]
    let b = p[1]
    return (a[0] <= b[1]) and (a[1] >= b[0])

let sectionPairs = readFile("4").splitLines.mapIt(it.split(",").mapIt(it.split('-').map(parseInt)))

echo "Part 1: ", sectionPairs.mapIt(int(it.fullOverlap)).sum
echo "Part 2: ", sectionPairs.mapIt(int(it.partialOverlap)).sum