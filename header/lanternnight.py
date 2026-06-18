class LanternNight:
    """Lantern Night event related information."""

    def __init__(
        self,
        manual: bool,
        natural: bool,
        cooldown: int,
        next_night_is_lantern_night: bool,
    ):
        self.manual: bool = manual
        """Was this night started by the player?"""

        self.natural: bool = natural
        """Was this night started by the game spontaneously?"""

        self.cooldown: int = cooldown
        """How many nights before the next lantern night can happen."""

        self.next_night_is_lantern_night: bool = next_night_is_lantern_night
        """Was a boss just defeated, making the next night a Lantern Night?"""

    def __repr__(self):
        return f"LanternNight(cooldown={self.cooldown}, natural={self.natural}, manual={self.manual}, cooldown={self.cooldown})"

    @property
    def is_active(self):
        return self.manual or self.natural
