from ..fileutils import FileReader
from ..items.itemstack import ItemStack


class SingleItemDisplay:
	"""Base class for Tile Entities that hold exactly one single item.

	See:
		Weapon Rack: https://terraria.wiki.gg/Weapon_Rack
		Item Frame: https://terraria.wiki.gg/Item_Frame
		Plate: https://terraria.wiki.gg/Plate
	"""

	__slots__ = ("item",)

	def __init__(self, item: ItemStack):
		self.item: ItemStack = item

	def __repr__(self):
		return f"<{self.__class__.__qualname__} with {repr(self.item)} inside>"

	@classmethod
	def read(cls, fr: FileReader) -> "SingleItemDisplay":
		return cls(
			item=ItemStack.read(fr),
		)
