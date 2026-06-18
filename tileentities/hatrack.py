from .clothingdisplay import ClothingDisplay
from ..fileutils import FileReader
from ..items.itemstack import ItemStack


class HatRack(ClothingDisplay):
	"""A `Hat Rack <https://terraria.wiki.gg/Hat_Rack>`_ containing up to 2 dyed helmets."""

	def __init__(self, items: list[ItemStack], dyes: list[ItemStack]):
		super().__init__(items, dyes)
		assert len(items) == 2 and len(dyes) == 2

	@classmethod
	def read(cls, fr: FileReader) -> "HatRack":
		item_flags = fr.bits()

		rack_items: list[ItemStack | None] = [None for _ in range(2)]
		for index, flag in enumerate(item_flags[0:2]):
			if flag:
				rack_items[index] = ItemStack.read(fr)

		rack_dyes: list[ItemStack | None] = [None for _ in range(2)]
		for index, flag in enumerate(item_flags[2:4]):
			if flag:
				rack_dyes[index] = ItemStack.read(fr)

		return cls(
			items=rack_items,
			dyes=rack_dyes,
		)
