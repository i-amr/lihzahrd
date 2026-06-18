import typing
import struct
import uuid

from .rect import Rect


class FileWriter:
    """Helper class for serializing a Terraria world file with context management."""

    __slots__ = (
        "file",
        "_should_close",
    )

    def __init__(self, file_or_path: typing.Union[typing.BinaryIO, str]) -> None:
        if isinstance(file_or_path, str):
            # Open for writing in binary mode
            self.file: typing.BinaryIO = open(file_or_path, "wb")
            self._should_close = True
        else:
            self.file: typing.BinaryIO = file_or_path
            self._should_close = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._should_close:
            self.file.close()

    # Pre-compiled struct packers
    _bool = struct.Struct("<?").pack
    _int1 = struct.Struct("<b").pack
    _uint1 = struct.Struct("<B").pack
    _int2 = struct.Struct("<h").pack
    _uint2 = struct.Struct("<H").pack
    _int4 = struct.Struct("<i").pack
    _uint4 = struct.Struct("<I").pack
    _int8 = struct.Struct("<q").pack
    _uint8 = struct.Struct("<Q").pack
    _single = struct.Struct("<f").pack
    _double = struct.Struct("<d").pack
    _rect = struct.Struct("<iiii").pack

    def bool(self, value: bool) -> None:
        self.file.write(self._bool(value))

    def int1(self, value: int) -> None:
        self.file.write(self._int1(value))

    def uint1(self, value: int) -> None:
        self.file.write(self._uint1(value))

    def int2(self, value: int) -> None:
        self.file.write(self._int2(value))

    def uint2(self, value: int) -> None:
        self.file.write(self._uint2(value))

    def int4(self, value: int) -> None:
        self.file.write(self._int4(value))

    def uint4(self, value: int) -> None:
        self.file.write(self._uint4(value))

    def int8(self, value: int) -> None:
        self.file.write(self._int8(value))

    def uint8(self, value: int) -> None:
        self.file.write(self._uint8(value))

    def single(self, value: float) -> None:
        self.file.write(self._single(value))

    def double(self, value: float) -> None:
        self.file.write(self._double(value))

    def bits(self, values: typing.Sequence[bool]) -> None:
        """Compresses a sequence of bools (up to 8) into a single byte."""
        byte = 0
        for i, val in enumerate(values):
            if i >= 8:
                break
            if val:
                byte |= 1 << i
        self.uint1(byte)

    def rect(self, value: Rect) -> None:
        self.file.write(self._rect(value.left, value.right, value.top, value.bottom))

    def uleb128(self, value: int) -> None:
        """Writes an integer using Base-128 VarInt encoding."""
        while value >= 0x80:
            self.uint1((value & 0x7F) | 0x80)
            value >>= 7
        self.uint1(value)

    def string(self, value: str, leb128=True) -> None:
        """Writes a string prefixed by its ULEB128 length."""
        data = value.encode("utf-8")
        if leb128:
            self.uleb128(len(data))
        self.file.write(data)

    def uuid(self, value: uuid.UUID) -> None:
        # Terraria uses little-endian bytes for UUIDs
        self.file.write(value.bytes_le)

    def tell(self) -> int:
        return self.file.tell()

    def seek(self, address: int) -> None:
        self.file.seek(address)

    def __repr__(self):
        return f"<FileWriter at {self.tell():02x}>"
