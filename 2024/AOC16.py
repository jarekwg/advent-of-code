from dataclasses import dataclass
from enum import IntEnum
from math import inf
from typing import Self


class Dir(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


DELTAS = {
    Dir.NORTH: (0, -1),
    Dir.EAST: (1, 0),
    Dir.SOUTH: (0, 1),
    Dir.WEST: (-1, 0),
}


# Translate the maze to a graph of nodes (branching points) and edges (connections between these)
@dataclass
class Node:
    x: int
    y: int
    d: Dir  # The way you're facing essentially becomes a third dimension.
    fwds: dict[
        Self, tuple[int, set[tuple[int, int]]]
    ]  # Reachable neighbours and the score&tiles to get there.

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.d))

    @property
    def xy(self) -> tuple[int, int]:
        return self.x, self.y


@dataclass
class Graph:
    start: Node
    ends: set[Node]

    def __init__(self, maze: list[list[str]]) -> None:
        self.maze = maze
        # Identify all nodes in the maze.
        nodes: dict[tuple[int, int, Dir], Node] = {}
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if cell == "#":
                    continue
                for d in Dir:
                    nodes[(x, y, d)] = Node(x, y, d, {})
                if cell == "S":
                    self.start = nodes[(x, y, Dir.EAST)]
                if cell == "E":
                    self.ends = {nodes[(x, y, d)] for d in Dir}

        # Connect the nodes with edges.
        for (x, y, d), node in nodes.items():
            dx, dy = DELTAS[d]
            if (x + dx, y + dy, d) in nodes:
                node.fwds[nodes[(x + dx, y + dy, d)]] = (1, {(x + dx, y + dy)})
            for rot in (-1, +1):
                node.fwds[nodes[(x, y, Dir((d + rot) % 4))]] = (1000, set())

    def display(self, tiles: set[tuple[int, int]]) -> None:
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                if cell == "#":
                    print("#", end="")
                elif (x, y) in tiles:
                    print("O", end="")
                else:
                    print(".", end="")
            print()

    def calc_lowest_score_and_tilecount(self) -> tuple[int, int]:
        # Reduce the graph until all edges have been processed.
        alltime_scores: dict[Node, tuple[int, set[tuple[int, int]]]] = (
            self.start.fwds.copy()
        )
        while self.start.fwds:
            # Pop the node with the lowest score.
            popped_node = min(self.start.fwds, key=lambda fwd: self.start.fwds[fwd][0])
            popped_score, popped_tiles = self.start.fwds.pop(popped_node)
            for fwd, (fwd_score, fwd_tiles) in popped_node.fwds.items():
                if fwd == self.start:
                    continue
                new_score = popped_score + fwd_score
                # If this is a new best score for getting to the node, add it.
                if new_score < alltime_scores.get(fwd, (inf, set()))[0]:
                    alltime_scores[fwd] = self.start.fwds[fwd] = (
                        new_score,
                        popped_tiles | fwd_tiles,
                    )
                # If this is a tie for the best score with an existing node, add it and combine the tiles.
                elif new_score == self.start.fwds.get(fwd, (inf, set()))[0]:
                    alltime_scores[fwd] = self.start.fwds[fwd] = (
                        new_score,
                        popped_tiles | fwd_tiles | self.start.fwds[fwd][1],
                    )
        actual_end = min(self.ends, key=lambda end: alltime_scores.get(end, inf))

        score, tiles = alltime_scores[actual_end]
        tiles |= {self.start.xy}

        self.display(tiles)
        return score, len(tiles)


graph = Graph([*map(list, open("16").read().splitlines())])

lowest_score, tilecount = graph.calc_lowest_score_and_tilecount()

print(f"Part 1: {lowest_score}")
print(f"Part 2: {tilecount}")
