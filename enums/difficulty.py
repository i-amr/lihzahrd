from __future__ import annotations

import enum


class Difficulty(enum.IntEnum):
    """All difficulty levels from classic to master. except for legendary"""

    CLASSIC = 0  # NORMAL
    EXPERT  = 1  # MEDIUMCORE
    MASTER  = 2  # HARDCORE
    JOURNEY = 3  # CREATIVE
    # LEGENDARY = 999

    def __repr__(self):
        return f"Difficulty.{self.name}"

    @classmethod
    def get(cls, i: int | float) -> Difficulty:
        if isinstance(i, int):
            if 0 <= i <= 3: return cls(i)
        elif isinstance(i, float):
            if i >= 3: return cls(2)
            if i >= 2: return cls(1)
            if i >= 1: return cls(0)
            if i >= 0: return cls(3)
        return cls(0)
