from __future__ import annotations


class Math:
	"""Math Helper Utility Class."""

	@staticmethod
	def clamp(x: float | int, minimum: float | int, maximum: float | int) -> float | int:
		"""Standard clamp between any two values."""
		return max(minimum, min(maximum, x))

	@staticmethod
	def lerp(minimum: float | int, maximum: float | int, amount: float | int) -> float | int:
		"""Standard Linear Interpolation."""
		return minimum + (maximum - minimum) * amount
