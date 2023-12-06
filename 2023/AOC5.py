import json
import re


def range_intersect(r1, r2):
    return range(max(r1.start, r2.start), min(r1.stop, r2.stop)) or None


class Almanac:
    def __init__(self):
        # Hack the file contents to resemble json, then read it to a dict. :3
        almanac_str = open("5").read()
        almanac_str = almanac_str.replace(" map", "")
        almanac_str = re.sub(r"([\w-]+):", r'"\1":[', almanac_str)
        almanac_str = almanac_str.replace("\n\n", "],\n")
        almanac_str = re.sub(r"(\d+ )", r"\1,", almanac_str)
        almanac_str = re.sub(r"(\d+)\n", r"\1,", almanac_str)
        almanac_str = f"{{{almanac_str}]}}"
        almanac_dict = json.loads(almanac_str)
        almanac_dict["mappings"] = {"forward": {}, "reverse": {}}
        for k in list(almanac_dict.keys()):
            if "-to-" in k:
                mapping = almanac_dict.pop(k)
                from_, to_ = k.split("-to-")
                forward_ranges = {}
                reverse_ranges = {}
                for m in zip(mapping[::3], mapping[1::3], mapping[2::3]):
                    forward_ranges[m[1]] = (m[2], m[0])
                    reverse_ranges[m[0]] = (m[2], m[1])
                almanac_dict["mappings"]["forward"][from_] = {
                    "to": to_,
                    "ranges": dict(sorted(forward_ranges.items())),
                }
                almanac_dict["mappings"]["reverse"][to_] = {
                    "from": from_,
                    "ranges": dict(sorted(reverse_ranges.items())),
                }
        self.data = almanac_dict

    def get_mapped_ranges(self, category: str, search_range: range) -> list[range]:
        cur = search_range.start
        for s, d in self.data["mappings"]["reverse"][category]["ranges"].items():
            if s + d[0] < cur:
                continue
            if s >= search_range.stop:
                continue
            if s > cur:
                yield range(cur, s)
                cur = s
            yield range(cur - s + d[1], min(s + d[0], search_range.stop) - s + d[1])
            cur = s + d[0]
        yield range(cur, search_range.stop)

    def _find_lowest_seed(
        self, seed_ranges, category: str, search_range: range
    ) -> int | None:
        # print(f"Searching for {category} in range {range}")
        if category == "seed":
            for seed_range in seed_ranges:
                if ri := range_intersect(seed_range, search_range):
                    return ri.start
            return None
        # Iterate over ranges, starting from most favourable.
        for r in self.get_mapped_ranges(category, search_range):
            # print(f"Reviewing range {r}")
            if (
                lowest_seed := self._find_lowest_seed(
                    seed_ranges, self.data["mappings"]["reverse"][category]["from"], r
                )
            ) is not None:
                return lowest_seed
        return None

    def get_seed_location(self, seed: int) -> int:
        cur = ("seed", seed)
        while cur[0] != "location":
            cur_mapping = self.data["mappings"]["forward"][cur[0]]
            for r, v in cur_mapping["ranges"].items():
                if r <= cur[1] and r + v[0] > cur[1]:
                    cur = (cur_mapping["to"], cur[1] - r + v[1])
                    break
            else:
                cur = (cur_mapping["to"], cur[1])
        return cur[1]

    def get_closest_location(self, interpret_seeds_as_ranges: bool = False):
        if interpret_seeds_as_ranges:
            seed_ranges = [
                range(a, a + b)
                for a, b in sorted(
                    zip(self.data["seeds"][::2], self.data["seeds"][1::2])
                )
            ]
        else:
            seed_ranges = [range(x, x + 1) for x in self.data["seeds"]]

        return self.get_seed_location(
            self._find_lowest_seed(seed_ranges, "location", range(0, 10**12))
        )


print(f"Part 1: {Almanac().get_closest_location()}")
print(f"Part 2: {Almanac().get_closest_location(interpret_seeds_as_ranges=True)}")
