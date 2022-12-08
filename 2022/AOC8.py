from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import io


class DIRECTION(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class TreePatch:
    heights_grid: list[list[int]]

    @property
    def size(self) -> int:
        # Assuming square.
        return len(self.heights_grid)

    def __init__(self, f: "io.TextIOWrapper") -> None:
        self.heights_grid = [[*map(int, line.strip())] for line in f.readlines()]

    def tree_visible_from_outside(self, ox: int, oy: int) -> bool:
        height = self.heights_grid[ox][oy]
        for direction in DIRECTION:
            x, y = ox, oy
            while 0 < x < self.size - 1 and 0 < y < self.size - 1:
                x, y = x + direction.value[0], y + direction.value[1]
                if self.heights_grid[x][y] >= height:
                    break
            else:
                return True
        return False

    def calc_tree_scenic_score(self, ox: int, oy: int) -> bool:
        height = self.heights_grid[ox][oy]
        score = 1
        for direction in DIRECTION:
            x, y = ox, oy
            direction_score = 0
            while 0 < x < self.size - 1 and 0 < y < self.size - 1:
                x, y = x + direction.value[0], y + direction.value[1]
                direction_score += 1
                if self.heights_grid[x][y] >= height:
                    break
            score *= direction_score
        return score

    def calc_stats(self) -> tuple[int, int]:
        n_visible = 0
        scenic_scores = []
        # For each tree in the patch
        for x in range(self.size):
            for y in range(self.size):
                n_visible += int(self.tree_visible_from_outside(x, y))
                scenic_scores.append(self.calc_tree_scenic_score(x, y))

        return n_visible, max(scenic_scores)


treepatch = TreePatch(open("8"))
n_visible, best_scenic_score = treepatch.calc_stats()

print(f"Part 1: {n_visible}")
print(f"Part 2: {best_scenic_score}")
