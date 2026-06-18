from __future__ import annotations
from ..fileutils import Coordinates, FileReader
from ..enums import EntityType


class Room:
	__slots__ = "npc", "position"

	def __init__(self, npc: EntityType, position: Coordinates):
		self.npc: EntityType = npc
		self.position: Coordinates = position

	def __repr__(self):
		return f"<Room for {self.npc} at {self.position}>"

	@classmethod
	def read(cls, fr: FileReader) -> Room:
		return cls(
			npc=EntityType(
				fr.int4(),
			),
			position=Coordinates(
				fr.int4(),
				fr.int4(),
			),
		)
