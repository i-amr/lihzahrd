class Dimensions:
    """A pair of dimensions."""

    __slots__ = "w", "h"

    def __init__(self, w, h) -> None:
        self.w = w
        self.h = h

    def __repr__(self) -> str:
        return f"Dimensions({self.w}, {self.h})"

    def __str__(self) -> str:
        return f"{self.w}, {self.h}"

    def __len__(self) -> int:
        if self.w != 0 and self.h != 0:
            return self.w * self.h
        return self.w + self.h

    def __eq__(self, other) -> bool:
        return self.w == other.w and self.h == other.h

    def __ne__(self, other) -> bool:
        return self.w != other.w or self.h != other.h

    def __gt__(self, other) -> bool:
        return self.w > other.w and self.h > other.h

    def __ge__(self, other) -> bool:
        return self.w >= other.w and self.h >= other.h

    def __lt__(self, other) -> bool:
        return self.w < other.w and self.h < other.h

    def __le__(self, other) -> bool:
        return self.w <= other.w and self.h <= other.h
