from dataclasses import dataclass, field
from enum import Enum


class RockShape(Enum):
    HORZ = (-1 + 4j, 0 + 4j, 1 + 4j, 2 + 4j)
    PLUS = (-1 + 5j, 0 + 4j, 0 + 5j, 0 + 6j, 1 + 5j)
    ANGL = (-1 + 4j, 0 + 4j, 1 + 4j, 1 + 5j, 1 + 6j)
    VERT = (-1 + 4j, -1 + 5j, -1 + 6j, -1 + 7j)
    SQRE = (-1 + 4j, -1 + 5j, 0 + 4j, 0 + 5j)


@dataclass
class Rock:
    shape: RockShape
    pos: complex
    chamber: "Chamber"

    def move(self, delta: complex) -> bool:
        self.pos += delta
        # Report on whether all points are happy (haven't hit walls, or another rock).
        for p in self.shape.value:
            p += self.pos
            if (
                not (-3 <= p.real <= 3)
                or p in self.chamber.settled_rocks
                or p.imag == 0
            ):
                self.pos -= delta
                return False
        return True

    def ossify(self) -> None:
        for p in self.shape.value:
            p += self.pos
            self.chamber.settled_rocks.add(p)
            self.chamber.cur_max_elevation = round(
                max(self.chamber.cur_max_elevation, p.imag)
            )

    def __repr__(self) -> str:
        return ""


@dataclass
class Chamber:
    jet_sequence: str
    rock_shape_sequence: list[RockShape]
    settled_rocks: set[complex] = field(default_factory=set)
    cur_max_elevation: int = 0

    jet_iterpos: int = -1
    rock_shape_iterpos: int = -1

    def draw(self) -> None:
        for y_ in range(self.cur_max_elevation):
            y = self.cur_max_elevation - y_
            for x in range(-3, 4):
                print("#" if x + y * 1j in self.settled_rocks else ".", end="")
            print()

    def get_normalised_elevations(self) -> tuple:
        heights = []
        for x in range(-3, 4):
            y = self.cur_max_elevation
            while not (x + y * 1j in self.settled_rocks or y == 0):
                y -= 1
            heights.append(y - self.cur_max_elevation)
        return tuple(heights)

    def get_next_jet(self) -> str:
        self.jet_iterpos = (self.jet_iterpos + 1) % len(self.jet_sequence)
        return self.jet_sequence[self.jet_iterpos]

    def get_next_rock(self) -> Rock:
        self.rock_shape_iterpos = (self.rock_shape_iterpos + 1) % len(
            self.rock_shape_sequence
        )
        return Rock(
            shape=self.rock_shape_sequence[self.rock_shape_iterpos],
            pos=self.cur_max_elevation * 1j,
            chamber=self,
        )

    def get_state(self) -> tuple[tuple[int], int, int]:
        return (
            self.get_normalised_elevations(),
            self.jet_iterpos,
            self.rock_shape_iterpos,
        )


def drop_rocks_and_calc_height(n_rocks: int) -> int:
    encountered_states = {}
    rocks_fallen = 0
    chamber = Chamber(
        jet_sequence=open("17").read(),
        rock_shape_sequence=list(RockShape.__members__.values()),
    )
    while rocks_fallen < n_rocks:
        # Draw new rock.
        rock = chamber.get_next_rock()
        # print(f"[{rocks_fallen}] Dropping rock {rock}")

        while True:
            # Move rock by jet (or not if blocked).
            rock.move(-1 if chamber.get_next_jet() == "<" else 1)

            # Move rock down (or if blocked, break the loop).
            if not rock.move(-1j):
                break

        # Add settled rock to chamber.
        rock.ossify()
        rocks_fallen += 1
        # chamber.draw()

        # Review whether we've seen this state before.
        state = chamber.get_state()
        if state in encountered_states:
            # FAST TRACK!!
            rocks_to_increment = rocks_fallen - encountered_states[state][0]
            height_to_increment = (
                chamber.cur_max_elevation - encountered_states[state][1]
            )

            n_increments = (n_rocks - rocks_fallen) // rocks_to_increment

            # print(f"[{rocks_fallen}] Dropping {n_increments * rocks_to_increment} rocks!")
            rocks_fallen += n_increments * rocks_to_increment
            chamber.cur_max_elevation += n_increments * height_to_increment

            # Create new floor for remaining rocks.
            heights = list(state[0])
            for x in range(-3, 4):
                chamber.settled_rocks.add(
                    x + (heights.pop(0) + chamber.cur_max_elevation) * 1j
                )

            encountered_states = {}
        else:
            encountered_states[state] = (rocks_fallen, chamber.cur_max_elevation)
    return chamber.cur_max_elevation


print(f"Part 1: {drop_rocks_and_calc_height(2022)}")
print(f"Part 2: {drop_rocks_and_calc_height(1_000_000_000_000)}")
