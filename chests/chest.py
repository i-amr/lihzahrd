from ..header import Version
from ..items import ItemStack
from ..enums import ItemType, PrefixType
from ..fileutils import Coordinates, FileReader


class Chest:
	"""A chest with its contents."""

	max_capacity = 40

	__slots__ = "name", "position", "contents"

	def __init__(
		self, name: str, position: Coordinates, contents: list[ItemStack]
	):
		self.name: str = name
		self.position: Coordinates = position
		self.contents: list[ItemStack] = contents

	def __repr__(self):
		item_count = sum(1 for item in self.contents if item is not None)
		return (
			f'<Chest "{self.name}" at {self.position} '
			f"with {item_count} items>"
		)

	@classmethod
	def read(cls, fr: FileReader, version: Version, items_per_chest: int) -> "Chest":
		chest_position = Coordinates(x=fr.int4(), y=fr.int4())
		chest_name = fr.string()

		if version >= Version(294):
			items_per_chest = fr.int4()

		items_to_read = min(items_per_chest, cls.max_capacity)
		items_to_skip = max(0, items_per_chest - cls.max_capacity)

		chest_contents = []
		for _ in range(items_to_read):
			item_quantity = fr.int2()
			if item_quantity != 0:
				item_type = ItemType.get(fr.int4())
				item_modifier = PrefixType.get(fr.uint1())
				actual_quantity = item_quantity if item_quantity > 0 else 1

				item = ItemStack(
					type_=item_type,
					prefix=item_modifier,
					quantity=actual_quantity,
				)
			else:
				item = None
			chest_contents.append(item)

		# Skip overflow
		for _ in range(items_to_skip):
			if fr.int2() > 0:
				fr.int4()
				fr.uint1()

		return cls(
			name=chest_name,
			position=chest_position,
			contents=chest_contents,
		)
