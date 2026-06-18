from __future__ import annotations
from ..fileutils import FileReader
from ..enums import ItemType

class AnchorBase:
	def __init__(self, type_: ItemType):
		self.type: ItemType = type_

	def __str__(self):
		raw_name = getattr(self.type, 'name', "Unknown")
		formatted_name = raw_name.replace('_', ' ').title()
		value = getattr(self.type, 'value', 0)
		return f"{formatted_name} - (ID: {value})"

	def __repr__(self):
		return f"{self.__class__.__name__}(type={self.value})"

	@classmethod
	def read(cls, fr: FileReader) -> AnchorBase:
		return cls(
			type_=fr.int2(),
		)
