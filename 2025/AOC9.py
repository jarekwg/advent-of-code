from dataclasses import dataclass

import matplotlib.pyplot as plt


@dataclass(frozen=True)
class Tile:
    x: int
    y: int

    def area_to(self, other: "Tile") -> int:
        return (abs(self.x - other.x) + 1) * (abs(self.y - other.y) + 1)


@dataclass(frozen=True)
class HLine:
    x1: int
    x2: int
    y: int


@dataclass(frozen=True)
class VLine:
    x: int
    y1: int
    y2: int


# Load up red tiles.
tiles = [Tile(*map(int, line.split(","))) for line in open("9").read().splitlines()]

# Calc all possible rectangles between any pair of red tiles and sort these by area.
rectangles = []
tiles_to_iterate = tiles.copy()
while tiles_to_iterate:
    tile = tiles_to_iterate.pop(0)
    rectangles.extend(
        [(tile.area_to(other), tile, other) for other in tiles_to_iterate]
    )

rectangles = sorted(rectangles, key=lambda x: x[0], reverse=True)


print(f"Part1: {rectangles[0][0]}")

# Construct sets of horizontal and vertical lines that make up the polygon.
polygon_hlines = list[HLine]()
polygon_vlines = list[VLine]()
prev_tile = tiles[-1]
for tile in tiles:
    if tile.y == prev_tile.y:
        polygon_hlines.append(
            HLine(min(prev_tile.x, tile.x), max(prev_tile.x, tile.x), tile.y)
        )
    else:
        polygon_vlines.append(
            VLine(tile.x, min(prev_tile.y, tile.y), max(prev_tile.y, tile.y))
        )
    prev_tile = tile

# Sort our lists of lines by their static coordinate to reduce iteration a bit.
polygon_hlines.sort(key=lambda x: x.y)
polygon_vlines.sort(key=lambda x: x.x)


def rect_intersects_polygon(x1: int, x2: int, y1: int, y2: int) -> bool:
    # - check our rectangle's hlines.
    for hline in (HLine(x1, x2, y1), HLine(x1, x2, y2)):
        for vline in polygon_vlines:
            # Skip ahead if vlines don't yet lie along the hline's xrange.
            if vline.x <= hline.x1:
                continue
            # Bail out early if vlines are past the hline's xrange.
            if vline.x >= hline.x2:
                break
            # If vline touches the hline, then we need to check other end to know if we're safe.
            if hline.y in (vline.y1, vline.y2):
                # Check if the hline's xrange intersects with the vline's xrange.
                if y1 <= vline.y1 <= y2 and y1 <= vline.y2 <= y2:
                    return True
            # If vline cleanly crosses the hline, we have trouble.
            if vline.y1 < hline.y < vline.y2:
                return True
    # - check our rectangle's vlines; same as above
    for vline in (VLine(x1, y1, y2), VLine(x2, y1, y2)):
        for hline in polygon_hlines:
            if hline.y <= vline.y1:
                continue
            if hline.y >= vline.y2:
                break
            if vline.x in (hline.x1, hline.x2):
                if x1 <= hline.x1 <= x2 and x1 <= hline.x2 <= x2:
                    return True
            if hline.x1 < vline.x < hline.x2:
                return True
    return False


def point_inside_polygon(x: int, y: int) -> bool:
    # Determine "outsideness" based on how many times the line 0,y->x,y crosses polygon vlines.
    # We offset y by 0.1, to avoid edge cases.
    is_outside = True
    for vline in polygon_vlines:
        if vline.x >= x:
            return is_outside
        if vline.y1 < y + 0.1 < vline.y2:
            is_outside = not is_outside
    return False


def plot_polygon(points: list[Tile]):
    closed_points = list(tiles) + [tiles[0]]
    cx = [p.x for p in closed_points]
    cy = [p.y for p in closed_points]
    plt.plot(cx, cy, marker=".")


def plot_rect(t1: Tile, t2: Tile):
    cx = [t1.x, t2.x, t2.x, t1.x, t1.x]
    cy = [t1.y, t1.y, t2.y, t2.y, t1.y]
    plt.plot(cx, cy, marker=".")


# Iterate over each rectangle until we find one that is contained within the polygon.
for area, t1, t2 in rectangles:
    # 1. Ensure none of our rectangle's boundaries intersect w the polygon's
    if rect_intersects_polygon(
        min(t1.x, t2.x), max(t1.x, t2.x), min(t1.y, t2.y), max(t1.y, t2.y)
    ):
        continue

    # 2. Ensure our rectangle is on the inside and not the outside of the polygon.
    if point_inside_polygon(min(t1.x, t2.x) + 1, min(t1.y, t2.y) + 1):
        continue

    print(f"Part2: {area}")
    plot_polygon(tiles)
    plot_rect(t1, t2)
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    ax = plt.gca()
    ax.set_axis_off()
    plt.show()
    break
