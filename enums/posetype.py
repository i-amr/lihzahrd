import enum


class PoseType(enum.IntEnum):
    """All possible types of display doll poses."""

    STANDING = 0
    SITTING  = 1
    JUMPING  = 2
    WALKING  = 3

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"
