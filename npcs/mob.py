import typing
from ..enums import EntityType
from ..fileutils import Coordinates, FileReader


class Mob:
	"""A mob entity stored in the world."""

	__slots__ = "type", "position"

	def __init__(
		self,
		type_: EntityType,
		position: Coordinates,
	):
		self.type: EntityType = type_
		"""The entity's internal type ID."""

		self.position: Coordinates = position
		"""The world coordinates where this mob is located."""

	def __repr__(self):
		return f"<Mob {repr(self.type)} at {self.position}>"

	@classmethod
	def read(cls, fr: FileReader) -> "Mob":
		mob_type = EntityType(fr.int4())
		mob_position = Coordinates(fr.single(), fr.single())

		return cls(
			type_=mob_type,
			position=mob_position,
		)
