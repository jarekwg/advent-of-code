import algorithm, math, sequtils, strutils

let elfloads = readFile("1").strip.split("\n\n").mapIt(
    it.split.map(parseInt).sum
)
echo "Part 1: ", elfloads.max
echo "Part 2: ", elfloads.sorted[^3..^1].sum

# # ALTERNATIVE SYNTAX -- not sure I like that this is possible
# let elfloads = mapIt(split(strip(readFile("1")), "\n\n"), sum(map(split(it), parseInt)))
# echo "Part 1: ", max(elfloads)
# echo "Part 2: ", sum(sorted(elfloads)[^3..^1])
