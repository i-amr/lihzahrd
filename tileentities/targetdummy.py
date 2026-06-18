from __future__ import annotations
from ..fileutils import FileReader


class TargetDummy:
	"""Data pertaining to a Target Dummy (https://terraria.wiki.gg/Target_Dummy)"""

	def __init__(self, bound_npc_index: int):
		# A Target Dummy consists of two distinct parts: 
		# 1. The 'Tile' (the physical wooden frame placed in the world).
		# 2. The 'NPC' (an invisible entity, type 488, that handles hit detection and damage).
		# This index links the Tile Entity to its corresponding NPC in the global NPC array.
		# When a player gets close it spawns the second part, so we can hit it and see damage numbers.
		# A value of -1 indicates no NPC is currently spawned.
		#
		# Based on TETrainingDummy.Activate(): Spawns a type 488 NPC (the straw man) to handle hit detection by calling NPC.NewNPC(...).
		# Based on TETrainingDummy.Update(): Spawns the NPC only if a player is nearby (checks if playerBox.Intersects(rectangle)). 
		# Note: The detection area is roughly 3200x3200 pixels (200x200 tiles) around the dummy via rectangle.Inflate(1600, 1600).
		self.bound_npc_index: int = bound_npc_index

	def __repr__(self):
		return f"TargetDummy(bound_npc_index={self.bound_npc_index})"

	@classmethod
	def read(cls, fr: FileReader) -> TargetDummy:
		return cls(
			bound_npc_index=fr.int2(),
		)
