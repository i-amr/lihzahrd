import enum


class RarityType(enum.IntEnum):
    """All possible types of item rarity."""

    AMBER = -11
    TRASH = -1
    WHITE = 0
    BLUE = 1
    GREEN = 2
    ORANGE = 3
    LIGHT_RED = 4
    PINK = 5
    LIGHT_PURPLE = 6
    LIME = 7
    YELLOW = 8
    CYAN = 9
    STRONG_RED = 10
    PURPLE = 11

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"
