from ..items.itemstack import ItemStack


class ClothingDisplay:
    """Data pertaining to an item to display clothing."""

    __slots__ = "items", "dyes"

    def __init__(self, items: list[ItemStack], dyes: list[ItemStack]):
        self.items: list[ItemStack] = items
        """What items is the display wearing."""

        self.dyes: list[ItemStack] = dyes
        """What dyes is the display wearing."""

    def __repr__(self):
        return f"<{self.__class__.__qualname__} with {self.total_count} items inside>"

    @property
    def items_count(self) -> int:
        return sum(1 for x in self.items if x is not None)

    @property
    def dyes_count(self) -> int:
        return sum(1 for x in self.items if x is not None)

    @property
    def total_count(self):
        return self.items_count + self.dyes_count
