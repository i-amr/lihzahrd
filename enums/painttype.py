import enum


__all__ = ["PaintType", "PaintCoatingType"]


class PaintType(enum.IntEnum):
    """All possible types of paints."""

    NONE = 0
    RED_PAINT = 1
    ORANGE_PAINT = 2
    YELLOW_PAINT = 3
    LIME_PAINT = 4
    GREEN_PAINT = 5
    TEAL_PAINT = 6
    CYAN_PAINT = 7
    SKY_BLUE_PAINT = 8
    BLUE_PAINT = 9
    PURPLE_PAINT = 10
    VIOLET_PAINT = 11
    PINK_PAINT = 12
    DEEP_RED_PAINT = 13
    DEEP_ORANGE_PAINT = 14
    DEEP_YELLOW_PAINT = 15
    DEEP_LIME_PAINT = 16
    DEEP_GREEN_PAINT = 17
    DEEP_TEAL_PAINT = 18
    DEEP_CYAN_PAINT = 19
    DEEP_SKY_BLUE_PAINT = 20
    DEEP_BLUE_PAINT = 21
    DEEP_PURPLE_PAINT = 22
    DEEP_VIOLET_PAINT = 23
    DEEP_PINK_PAINT = 24
    BLACK_PAINT = 25
    WHITE_PAINT = 26
    GRAY_PAINT = 27
    BROWN_PAINT = 28
    SHADOW_PAINT = 29
    NEGATIVE_PAINT = 30
    ILLUMINANT_PAINT = 31

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"


class PaintCoatingType(enum.IntEnum):
    """All possible types of coating paints."""

    NONE = 0
    GLOW = 1
    ECHO = 2

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"
