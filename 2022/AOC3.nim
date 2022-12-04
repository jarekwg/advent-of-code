import math, sequtils, sets, strutils

let rucksacks = readFile("3").splitLines

proc common(sets: seq[string]): char =
    return sets.mapIt(it.toHashSet).foldl(a*b).toSeq[0]

proc prio(c: char): int =
    return if c.ord > 96: c.ord - 96 else: c.ord - 38

echo "Part 1: ", rucksacks.mapIt(it.toSeq.distribute(2).mapIt(it.join).common.prio).sum
echo "Part 2: ", rucksacks.distribute(int(rucksacks.len/3)).mapIt(it.common.prio).sum