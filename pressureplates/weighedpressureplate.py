from __future__ import annotations
from ..fileutils import Coordinates, FileReader


class WeighedPressurePlate:
	"""A single `Weighed Pressure Plate <https://terraria.wiki.gg/Pressure_Plates>`_ placed in the world."""

	__slots__ = ("position",)

	def __init__(self, position: Coordinates):
		self.position: Coordinates = position

	def __repr__(self):
		return f"PressurePlate(position={self.position})"

	@classmethod
	def read(cls, fr: FileReader) -> WeighedPressurePlate:
		return cls(
			position=Coordinates(
				fr.int4(),
				fr.int4(),
			),
		)
