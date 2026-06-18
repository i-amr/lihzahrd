from ..fileutils import Coordinates, FileReader


class Sign:
	"""A sign with something written on it."""

	__slots__ = "text", "position"

	def __init__(self, text: str, position: Coordinates):
		self.text: str = text
		self.position: Coordinates = position

	def __repr__(self):
		return f'<Sign "{self.text}" at {self.position}>'

	@classmethod
	def read(cls, fr: FileReader) -> "Sign":
		sign_text = fr.string()
		sign_position = Coordinates(fr.int4(), fr.int4())

		return cls(
			text=sign_text, 
			position=sign_position,
		)
