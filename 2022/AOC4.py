from dataclasses import dataclass


@dataclass
class Section:
    start: int
    end: int

    @classmethod
    def from_str(cls, sectionstr: str):
        return cls(*map(int, sectionstr.split("-")))

    def __le__(self, other: "Section"):
        """Using less-than-or-equal operator as pseudo subset operator.."""
        return self.start >= other.start and self.end <= other.end


def sectionsFullyOverlap(a: Section, b: Section):
    return a <= b or b <= a


def sectionsPartiallyOverlap(a: Section, b: Section):
    return a.start <= b.end and a.end >= b.start


print(
    f"""Part 1: {sum(sectionsFullyOverlap(*map(Section.from_str, line.split(","))) for line in open("4"))}"""
)
print(
    f"""Part 2: {sum(sectionsPartiallyOverlap(*map(Section.from_str, line.split(","))) for line in open("4"))}"""
)
