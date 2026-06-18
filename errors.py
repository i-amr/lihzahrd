class LihzahrdError(Exception):
	"""Base exception for all errors in the Lihzahrd library."""

class FormatException(LihzahrdError):
	"""Raised when the file structure or signature is fundamentally broken."""

class MetadataError(FormatException):
	"""Raised when the file header/metadata block contains invalid data."""

class UnsupportedVersionError(MetadataError):
	"""Raised when the world file version is too old or too new to be parsed."""

class FooterError(FormatException):
	"""Raised when the file tail/footer validation fails."""

class SectionError(FormatException):
	"""Raised when the reader's position does not match the expected section pointer."""
