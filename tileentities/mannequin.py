from ..header import Version
from ..fileutils import FileReader
from ..enums.posetype import PoseType
from ..items.itemstack import ItemStack
from .clothingdisplay import ClothingDisplay


class Mannequin(ClothingDisplay):
	"""
	Data container for Mannequin and Womannequin entities stored in a Terraria world file.

	This class holds the state of clothing displays,
	including armor, accessories, dyes, mount, held item, and pose.

	Wiki References:
		- https://terraria.wiki.gg/Mannequin
		- https://terraria.wiki.gg/Womannequin

	Attributes:
		gear (list[ItemStack | None]): 9 total equipment slots:
			- 1–3: Armor (Helmet, Shirt, Pants)
			- 4–8: Accessories
			- 9: Mount or Minecart
		dyes (list[ItemStack | None]): 9 total dye slots:
			- 1–3: Armor Dyes
			- 4–8: Accessory Dyes
			- 9: Mount/Minecart Dye
		misc (list[ItemStack | None]): 1 slot for a held item (e.g., a Sword).
		pose (int): The visual pose ID (introduced in world version 307).
	"""

	def __init__(
		self,
		gear: list[ItemStack],
		dyes: list[ItemStack],
		misc: list[ItemStack],
		pose: PoseType,
	):
		super().__init__(gear, dyes)

	@classmethod
	def read(cls, fr: FileReader, version: Version) -> "Mannequin":
		mannequin_gear: list[ItemStack] = [None] * 9
		mannequin_dyes: list[ItemStack] = [None] * 9
		mannequin_misc: list[ItemStack] = [None] * 1

		item_flags = fr.uint1()
		dye_flags = fr.uint1()

		mannequin_pose = fr.uint1() if version >= 307 else 0

		extra_flags = fr.uint1() if version >= 308 else 0

		effective_extra = extra_flags
		has_legacy_tail = False

		if version == 311:
			effective_extra &= ~0x02
			has_legacy_tail = bool(extra_flags & 0x02)

		item_mask = item_flags | (0x100 if (effective_extra & 0x02) else 0)
		dye_mask = dye_flags | (0x100 if (effective_extra & 0x04) else 0)

		for i in range(len(mannequin_gear)):
			if item_mask & (1 << i):
				mannequin_gear[i] = ItemStack.read(fr)

		for i in range(len(mannequin_dyes)):
			if dye_mask & (1 << i):
				mannequin_dyes[i] = ItemStack.read(fr)

		for i in range(len(mannequin_misc)):
			if effective_extra & (1 << i):
				mannequin_misc[i] = ItemStack.read(fr)

		if has_legacy_tail:
			mannequin_gear[8] = ItemStack.read(fr)

		return cls(
			gear=mannequin_gear,
			dyes=mannequin_dyes,
			misc=mannequin_misc,
			pose=mannequin_pose,
		)
