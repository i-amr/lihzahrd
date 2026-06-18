from __future__ import annotations

from .math import Math


class Utils:
    """Utility Class."""

    @staticmethod
    def smooth_step(
        x: float,
        minimum: float,
        maximum: float,
        clamped: bool = True,
    ) -> float:
        """
        Stepping smoothly between minimum and maximum by x
        """
        denominator = maximum - minimum
        if denominator == 0: return 0.0

        val = (x - minimum) / denominator
        return Math.clamp(val, 0.0, 1.0) if clamped else val

    @staticmethod
    def get_lerp_value(
        x: float,
        minimum: float,
        maximum: float,
        clamped: bool = False,
    ) -> float:
        """
        Calculates the progress (0.0 to 1.0) of x between minimum and maximum.
        Equivalent to Terraria's Utils.GetLerpValue.
        """
        return Utils.smooth_step(x, minimum, maximum, clamped)

    @staticmethod
    def remap(
        x: float, 
        from_min: float, 
        from_max: float, 
        to_min: float, 
        to_max: float, 
        clamped: bool = True,
    ) -> float:
        """
        Remaps a value from one range to another.
        Equivalent to Terraria's Utils.Remap.
        """
        amount = Utils.get_lerp_value(x, from_min, from_max, clamped)
        return Math.lerp(to_min, to_max, amount)

    @staticmethod
    def linear_gradient(
        start_color: tuple,
        end_color: tuple,
        count: int = 256
    ) -> list[tuple]:
        """
        Returns a list of `count` RGB tuples interpolating linearly from
        `start_color` to `end_color`, inclusive on both ends.

        count must be greater than 1, otherwise raises a ValueError.
        """
        if count < 2:
            raise ValueError("Gradient requires at least 2 colors.")
        count -= 1
        color_array = [
            tuple(int(Math.lerp(s, e, i / count)) for s, e in zip(start_color, end_color))
            for i in range(count)
        ]
        color_array.append(end_color)
        return color_array
