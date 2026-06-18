from typing import Optional
from .mob import Mob
from ..header import Version
from ..enums import EntityType
from ..fileutils import Coordinates, FileReader


class NPC(Mob):
	"""An NPC entity stored in the world."""

	__slots__ = "name", "type", "position", "variation_index", "home"

	def __init__(
		self,
		name: str,
		type_: EntityType,
		position: Coordinates,
		variation_index: int,
		home: Optional[Coordinates] = None,
	):
		super().__init__(type_, position)

		self.name: str = name
		"""The name given to this NPC."""

		self.home: Optional[Coordinates] = home
		"""The tile coordinates of this NPC's home, or ``None`` if they are currently homeless."""

		self.variation_index: int = variation_index
		"""The visual variation of this NPC, e.g., Zoologist's lunar form.
		See: https://terraria.wiki.gg/wiki/NPCs"""

	def __repr__(self):
		return f"<NPC {repr(self.type)} at {self.position}>"

	@classmethod
	def read(cls, fr: FileReader, version: Version) -> "NPC":
		npc_type = EntityType(fr.int4())
		npc_name = fr.string()  # e.g. Bruno
		npc_position = Coordinates(fr.single(), fr.single())
		is_homeless = fr.bool()
		npc_home = Coordinates(fr.int4(), fr.int4())
		if is_homeless:
			npc_home = None

		npc_flags = fr.bits()
		npc_variation_index = fr.int4() if npc_flags[0] else 0

		is_homeless_despawn = version >= Version(315) and fr.bool()

		return cls(
			name=npc_name,
			type_=npc_type,
			home=npc_home,
			position=npc_position,
			variation_index=npc_variation_index,
		)
