DIRECTIONS = {
    "U": (0, 1),
    "D": (0, -1),
    "L": (-1, 0),
    "R": (1, 0),
}


class Rope:
    def __init__(self, length: int):
        self.length = length
        self.knot_locs = [(0, 0)] * length
        self.locs_covered_by_knots = [{(0, 0)} for i in range(length)]

    def _move_head_in_dir(self, dir):
        self.knot_locs[0] = (
            self.knot_locs[0][0] + DIRECTIONS[dir][0],
            self.knot_locs[0][1] + DIRECTIONS[dir][1],
        )
        for i in range(1, self.length):
            diffx = self.knot_locs[i - 1][0] - self.knot_locs[i][0]
            diffy = self.knot_locs[i - 1][1] - self.knot_locs[i][1]
            movx = diffx // abs(diffx) if diffx != 0 else 0
            movy = diffy // abs(diffy) if diffy != 0 else 0
            if abs(diffx) + abs(diffy) > 2:
                self.knot_locs[i] = (
                    self.knot_locs[i][0] + movx,
                    self.knot_locs[i][1] + movy,
                )
            elif abs(diffx) > 1:
                self.knot_locs[i] = (self.knot_locs[i][0] + movx, self.knot_locs[i][1])
            elif abs(diffy) > 1:
                self.knot_locs[i] = (self.knot_locs[i][0], self.knot_locs[i][1] + movy)

            self.locs_covered_by_knots[i].add(self.knot_locs[i])

    def process_instructions(self, instructions: list[str]) -> None:
        for instruction in instructions:
            dir, n_moves = instruction.split()
            for _ in range(int(n_moves)):
                self._move_head_in_dir(dir)


rope = Rope(10)
rope.process_instructions(open("9").readlines())
print(f"Part 1: {len(rope.locs_covered_by_knots[1])}")
print(f"Part 2: {len(rope.locs_covered_by_knots[9])}")
