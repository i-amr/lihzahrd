import enum


class FileType(enum.IntEnum):
    """Terraria's File Type."""

    NONE = 0
    MAP = 1
    WORLD = 2
    PLAYER = 3

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"
