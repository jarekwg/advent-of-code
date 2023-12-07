from collections import Counter
from dataclasses import dataclass


@dataclass
class Hand:
    _cards: str
    bid: int
    jack_is_joker: bool = False

    def __init__(self, hand_str: str) -> None:
        self._cards, bid_str = hand_str.split()
        self.bid = int(bid_str)

    def __gt__(self, other):
        return self.score > other.score

    @property
    def cards(self):
        if Hand.jack_is_joker:
            return self._cards.replace("J", "*")
        else:
            return self._cards

    @property
    def category(self) -> int:
        c = Counter(self.cards)
        match sorted(c.values(), reverse=True):
            case [5]:
                return 7
            case [4, _]:
                if "*" in self.cards:
                    return 7
                return 6
            case [3, 2]:
                if "*" in self.cards:
                    return 7
                return 5
            case [3, *_]:
                if c.get("*", 0) in [1, 3]:
                    return 6
                return 4
            case [2, 2, _]:
                if c.get("*", 0) == 1:
                    return 5
                if c.get("*", 0) == 2:
                    return 6
                return 3
            case [2, *_]:
                if c.get("*", 0) in [1, 2]:
                    return 4
                return 2
            case _:
                if "*" in self.cards:
                    return 2
                return 1

    @property
    def second_score(self) -> int:
        weights = "*23456789TJQKA"
        score = 0
        for i, c in enumerate(self.cards):
            score += 15 ** (5 - i) * weights.index(c)
        return score

    @property
    def score(self) -> tuple[int, int]:
        return (self.category, self.second_score)


def total_winnings(hands: list[Hand], jack_is_joker: bool = False) -> int:
    Hand.jack_is_joker = jack_is_joker  # toggle Hand's behaviour
    ranked_hands = sorted(hands)
    result = 0
    for i, h in enumerate(ranked_hands):
        result += (i + 1) * h.bid
    return result


hands = [*map(Hand, open("7").readlines())]
print(f"Part 2: {total_winnings(hands)}")
print(f"Part 2: {total_winnings(hands, jack_is_joker=True)}")
