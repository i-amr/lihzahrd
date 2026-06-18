import enum


class WireType(enum.IntEnum):
    """All possible types of wires."""

    RED = 0
    BLUE = 1
    GREEN = 2
    YELLOW = 3

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"
