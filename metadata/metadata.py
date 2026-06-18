from __future__ import annotations

from ..enums import FileType
from ..fileutils import FileReader, FileWriter
from ..errors import MetadataError


class Metadata:
	__slots__ = ["file_type", "revision", "is_favorite", "signature"]

	def __init__(
		self,
		file_type: FileType,
		revision: int,
		signature: str,
		is_favorite: bool,
	):
		self.signature = signature
		self.file_type = file_type
		self.revision = revision
		self.is_favorite = is_favorite

	@classmethod
	def read(cls, fr: FileReader, expected_type: FileType) -> Metadata:
		signature: str = fr.string(7)
		if signature != "relogic":
			raise MetadataError("Expected Re-Logic file signature.")

		ftype: int = FileType(fr.uint1())
		if ftype != expected_type:
			raise MetadataError(f'Metadata file type mismatch. Expected "{expected_type.name}", got "{ftype.name}"')

		revision: int = fr.uint4()
		is_favorite: bool = fr.uint8() & 1 == 1

		return Metadata(
			file_type=ftype,
			revision=revision, 
			signature=signature,
			is_favorite=is_favorite,
		)

	def write(self, fw: FileWriter) -> None:
		fw.string(self.signature, leb128=False)
		fw.uint1(self.file_type)
		fw.uint4(self.revision)
		fw.uint8(self.is_favorite)
