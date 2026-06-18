import enum


class LayerType(enum.IntEnum):
    """All possible types of depth layers."""

    SPACE = -1
    SURFACE = 0
    UNDERGROUND = 1  # Dirt
    CAVERN = 2  # Rock
    UNDERWORLD = 3  # Hell

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"
