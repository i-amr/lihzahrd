class Coordinates:
    """A pair of coordinates."""

    __slots__ = "x", "y"

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Coordinates({self.x}, {self.y})"

    def __str__(self) -> str:
        return f"{self.x}, {self.y}"

    def __len__(self) -> int:
        if self.x != 0 and self.y != 0:
            return self.x * self.y
        return self.x + self.y

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other) -> bool:
        return self.x != other.x or self.y != other.y

    def __gt__(self, other) -> bool:
        return self.x > other.x and self.y > other.y

    def __ge__(self, other) -> bool:
        return self.x >= other.x and self.y >= other.y

    def __lt__(self, other) -> bool:
        return self.x < other.x and self.y < other.y

    def __le__(self, other) -> bool:
        return self.x <= other.x and self.y <= other.y
