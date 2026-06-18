from typing import *
from ..enums import BlockType


class SavedOreTiers:
    """The types of ores that generated in the world."""

    def __init__(
        self,
        tier_1: BlockType,
        tier_2: BlockType,
        tier_3: BlockType,
        tier_4: BlockType,
        # Hardmode
        tier_5: Optional[BlockType],
        tier_6: Optional[BlockType],
        tier_7: Optional[BlockType],
    ):
        self.tier_1: BlockType = tier_1
        """Copper or Tin?"""
        assert self.tier_1 == BlockType.COPPER or self.tier_1 == BlockType.TIN

        self.tier_2: BlockType = tier_2
        """Iron or Lead?"""
        assert self.tier_2 == BlockType.IRON or self.tier_2 == BlockType.LEAD

        self.tier_3: BlockType = tier_3
        """Silver or Tungsten?"""
        assert self.tier_3 == BlockType.SILVER or self.tier_3 == BlockType.TUNGSTEN

        self.tier_4: BlockType = tier_4
        """Gold or Platinum?"""
        assert self.tier_4 == BlockType.GOLD or self.tier_4 == BlockType.PLATINUM

        self.tier_5: Optional[BlockType] = tier_5
        """Cobalt or Palladium? None if it hasn't been determined yet."""
        assert (
            self.tier_5 == BlockType.NONE
            or self.tier_5 == BlockType.COBALT
            or self.tier_5 == BlockType.PALLADIUM
        )

        self.tier_6: Optional[BlockType] = tier_6
        """Mythril or Orichalcum? None if it hasn't been determined yet."""
        assert (
            self.tier_6 == BlockType.NONE
            or self.tier_6 == BlockType.MYTHRIL
            or self.tier_6 == BlockType.ORICHALCUM
        )

        self.tier_7: Optional[BlockType] = tier_7
        """Adamantite or Titanium? None if it hasn't been determined yet."""
        assert (
            self.tier_7 == BlockType.NONE
            or self.tier_7 == BlockType.ADAMANTITE
            or self.tier_7 == BlockType.TITANIUM
        )

    def __repr__(self):
        return f"<SavedOreTiers>"
