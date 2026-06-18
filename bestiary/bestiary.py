from __future__ import annotations
from ..fileutils import FileReader
from ..enums import EntityType


class Bestiary:
	"""A bestiary entry."""

	__slots__ = "chats", "kills", "sights"

	def __init__(
		self,
		chats: list[EntityType],
		kills: dict[EntityType, int],
		sights: list[EntityType],
	):
		self.chats: list[EntityType] = chats
		self.kills: dict[EntityType, int] = kills
		self.sights: list[EntityType] = sights

	def __repr__(self):
		return f"<Bestiary with {len(self.chats) + len(self.kills.keys()) + len(self.sightings)} entries>"

	@classmethod
	def read(cls, fr: FileReader) -> Bestiary:
		bestiary_kills = {EntityType.get(fr.string()): fr.int4() for _ in range(fr.int4())}
		bestiary_sights = [EntityType.get(fr.string()) for _ in range(fr.int4())]
		bestiary_chats = [EntityType.get(fr.string()) for _ in range(fr.int4())]

		return cls(
			kills=bestiary_kills,
			chats=bestiary_chats,
			sightings=bestiary_sights,
		)
