class Party:
    """NPC Party related information."""

    def __init__(
        self,
        manual: bool,
        natural: bool,
        cooldown: int,
        is_doomed: bool,
        partying_npcs: list[int],
    ):
        self.manual: bool = manual
        """If the party was started by a Party Center."""

        self.natural: bool = natural
        """If the item was spontaneously thrown by NPCs."""

        self.cooldown: int = cooldown
        """How long a party cannot be started for."""

        self.is_doomed: bool = is_doomed
        """If all NPCs will die after this party ends."""

        self.partying_npcs: list[int] = partying_npcs
        """The list of NPC IDs that threw the party."""

    def __repr__(self):
        return f"Party(is_doomed={self.is_doomed}, manual={self.manual}, natural={self.natural}, cooldown={self.cooldown}, partying_npcs={self.partying_npcs})"

    @property
    def is_active(self):
        return self.manual or self.natural
