class Pointers:
    """Pointers to the various sections of the Terraria save file.

    All values are in number of bytes from the start."""

    __slots__ = (
        "file_format",
        "world_header",
        "world_tiles",
        "chests",
        "signs",
        "npcs",
        "tile_entities",
        "pressure_plates",
        "town_manager",
        "bestiary",
        "journey_powers",
        "footer",
        "unknown",
    )

    _FIELD_ORDER = __slots__

    def __init__(
        self,
        world_header: int,
        world_tiles: int,
        chests: int,
        signs: int,
        npcs: int,
        tile_entities: int,
        pressure_plates: int,
        town_manager: int,
        bestiary: int,
        journey_powers: int,
        footer: int,
        *unknown,
    ):
        self.file_format: int = 0
        self.world_header: int = world_header
        self.world_tiles: int = world_tiles
        self.chests: int = chests
        self.signs: int = signs
        self.npcs: int = npcs
        self.tile_entities: int = tile_entities
        self.pressure_plates: int = pressure_plates
        self.town_manager: int = town_manager
        self.bestiary: int = bestiary
        self.journey_powers: int = journey_powers
        self.footer: int = footer
        self.unknown: list[int] = list(unknown)

    def __getitem__(self, item: int):
        if not isinstance(item, int):
            raise TypeError("Pointers indices must be integers")

        if 0 <= item < len(self._FIELD_ORDER) - 1:
            return getattr(self, self._FIELD_ORDER[item])

        unknown_index = item - (len(self._FIELD_ORDER) - 1)
        if 0 <= unknown_index < len(self.unknown):
            return self.unknown[unknown_index]

        raise IndexError("Pointers index out of range")

    def __len__(self):
        return len(self._FIELD_ORDER) - 1 + len(self.unknown)

    def __repr__(self):
        return ', '.join([f"{k}={getattr(self, k)}" for k in self._FIELD_ORDER])
