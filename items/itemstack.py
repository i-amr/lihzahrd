from typing import Optional
from ..fileutils import FileReader
from ..enums import ItemType, PrefixType


class ItemStack:
	"""A stack of a certain item."""

	__slots__ = "type", "quantity", "prefix"

	def __init__(
		self,
		type_: ItemType,
		quantity: int = 1,
		prefix: Optional[PrefixType] = None
	):
		self.type: ItemType = type_
		"""The type of item represented in this stack."""

		self.quantity: int = quantity
		"""A number from 1 to 999 representing the number of items inside this stack."""

		self.prefix: Optional[PrefixType] = prefix
		"""The modifier of the item in this stack. Should be set only when quantity is 1."""

	def __eq__(self, other):
		return (
			self.type == getattr(other, 'type', None)
			and self.quantity == getattr(other, 'quantity', None)
			and self.prefix == getattr(other, 'prefix', None)
		)

	def __repr__(self):
		return f"<ItemStack of {self.quantity}x {repr(self.type)} ({self.prefix})>"

	@classmethod
	def read(cls, fr: FileReader) -> "ItemStack":
		return cls(
			type_=ItemType.get(fr.int2()),
			prefix=PrefixType.get(fr.uint1()),
			quantity=fr.int2(),
		)
