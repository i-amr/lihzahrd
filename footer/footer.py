from __future__ import annotations

from ..fileutils import FileReader, FileWriter
from ..errors import FooterError

class Footer:
	def __init__(self, label: str, world_id: int):
		self.label = label
		self.world_id = world_id

	@classmethod
	def read(cls, fr: FileReader, expected_label: str, expected_id: int) -> Footer:
		tail = fr.bool()
		if not tail:
			raise FooterError("Footer handshake failed.")

		found_label = fr.string()
		if found_label != expected_label:
			raise FooterError(f"Footer label mismatch. Expected '{expected_label}', got '{found_label}'")

		found_id = fr.int4()
		if found_id != expected_id:
			raise FooterError(f"Footer ID mismatch. Expected {expected_id}, got {found_id}")

		return cls(label=found_label, world_id=found_id)

	def write(self, fw: FileWriter) -> None:
		fw.bool(True)
		fw.string(self.label)
		fw.int4(self.world_id)
