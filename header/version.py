import typing

class Version:
    """A Terraria version handler for mapping engine IDs to content limits."""

    __slots__ = ("id",)

    # Version Name -> Internal Engine ID
    _versions = {
        "1.4.0"    : 224,
        "1.4.0.1"  : 225,
        "1.4.0.2"  : 226,
        "1.4.0.3"  : 227,
        "1.4.0.4"  : 228,
        "1.4.0.5.1": 229,
        "1.4.0.5"  : 230,

        "1.4.1"    : 232,
        "1.4.1.1"  : 233,
        "1.4.1.2"  : 234,
        "1.4.2"    : 235,
        "1.4.2.1"  : 236,
        "1.4.2.2"  : 237,
        "1.4.2.3"  : 238,

        "1.4.3"    : 242,
        "1.4.3.1"  : 243,
        "1.4.3.2"  : 244,
        "1.4.3.3"  : 245,
        "1.4.3.4"  : 246,
        "1.4.3.5"  : 247,
        "1.4.3.6"  : 248,

        "1.4.4"    : 269,
        "1.4.4.1"  : 270,
        "1.4.4.2"  : 271,
        "1.4.4.3"  : 272,
        "1.4.4.4"  : 273,
        "1.4.4.5"  : 274,
        "1.4.4.6"  : 275,
        "1.4.4.7"  : 276,
        "1.4.4.8"  : 277,
        "1.4.4.8.1": 278,
        "1.4.4.9"  : 279,

        "1.4.5.0"  : 315,
        "1.4.5.1"  : 315,
        "1.4.5.2"  : 315,
        "1.4.5.3"  : 316,
        "1.4.5.4"  : 317,
        "1.4.5.5"  : 318,
        "1.4.5.6"  : 319,
    }

    # Reverse mapping for the .name property
    _id_to_name = {v: k for k, v in _versions.items()}

    def __init__(self, data: typing.Union[int, str]):
        if isinstance(data, int):
            self.id = data
        elif data in self._versions:
            self.id = self._versions[data]
        else:
            raise ValueError(f"Unknown version string: {data}")

    def _get_limit(self, mapping: typing.Dict[typing.Iterable[int], int]) -> typing.Optional[int]:
        """Helper to find limits based on ID membership."""
        for ids, value in mapping.items():
            if self.id in ids:
                return value
        return None

    @property
    def max_tile_id(self) -> typing.Optional[int]:
        limits = {
            range(224, 231): 622,
            range(232, 239): 623,
            range(242, 249): 624,
            range(269, 280): 692,
            range(315, 320): 752
        }
        return self._get_limit(limits)

    @property
    def max_wall_id(self) -> typing.Optional[int]:
        limits = {
            range(224, 249): 315,
            range(269, 280): 346,
            range(315, 320): 366,
        }
        return self._get_limit(limits)

    @property
    def max_item_id(self) -> typing.Optional[int]:
        limits = {
            range(224, 229): 5042,
            (230,)         : 5044,
            range(232, 239): 5087,
            range(242, 249): 5124,
            range(269, 274): 5452,
            range(274, 280): 5455,
            range(315, 319): 6144,
            (319,)         : 6146,
        }
        return self._get_limit(limits)

    @property
    def max_npc_id(self) -> typing.Optional[int]:
        limits = {
            range(224, 231): 662,
            range(232, 237): 664,
            (237,)         : 666,
            (238,)         : 667,
            range(242, 249): 669,
            range(269, 280): 687,
            range(315, 320): 696,
        }
        return self._get_limit(limits)

    @property
    def max_moon_id(self) -> typing.Optional[int]:
        limits = {
            range(224, 320): 9,
        }
        return self._get_limit(limits)

    @property
    def name(self) -> str:
        return self._id_to_name.get(self.id, f'Unknown ({self.id})')

    def __repr__(self):
        return f"Version ({self.id})"

    def __str__(self):
        return self.name

    def __eq__(self, value):
        if isinstance(value, int):
            return self.id == value
        else:
            return self.id == getattr(value, 'id', None)

    def __gt__(self, value):
        if isinstance(value, int):
            return self.id > value
        else:
            return self.id > getattr(value, 'id', None)

    def __lt__(self, value):
        if isinstance(value, int):
            return self.id < value
        else:
            return self.id < getattr(value, 'id', None)

    def __ne__(self, value):
        if isinstance(value, int):
            return self.id != value
        else:
            return self.id != getattr(value, 'id', None)

    def __ge__(self, value):
        if isinstance(value, int):
            return self.id >= value
        else:
            return self.id >= getattr(value, 'id', None)

    def __le__(self, value):
        if isinstance(value, int):
            return self.id <= value
        else:
            return self.id <= getattr(value, 'id', None)

    def __add__(self, value):
        if isinstance(value, int):
            return Version(self.id + value)
        else:
            return Version(self.id + getattr(value, 'id', None))

    def __sub__(self, value):
        if isinstance(value, int):
            return Version(self.id - value)
        else:
            return Version(self.id - getattr(value, 'id', None))

    def __int__(self):
        return self.id

    def __index__(self):
        return self.id

    def __bool__(self):
        return self.id != 0
