import struct
from datetime import datetime, timedelta, timezone


class NetDateTime:
    """
    Utility for converting between Python datetime and .NET DateTime binary format.

    .NET DateTime binary layout (64-bit):
    - Bits 0–61  : ticks (100-nanosecond intervals since 0001-01-01)
    - Bits 62–63 : kind
        0 = Unspecified
        1 = UTC
        2 = Local
    """

    # .NET Ticks start at 0001-01-01 00:00:00
    DOTNET_EPOCH = datetime(1, 1, 1, tzinfo=timezone.utc)

    # Number of ticks per second (1 tick = 100ns; 10 million ticks = 1s)
    TICKS_PER_SECOND = 10_000_000

    # Bit masks
    TICKS_MASK = 0x3FFFFFFFFFFFFFFF
    KIND_MASK = 0xC000000000000000

    # Flags for .NET DateTimeKind (stored in the 2 MSB)
    KIND_UNSPECIFIED = 0x00
    KIND_UTC         = 0x01
    KIND_LOCAL       = 0x02

    @classmethod
    def from_binary(cls, value: int) -> datetime:
        """
        Convert a .NET DateTime binary (Int64) into a Python datetime.
        """
        # Normalize to unsigned 64-bit
        raw = value & 0xFFFFFFFFFFFFFFFF

        # Extract kind from the top 2 bits
        kind = (raw >> 62) & 0x03

        # Extract ticks from the remaining 62 bits
        ticks = raw & cls.TICKS_MASK

        # Calculate base UTC time
        utc_dt = cls.DOTNET_EPOCH + timedelta(microseconds=ticks // 10)

        # Apply kind behavior
        if kind == cls.KIND_LOCAL:
            # Convert to local time, return naive (matches .NET typical usage)
            return utc_dt.astimezone().replace(tzinfo=None)

        if kind == cls.KIND_UTC:
            return utc_dt

        # Unspecified → return naive datetime
        return utc_dt.replace(tzinfo=None)

    @classmethod
    def to_binary(cls, value: datetime | None = None) -> int:
        """
        Convert a Python datetime into .NET DateTime binary (Int64).
        """
        if value is None:
            value = datetime.now()

        # Ensure timezone-aware
        if value.tzinfo is None:
            # Assume local time if naive
            value = value.astimezone()

        # Convert to UTC for tick calculation
        utc_dt = value.astimezone(timezone.utc)

        # Compute ticks
        delta = utc_dt - cls.DOTNET_EPOCH
        ticks = int(delta.total_seconds() * cls.TICKS_PER_SECOND)

        # Set kind to Local
        raw = (ticks & cls.TICKS_MASK) | (cls.KIND_LOCAL << 62)

        # Convert to signed 64-bit (matches .NET "long")
        return struct.unpack("q", struct.pack("Q", raw))[0]

    @classmethod
    def bin(cls, value: datetime | int | None = None) -> datetime | int:
        """
        Smart helper:
        - int      → datetime
        - datetime → int
        - None     → current datetime → int
        """
        if isinstance(value, int):
            return cls.from_binary(value)
        return cls.to_binary(value)