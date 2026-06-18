from .pillarsinfo import PillarsInfo


class LunarEvents:
    """Lunar Events (Lunar Pillars) related information."""

    def __init__(self, apocalypse: bool, pillars_present: PillarsInfo):
        self.apocalypse: bool = apocalypse
        """If the Lunar Events are active or not."""

        self.pillars_present: PillarsInfo = pillars_present
        """Which pillars are currently present in the world."""

    def __repr__(self):
        return f"WorldLunarEvents(are_active={self.apocalypse}, pillars_present={repr(self.pillars_present)})"
