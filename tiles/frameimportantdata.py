class FrameImportantData:
    """Frame data of FrameImportant blocks.

    Some blocks share the same type and texture of other blocks (ex: banners), so they store some texture data inside
    the save file."""

    __slots__ = "x", "y"

    def __init__(self, x, y):
        self.x: int = x
        self.y: int = y

    def copy(self):
        return FrameImportantData(
            x=self.x,
            y=self.y,
        )

    def __repr__(self):
        return f"FrameImportantData(x={self.x}, y={self.y})"
